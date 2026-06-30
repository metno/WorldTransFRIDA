"""
gen_docs.py — Generate the FRIDA documentation site (MkDocs + Material) from the
parsed model.

This script and its inputs live inside ``docs/`` alongside the content:
  gen_docs.py / parse_frida_model.py        the generator (excluded from the build)
  science/<name>.md                         authored prose partials (excluded; inlined)

It writes, into ``docs/``:
  index.md                                  landing page
  architecture.md                           module map + how modules connect
  conventions.md                            how to read the reference (types, tags)
  modules/<module>/index.md                 conceptual overview (paper content goes here)
  modules/<module>/reference/<submodel>.md  auto-generated variable reference

Also (re)writes the whole ``mkdocs.yml`` (theme, nav, exclude_docs). The built
site goes to ``docs-site/`` (``mkdocs build``).

Run:  .venv/bin/python docs/gen_docs.py
"""
from __future__ import annotations

import os
import re
import shutil
from collections import defaultdict

from parse_frida_model import (
    REPO, build_registry, norm, ident, qualify,
    build_connect_map, resolve_source, build_dimension_names,
)

DOCS = os.path.join(REPO, "docs")
SCIENCE = os.path.join(DOCS, "science")  # authored prose partials, inlined into overviews

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def slug(s: str) -> str:
    s = s.replace("&", " and ")
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-+", "-", s) or "x"


def anchor(s: str) -> str:
    return slug(s)


# Human descriptions for the (canonical) classification tags shown in the docs.
TAG_INFO = {
    "Policy": ("Policy lever", "A variable intended to be changed to represent a policy intervention or scenario."),
    "Assumption": ("Assumption", "A value set by modeller judgement rather than fit to data."),
    "Internal Calibration Parameter": ("Internal calibration parameter", "A parameter tuned internally so the model reproduces historical data."),
    "External Calibration Parameter": ("External calibration parameter", "A calibration parameter constrained by external data."),
    "Calibrated": ("Calibrated", "Calibrated against data."),
    "Climate Impact Parameter": ("Climate-impact parameter", "Governs how climate change translates into an impact (e.g. on crops, mortality, labour)."),
    "Unit": ("Unit helper", "A units-conversion or bookkeeping helper variable."),
}

# Canonicalisation of the raw model tags onto the smaller set above.
# A raw tag maps to its displayed tag; a tag mapped to None is dropped entirely.
# Tags not listed here are kept verbatim.
TAG_CANON = {
    "Parameter": "Assumption",
    "External Parameter": "Assumption",
    "Calibrated Output": "Calibrated",
    "Explanatory Variable": None,
    "Output": None,
    "No Sensi": None,
    "Discrete Outflow": None,
}


def canon_tags(tags):
    """Apply TAG_CANON: remap/drop raw tags, dedupe, preserve order."""
    out = []
    for t in tags:
        c = TAG_CANON.get(t, t)
        if c and c not in out:
            out.append(c)
    return out

TYPE_BADGE = {"stock": "stock", "flow": "flow", "aux": "aux"}


def badge(kind: str) -> str:
    return f'<span class="badge badge-{kind}">{kind}</span>'


def tag_spans(tags) -> str:
    out = []
    for t in canon_tags(tags):
        label = TAG_INFO.get(t, (t, ""))[0]
        out.append(f'<span class="tag tag-{slug(t)}" title="{TAG_INFO.get(t,(t,t))[1]}">{label}</span>')
    return " ".join(out)


def fence(code: str) -> str:
    return "```text\n" + code.strip() + "\n```"


def read_partial(name: str) -> str | None:
    """Return the contents of an authored science partial, or None."""
    p = os.path.join(SCIENCE, f"{name}.md")
    if os.path.isfile(p):
        with open(p) as f:
            txt = f.read().strip()
        return txt or None
    return None


def esc(s: str) -> str:
    return s.replace("|", "\\|")


# ---------------------------------------------------------------------------
# build hierarchy: top-level modules + their descendants (flattened, ordered)
# ---------------------------------------------------------------------------

reg, ROOT = build_registry()
CMAP = build_connect_map()

# Per-module replacement table: local input identifier -> qualified source string.
# Used to (a) list a module's inputs and (b) rewrite equations so cross-module
# inputs read as e.g. "GDP.Real_GDP_in_2021c$" instead of "Converter_2".
module_inputs = {}      # module_norm -> { local_ident: qualified_source_str }
for (tm, tv), (fm, fv) in CMAP.items():
    sm, sv = resolve_source(CMAP, tm, tv)
    if sm:
        module_inputs.setdefault(tm, {})[tv] = qualify(sm, sv)


def is_input(mod_norm, v) -> bool:
    """True if a variable is a module input (a port fed from another module),
    rather than something this module computes itself."""
    return v.access == "input" or ident(v.raw_name) in module_inputs.get(mod_norm, {})


DIMS = build_dimension_names()

# Per-module equation rewrite table: identifier -> fully-qualified reference.
# Inputs map to their resolved source; local variables map to "Module.self".
# Dimension/element names are excluded so subscripts are left untouched.
eqn_repl = {}
for _md in reg.values():
    table = dict(module_inputs.get(_md.name, {}))
    for v in _md.vars:
        i = ident(v.raw_name)
        if i in DIMS or i in table:
            continue
        table[i] = qualify(_md.name, v.raw_name)
    if table:
        eqn_repl[_md.name] = table

# A reference is an optional "Module." prefix followed by a bare or quoted name.
_REF = re.compile(r'(?<![\w$.])([A-Za-z_][A-Za-z0-9_]*\.)?("[^"]*"|[A-Za-z_][A-Za-z0-9_$]*)')


def rewrite_eqn(eqn: str, mod_norm: str) -> str:
    """Qualify every variable name in an equation as ``Module.variable``.

    Input ports resolve to their true cross-module source; local variables are
    prefixed with their own module. Already-qualified references, dimension
    names, numbers, and built-in functions are left untouched.
    """
    table = eqn_repl.get(mod_norm)
    if not eqn or not table:
        return eqn

    def repl(m):
        if m.group(1):          # already qualified (Module.var) -> leave as-is
            return m.group(0)
        name = m.group(2)
        return table.get(name.strip('"'), name)

    return _REF.sub(repl, eqn)


def children(name):
    md = reg.get(name)
    return md.module_refs if md else []


# top-level modules = direct children of FRIDA root
TOP = children(ROOT)

# assign every reachable model to a top-level ancestor, preserving DFS order
descendants = defaultdict(list)   # top norm-name -> [ (depth, norm-name) ] excluding the top itself
model_parent = {}                  # norm-name -> parent norm-name
_seen = set()


def walk(name, top, depth):
    if name in _seen:
        return
    _seen.add(name)
    if name != top:
        descendants[top].append((depth, name))
    for c in children(name):
        model_parent[c] = name
        walk(c, top, depth + 1)


_seen = {ROOT}
for t in TOP:
    model_parent[t] = ROOT
    walk(t, t, 0)

# attach orphan models to the top-level module that owns most models from the
# same source file
file_to_top = {}
for t in TOP:
    files = defaultdict(int)
    files[reg[t].file] += 1
    for _, d in descendants[t]:
        files[reg[d].file] += 1
    for f in files:
        file_to_top.setdefault(f, []).append((files[f], t))

orphans = [n for n in reg if n not in _seen and n != ROOT]
for o in orphans:
    cand = file_to_top.get(reg[o].file)
    if cand:
        top = sorted(cand, reverse=True)[0][1]
        descendants[top].append((0, o))
        model_parent[o] = top

# nice display titles for the 9 top-level modules
TOP_TITLES = {
    "Energy": "Energy",
    "Demographics": "Demographics",
    "Climate": "Climate",
    "Land_Use_and_Agriculture": "Land Use & Agriculture",
    "Behavioral_Choices": "Behavioral Choices",
    "Government_Regulations": "Government Regulations",
    "Behavioral_Change": "Behavioral Change",
    "Resources": "Resources",
    "Economy": "Economy",
}

# page path for each model's reference (relative to docs/)
ref_path = {}
for t in TOP:
    tslug = slug(reg[t].display)
    # the container's own vars get a page too if it has any
    for depth, n in descendants[t]:
        ref_path[n] = f"modules/{tslug}/reference/{slug(reg[n].display)}.md"
    if reg[t].vars:
        ref_path[t] = f"modules/{tslug}/reference/{slug(reg[t].display)}-core.md"

# global variable index: clean lower name -> list of (display, top, path, anchor)
var_index = defaultdict(list)


def register_vars(md, top):
    p = ref_path.get(md.name)
    if not p:
        return
    web = p[:-3]  # strip .md
    for v in md.vars:
        var_index[v.name.lower()].append((v.name, top, web, anchor(v.name)))


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------

def render_var(v, mnorm) -> str:
    qname = qualify(mnorm, v.raw_name)          # e.g. GDP.Real_GDP_in_2021c$
    parts = [f"### {qname} {{#{anchor(qname)}}}", ""]
    meta = badge(v.kind)
    ts = tag_spans(v.tags)
    if ts:
        meta += " " + ts
    parts.append(meta)
    parts.append("")
    facts = []
    if v.units:
        facts.append(f"**Units:** {v.units}")
    if v.dims:
        facts.append(f"**Dimensions:** {', '.join(v.dims)}")
    if v.rng:
        lo, hi = v.rng
        facts.append(f"**Range:** {lo} – {hi}")
    if v.kind == "stock":
        if v.inflows:
            facts.append("**Inflows:** " + ", ".join(qualify(mnorm, f) for f in v.inflows))
        if v.outflows:
            facts.append("**Outflows:** " + ", ".join(qualify(mnorm, f) for f in v.outflows))
    if v.is_graphical:
        facts.append("**Graphical function**")
    if facts:
        parts.append("  ·  ".join(facts))
        parts.append("")
    if v.doc:
        for line in v.doc.split("\n"):
            parts.append(f"> {line}" if line.strip() else ">")
        parts.append("")
    if v.eqn:
        label = "Initial value" if v.kind == "stock" else "Equation"
        parts.append(f"*{label}:*")
        parts.append(fence(rewrite_eqn(v.eqn, mnorm)))
        parts.append("")
    return "\n".join(parts)


def render_reference(md, top, depth_label) -> str:
    mnorm = md.name
    inset = module_inputs.get(mnorm, {})
    stocks = [v for v in md.stocks if not is_input(mnorm, v)]
    flows = [v for v in md.flows if not is_input(mnorm, v)]
    auxes = [v for v in md.auxes if not is_input(mnorm, v)]

    title = md.display
    lines = [f"# {title}", ""]
    if depth_label:
        lines.append(f"*Sub-model of {depth_label}.*  ")
    lines.append(
        f"`{len(stocks)}` stocks · `{len(flows)}` flows · `{len(auxes)}` auxiliaries/parameters · "
        f"`{len(inset)}` inputs · source: `{md.file}`"
    )
    lines.append("")
    lines.append(
        "Auto-generated reference. Variable names are fully qualified as "
        "`Module.variable`. Each entry shows the variable type, classification "
        "tags, units, range, the modeller's notes, and the model equation."
    )
    lines.append("")

    # Inputs received from other modules — resolved to their true source so a
    # generic port name (e.g. Converter_2) shows its real origin.
    if inset:
        lines.append("## Inputs (from other modules)")
        lines.append("")
        lines.append(
            "Variables this sub-model reads from elsewhere in FRIDA, shown as their "
            "fully-qualified source."
        )
        lines.append("")
        for src in sorted(set(inset.values()), key=str.lower):
            lines.append(f"- `{src}`")
        lines.append("")

    groups = [("Stocks", stocks), ("Flows", flows), ("Auxiliaries & parameters", auxes)]
    for gname, vs in groups:
        if not vs:
            continue
        lines.append(f"## {gname}")
        lines.append("")
        for v in vs:
            lines.append(render_var(v, mnorm))
    return "\n".join(lines)


def feedback_summary(md):
    """A short textual description of a stock's flow structure."""
    out = []
    for s in md.stocks:
        if is_input(md.name, s):
            continue
        bits = []
        if s.inflows:
            bits.append("increased by " + ", ".join(f"*{x}*" for x in s.inflows))
        if s.outflows:
            bits.append("drained by " + ", ".join(f"*{x}*" for x in s.outflows))
        desc = "; ".join(bits) if bits else "a state variable"
        out.append((s, desc))
    return out


def collect(top):
    """All ModelDefs under a top-level module, container first."""
    mds = [reg[top]] if reg[top].vars else []
    for depth, n in descendants[top]:
        mds.append(reg[n])
    return mds


def render_overview(top) -> str:
    md = reg[top]
    title = TOP_TITLES.get(top, md.display)
    subs = [(depth, reg[n]) for depth, n in descendants[top]]

    # aggregate stats
    all_mds = collect(top)
    n_stock = sum(len(m.stocks) for m in all_mds)
    n_flow = sum(len(m.flows) for m in all_mds)
    n_aux = sum(len(m.auxes) for m in all_mds)
    policy = [(m, v) for m in all_mds for v in m.vars
              if "Policy" in v.tags and not is_input(m.name, v)]

    science = read_partial(slug(md.display))

    L = [f"# {title}", ""]
    if not science:
        L.append(
            "!!! note \"Conceptual overview\"\n"
            "    This page summarises the module's purpose and structure, derived from the "
            "model itself. The scientific narrative will be expanded from the "
            "FRIDA documentation papers.\n"
        )

    # paper-derived narrative leads the page
    if science:
        L.append("## How it works")
        L.append("")
        L.append(science)
        L.append("")

    L.append("## At a glance")
    L.append("")
    L.append(f"- **Sub-models:** {len(subs)}")
    L.append(f"- **Stocks (state variables):** {n_stock}")
    L.append(f"- **Flows:** {n_flow}")
    L.append(f"- **Auxiliaries & parameters:** {n_aux}")
    if policy:
        L.append(f"- **Policy levers:** {len(policy)}")
    L.append(f"- **Source file:** `{md.file}`")
    L.append("")

    # sub-model table
    if subs:
        L.append("## Sub-models")
        L.append("")
        L.append("| Sub-model | Stocks | Flows | Aux/params | Reference |")
        L.append("|---|--:|--:|--:|---|")
        tslug = slug(md.display)
        for depth, sm in subs:
            indent = "&nbsp;&nbsp;" * depth
            p = ref_path.get(sm.name, "")
            link = f"[open](reference/{os.path.basename(p)[:-3]}.md)" if p else ""
            L.append(
                f"| {indent}{esc(sm.display)} | {len(sm.stocks)} | {len(sm.flows)} | {len(sm.auxes)} | {link} |"
            )
        L.append("")

    # core (container) variables
    if md.vars:
        L.append("## Module-level variables")
        L.append("")
        L.append(
            f"This module defines {len(md.vars)} variable(s) directly (outside its sub-models). "
            f"See the [core reference](reference/{slug(md.display)}-core.md)."
        )
        L.append("")

    if not science:
        L.append("## Scientific background")
        L.append("")
        L.append(
            "*To be completed from the FRIDA documentation papers.* "
            "This section will describe the theoretical basis, key relationships, "
            "and calibration approach for this module."
        )
        L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------------------
# static pages
# ---------------------------------------------------------------------------

def page_index() -> str:
    rows = []
    for t in TOP:
        md = reg[t]
        all_mds = collect(t)
        ns = sum(len(m.stocks) for m in all_mds)
        nf = sum(len(m.flows) for m in all_mds)
        na = sum(len(m.auxes) for m in all_mds)
        title = TOP_TITLES.get(t, md.display)
        rows.append(
            f"| [{title}](modules/{slug(md.display)}/index.md) | {len(descendants[t])} | {ns} | {nf} | {na} |"
        )
    tot_models = len(reg)
    tot_s = sum(len(m.stocks) for m in reg.values())
    tot_f = sum(len(m.flows) for m in reg.values())
    tot_a = sum(len(m.auxes) for m in reg.values())
    home = read_partial("_home")
    intro = home if home else (
        "**FRIDA** — the *Feedback-based knowledge Repository for Integrated "
        "Assessments* — is a fully coupled, one-region model of the Earth's coupled "
        "human–climate system. It links the economy, energy, demographics, land use "
        "and agriculture, behaviour, and the carbon cycle and climate into a single "
        "set of feedback loops, with no exogenous emission scenarios: emissions, "
        "climate, impacts, and human responses are all computed endogenously."
    )
    return f"""# FRIDA model documentation

{intro}

!!! tip "Try the interactive simulator"
    Explore FRIDA live in your browser — adjust policies and scenarios and watch the
    feedbacks play out — at **[frida.earth](https://frida.earth/)**.

FRIDA is a **system-dynamics** model built in
[Stella Architect](https://www.iseesystems.com/store/products/stella-architect.aspx).
This site documents the model module by module, combining paper-grounded overviews
with a complete, auto-generated reference of every stock, flow, and parameter.

!!! tip "How this site is organised"
    * **[Model architecture](architecture.md)** — the big picture and how the modules connect.
    * **[Reading the reference](conventions.md)** — variable types, classification tags, and equation notation.
    * **Modules** (left sidebar) — each has a paper-grounded **Overview** plus a full **Reference**.

## Modules

| Module | Sub-models | Stocks | Flows | Aux/params |
|---|--:|--:|--:|--:|
{chr(10).join(rows)}

## Model size

The model comprises **{tot_models} sub-models** containing roughly
**{tot_s} stocks**, **{tot_f} flows**, and **{tot_a} auxiliary variables and
parameters**.

## How to cite

If you use FRIDA in your work, please cite the model description paper:

> Schoenberg, W., Blanz, B., Rajah, J. K., Callegari, B., Wells, C., Breier, J., Grimeland, M. B., Lindqvist, A. N., Ramme, L., Smith, C., Li, C., Mashhadi, S., Muralidhar, A., and Mauritzen, C.: [An overview of FRIDA v2.1: a feedback-based, fully coupled, global integrated assessment model of climate and humans](https://gmd.copernicus.org/articles/18/8047/2025/gmd-18-8047-2025.html), Geoscientific Model Development, 18, 8047–8069, 2025. doi:[10.5194/gmd-18-8047-2025](https://doi.org/10.5194/gmd-18-8047-2025).

The complete set of papers documenting FRIDA is collected in the
[GMD FRIDA special issue](https://gmd.copernicus.org/articles/collection12.html).

!!! info "Source"
    Generated from `FRIDA.stmx` and `FRIDA_Modules/*.itmx`. FRIDA is developed by the
    [WorldTrans](https://worldtrans-horizon.eu/) project (Horizon Europe grant no. 101081661).
    See the repository `README.md` for data-processing pipelines and related tools.
"""


def page_architecture() -> str:
    lines = ["# Model architecture", ""]
    arch = read_partial("_architecture")
    if arch:
        lines.append(arch)
    else:
        lines.append(
            "FRIDA couples the human and Earth systems into one feedback structure. "
            "The nine top-level modules each decompose into sub-models, browsable "
            "from the sidebar."
        )
    lines.append("")
    return "\n".join(lines)


def page_how_to() -> str:
    lines = ["# How to", ""]
    body = read_partial("_how-to")
    if body:
        lines.append(body)
    else:
        lines.append(
            "Practical guides for installing, running, and extending FRIDA. "
            "*To be completed.*"
        )
    lines.append("")
    return "\n".join(lines)


def page_conventions() -> str:
    tag_rows = []
    for tag, (label, desc) in TAG_INFO.items():
        tag_rows.append(f'| {tag_spans([tag])} | {desc} |')
    return f"""# Reading the reference

This page explains the notation used throughout the auto-generated reference.

## Variable types

FRIDA is a system-dynamics model, so every variable is one of three kinds:

| Type | Meaning |
|---|---|
| {badge('stock')} | An **accumulation** (state variable). Stocks integrate their inflows minus outflows over time; their initial value is shown as *Initial value*. |
| {badge('flow')} | A **rate** that adds to or drains a stock. Flows have units of *something per year*. |
| {badge('aux')} | An **auxiliary** variable or **parameter** — an algebraic relationship or a constant, computed instantaneously each time step. |

## Classification tags

Variables carry one or more classification tags (originally stored in the model as
documentation macros). They describe the *role* a variable plays:

| Tag | Meaning |
|---|---|
{chr(10).join(tag_rows)}

## Equations

Equations are shown exactly as defined in the model. A few conventions:

- Names use underscores for spaces, e.g. `Surface_Temperature_Anomaly`.
- Square brackets denote **array subscripts**, e.g. `selected_climate_case[Run]`.
- Names in double quotes contain characters such as `&` or operators, e.g.
  `"Heat_Capacity_of_Land_&_Ocean_Surface"`.
- Built-in functions (`INIT`, `DELAY`, `SMTH1`, `GRAPH`, …) are Stella/XMILE functions.
- For arrayed variables, per-element equations are listed as `[subscript] = …`.

## Time and integration

The model runs from **1980** with a time step of **1/8 year** using 4th-order
Runge–Kutta integration. Historical years are calibrated against data; later years
are projections.
"""


# ---------------------------------------------------------------------------
# write everything
# ---------------------------------------------------------------------------

def write(path, text):
    full = os.path.join(DOCS, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(text.rstrip() + "\n")


def main():
    # clean generated dirs (keep hand-written stylesheets / papers)
    for sub in ["modules"]:
        p = os.path.join(DOCS, sub)
        if os.path.isdir(p):
            shutil.rmtree(p)

    write("index.md", page_index())
    write("architecture.md", page_architecture())
    write("how-to.md", page_how_to())
    write("conventions.md", page_conventions())

    nav_modules = []
    for t in TOP:
        md = reg[t]
        title = TOP_TITLES.get(t, md.display)
        tslug = slug(md.display)
        write(f"modules/{tslug}/index.md", render_overview(t))

        ref_entries = []
        # container core vars
        if md.vars:
            register_vars(md, t)
            write(f"modules/{tslug}/reference/{tslug}-core.md",
                  render_reference(md, t, None))
            ref_entries.append({f"{md.display} (core)": f"modules/{tslug}/reference/{tslug}-core.md"})
        # sub-models
        for depth, n in descendants[t]:
            sm = reg[n]
            register_vars(sm, t)
            parent = reg.get(model_parent.get(n))
            dl = parent.display if parent and parent.name != t else None
            write(ref_path[n], render_reference(sm, t, dl))
            ref_entries.append({sm.display: ref_path[n]})

        module_nav = [{"Overview": f"modules/{tslug}/index.md"}]
        if ref_entries:
            module_nav.append({"Reference": ref_entries})
        nav_modules.append({title: module_nav})

    write_mkdocs_nav(nav_modules)
    print(f"Wrote docs for {len(TOP)} top-level modules, {len(reg)} models total.")
    print(f"Indexed {sum(len(v) for v in var_index.values())} variable entries.")


def yaml_nav(nav, indent=2):
    """Serialise a nav list (of dicts/strings) to YAML lines."""
    pad = " " * indent
    out = []
    for item in nav:
        if isinstance(item, str):
            out.append(f"{pad}- {item}")
        elif isinstance(item, dict):
            (k, v), = item.items()
            if isinstance(v, str):
                out.append(f"{pad}- {yq(k)}: {v}")
            else:
                out.append(f"{pad}- {yq(k)}:")
                out.extend(yaml_nav(v, indent + 4))
    return out


def yq(s):
    """Quote a nav title if needed."""
    if re.search(r"[:&]", s) or s != s.strip():
        return '"' + s.replace('"', '\\"') + '"'
    return s


MKDOCS_HEADER = """\
site_name: FRIDA Model Documentation
site_description: Documentation for the WorldTrans FRIDA integrated assessment model
site_author: WorldTrans / isee systems
copyright: "FRIDA is developed by the WorldTrans project (Horizon Europe grant no. 101081661)."
repo_url: https://github.com/metno/WorldTransFRIDA
repo_name: metno/WorldTransFRIDA
use_directory_urls: true

# The docs/ folder also holds the generator and its sources; keep them out of the build.
site_dir: docs-site
exclude_docs: |
  *.py
  *.pyc
  __pycache__/
  science/

theme:
  name: material
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: teal
      accent: green
      toggle:
        icon: material/weather-night
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: teal
      accent: green
      toggle:
        icon: material/weather-sunny
        name: Switch to light mode
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.sections
    - navigation.top
    - navigation.indexes
    - toc.follow
    - search.suggest
    - search.highlight
    - content.code.copy
  icon:
    repo: fontawesome/brands/github

extra_css:
  - stylesheets/extra.css

# Per-branch deploys are published with `mike`; this adds a branch/version
# selector to the header. See .github/workflows/deploy-docs.yml.
extra:
  version:
    provider: mike

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - tables
  - footnotes
  - toc:
      permalink: true
      toc_depth: 3
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets

plugins:
  - search

nav:
  - Home: index.md
  - Model architecture: architecture.md
  - How to: how-to.md
  - Reading the reference: conventions.md
  - Modules:
"""


def write_mkdocs_nav(nav_modules):
    lines = MKDOCS_HEADER.rstrip("\n").split("\n")
    lines += yaml_nav(nav_modules, indent=6)
    with open(os.path.join(REPO, "mkdocs.yml"), "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
