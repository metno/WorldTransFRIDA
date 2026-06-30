"""
parse_frida_model.py — Parse the FRIDA Stella/XMILE model into a navigable Python model.

FRIDA is stored as an XMILE root file (FRIDA.stmx) plus a set of module files
(FRIDA_Modules/*.itmx). Each file contains one or more <model> elements:

  * The first <model> in a file is a *container* whose <variables> hold <module>
    references (and sometimes a few of its own auxiliaries). Each <module>
    reference names a sub-model.
  * Additional <model name="..."> elements in the same file *define* sub-models.

A <module> reference is resolved to a <model> definition by name (after
normalising spaces / newlines to underscores). Definitions may live in the same
file or in another file (resolved through a global registry).

This module builds:
  * REGISTRY: normalised model-name -> ModelDef
  * a tree rooted at the FRIDA model, following <module> references.

It is import-only; doc generation lives in gen_docs.py.
"""
from __future__ import annotations

import glob
import html
import os
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

X = "{http://docs.oasis-open.org/xmile/ns/XMILE/v1.0}"
ISEE = "{http://iseesystems.com/XMILE}"

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ln(el) -> str:
    """Local (namespace-stripped) tag name."""
    return el.tag.split("}")[-1]


def norm(name: str | None) -> str:
    """Normalise a model/module name for registry lookup."""
    if not name:
        return ""
    name = name.replace("\\n", " ").replace("\n", " ")
    name = html.unescape(name).strip()
    return re.sub(r"\s+", "_", name)


def clean_name(name: str | None) -> str:
    """Human-readable variable/model name."""
    if not name:
        return ""
    name = name.replace("\\n", " ").replace("\n", " ")
    name = html.unescape(name)
    return re.sub(r"\s+", " ", name).strip()


def ident(name: str | None) -> str:
    """Canonical Stella identifier form of a name (spaces -> underscores)."""
    if not name:
        return ""
    name = name.replace("\\n", " ").replace("\n", " ")
    name = html.unescape(name)
    return re.sub(r"\s+", "_", name.strip())


_IDENT_OK = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def qualify(mod_norm: str, var: str) -> str:
    """Fully-qualified Stella reference, quoting the variable part if needed."""
    vi = ident(var)
    if not _IDENT_OK.match(vi):
        vi = '"' + vi + '"'
    return f"{mod_norm}.{vi}" if mod_norm else vi


TAG_RE = re.compile(r"\$\{([^}]*)\}")


def split_doc(raw: str | None):
    """Return (tags:list[str], prose:str) from a raw <doc> string.

    isee stores variable classification tags inline as ``${Tag,Tag2}`` macros
    mixed with free prose. We pull the tags out and keep the remaining prose.
    """
    if not raw:
        return [], ""
    tags: list[str] = []
    for m in TAG_RE.findall(raw):
        for t in m.split(","):
            t = t.strip()
            if t and t not in tags:
                tags.append(t)
    prose = TAG_RE.sub("", raw)
    prose = html.unescape(prose)
    # collapse >2 blank lines, trim each line's trailing ws
    prose = re.sub(r"\n[ \t]+", "\n", prose)
    prose = re.sub(r"\n{3,}", "\n\n", prose).strip()
    return tags, prose


@dataclass
class Var:
    name: str
    raw_name: str
    kind: str  # stock | flow | aux
    units: str = ""
    eqn: str = ""
    tags: list[str] = field(default_factory=list)
    doc: str = ""
    rng: tuple[str, str] | None = None
    inflows: list[str] = field(default_factory=list)
    outflows: list[str] = field(default_factory=list)
    dims: list[str] = field(default_factory=list)
    is_graphical: bool = False
    access: str = ""
    non_negative: bool = False


@dataclass
class ModelDef:
    name: str          # normalised name (registry key)
    display: str       # human name
    file: str          # source filename (basename)
    module_refs: list[str] = field(default_factory=list)   # normalised child names
    vars: list[Var] = field(default_factory=list)

    @property
    def stocks(self):
        return [v for v in self.vars if v.kind == "stock"]

    @property
    def flows(self):
        return [v for v in self.vars if v.kind == "flow"]

    @property
    def auxes(self):
        return [v for v in self.vars if v.kind == "aux"]


def _text(el, tag) -> str:
    c = el.find(X + tag)
    return (c.text or "").strip() if c is not None and c.text else ""


def parse_var(el) -> Var:
    kind = ln(el)
    raw = el.get("name") or ""
    name = clean_name(raw)
    units = _text(el, "units")
    tags, doc = split_doc(el.findtext(X + "doc"))

    # equation: either a top-level <eqn> or per-<element> eqns (arrayed)
    eqn = _text(el, "eqn")
    if not eqn:
        elem_eqns = []
        for e in el.findall(X + "element"):
            sub = e.get("subscript", "")
            ee = (e.findtext(X + "eqn") or "").strip()
            if ee:
                elem_eqns.append(f"[{sub}] = {ee}" if sub else ee)
        if elem_eqns:
            eqn = "\n".join(elem_eqns)

    rng = None
    r = el.find(X + "range")
    if r is not None and (r.get("min") is not None or r.get("max") is not None):
        rng = (r.get("min", ""), r.get("max", ""))

    inflows = [clean_name(c.text).replace("_", " ") for c in el.findall(X + "inflow") if c.text]
    outflows = [clean_name(c.text).replace("_", " ") for c in el.findall(X + "outflow") if c.text]

    dims = []
    d = el.find(X + "dimensions")
    if d is not None:
        dims = [dd.get("name") for dd in d.findall(X + "dim") if dd.get("name")]

    return Var(
        name=name,
        raw_name=raw,
        kind=kind,
        units=units,
        eqn=eqn,
        tags=tags,
        doc=doc,
        rng=rng,
        inflows=inflows,
        outflows=outflows,
        dims=dims,
        is_graphical=el.find(X + "gf") is not None,
        access=el.get("access", ""),
        non_negative=el.find(X + "non_negative") is not None,
    )


def parse_model(model_el, filename: str) -> ModelDef:
    # model names are stored with underscores standing in for spaces
    display = clean_name(model_el.get("name") or os.path.splitext(filename)[0]).replace("_", " ")
    md = ModelDef(name=norm(model_el.get("name") or display), display=display, file=filename)
    vsec = model_el.find(X + "variables")
    if vsec is not None:
        for ch in vsec:
            t = ln(ch)
            if t == "module":
                md.module_refs.append(norm(ch.get("name")))
            elif t in ("stock", "flow", "aux"):
                md.vars.append(parse_var(ch))
    return md


def build_registry():
    """Return (registry, root_name). registry: norm name -> ModelDef."""
    registry: dict[str, ModelDef] = {}
    files = [os.path.join(REPO, "FRIDA.stmx")] + sorted(
        glob.glob(os.path.join(REPO, "FRIDA_Modules", "*.itmx"))
    )
    for f in files:
        base = os.path.basename(f)
        root = ET.parse(f).getroot()
        for model_el in root.iter(X + "model"):
            md = parse_model(model_el, base)
            if not md.name:
                # the unnamed top model of FRIDA.stmx
                md.name = norm("FRIDA")
                md.display = "FRIDA"
            # keep the richest definition if duplicated
            if md.name not in registry or len(md.vars) > len(registry[md.name].vars):
                registry[md.name] = md
    # FRIDA root: the model in FRIDA.stmx (its <model> has no name attr)
    root_name = norm("FRIDA")
    return registry, root_name


def _split_qual(q):
    """'GDP."Real_GDP_in_2021c$"' -> ('GDP', 'Real_GDP_in_2021c$'); bare -> (None, name)."""
    if not q:
        return (None, None)
    if "." not in q:
        return (None, ident(q.strip().strip('"')))
    mod, var = q.split(".", 1)
    return (norm(mod.strip()), ident(var.strip().strip('"')))


def build_dimension_names():
    """Set of all dimension and element names (never qualified in equations)."""
    import glob as _glob
    names = set()
    files = [os.path.join(REPO, "FRIDA.stmx")] + sorted(
        _glob.glob(os.path.join(REPO, "FRIDA_Modules", "*.itmx"))
    )
    for f in files:
        root = ET.parse(f).getroot()
        for d in root.iter(X + "dim"):
            if d.get("name"):
                names.add(ident(d.get("name")))
        for e in root.iter(X + "elem"):
            if e.get("name"):
                names.add(ident(e.get("name")))
    return names


def build_connect_map():
    """Map every connection target (module, var) -> source (module, var).

    Merges the standard ``<connect>`` and isee ``<connect2>`` elements across all
    files. Where the two disagree, a *qualified* source (one that names a module)
    is preferred, because ``<connect2>`` sometimes drops the module qualifier.
    """
    import glob as _glob
    from collections import defaultdict

    raw = defaultdict(list)
    files = [os.path.join(REPO, "FRIDA.stmx")] + sorted(
        _glob.glob(os.path.join(REPO, "FRIDA_Modules", "*.itmx"))
    )
    for f in files:
        root = ET.parse(f).getroot()
        for e in root.iter():
            if ln(e) in ("connect", "connect2"):
                tm, tv = _split_qual(e.get("to"))
                fm, fv = _split_qual(e.get("from"))
                if tm and tv and fv:
                    raw[(tm, tv)].append((fm, fv))
    cmap = {}
    for k, vs in raw.items():
        qual = [x for x in vs if x[0]]      # prefer a source that names a module
        cmap[k] = qual[0] if qual else vs[0]
    return cmap


def resolve_source(cmap, mod_norm, var):
    """Follow the connection chain to a terminal qualified source.

    Returns (module_norm, var_ident). Stops if the chain leaves the qualified
    space (an unqualified source) or loops.
    """
    cur = (mod_norm, ident(var))
    seen = set()
    while cur in cmap and cur not in seen:
        seen.add(cur)
        nxt = cmap[cur]
        if not nxt[0]:
            break
        cur = nxt
    return cur


if __name__ == "__main__":
    reg, root = build_registry()
    print(f"Total models in registry: {len(reg)}")
    cmap = build_connect_map()
    print(f"Connection map entries: {len(cmap)}")
    for m, v in [("Energy_demand", "Converter_2"), ("Finance", "Nominal_GDP"),
                 ("Renewable_energy", "Wind_Energy_Capacity_1")]:
        sm, sv = resolve_source(cmap, m, v)
        print(f"  {m}.{v} -> {qualify(sm, sv)}")

    visited = set()

    def walk(nm, depth=0):
        md = reg.get(nm)
        if md is None:
            print("  " * depth + f"?? UNRESOLVED: {nm}")
            return
        seen = nm in visited
        visited.add(nm)
        s = f"{md.display}  [{md.file}]  stocks={len(md.stocks)} flows={len(md.flows)} aux={len(md.auxes)}"
        print("  " * depth + ("- " if depth else "") + s + (" (repeat)" if seen else ""))
        if not seen:
            for c in md.module_refs:
                walk(c, depth + 1)

    walk(root)
    orphans = set(reg) - visited
    if orphans:
        print("\nOrphan models (defined but not referenced from FRIDA root):")
        for o in sorted(orphans):
            md = reg[o]
            print(f"  {md.display}  [{md.file}]  vars={len(md.vars)}")
