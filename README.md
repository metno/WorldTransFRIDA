# FRIDA

**FRIDA** — the *Feedback-based knowledge Repository for Integrated Assessments* — is a global,
one-region integrated assessment model that treats the human world and the Earth system as a
single, fully coupled whole. Rather than passing information between a climate model and an
economic model through fixed scenarios, it represents emissions, the climate's response, the
resulting impacts, and the human reactions to those impacts as one continuous web of feedback.
There are no exogenous emission pathways and no prescribed growth trajectories: outcomes emerge
from the structure itself.

> **Funding**
> This research was supported by the Horizon Europe research and innovation programs under grant agreement no. 101081661 (WorldTrans).

| | |
|---|---|
| **Try it live** | **[frida.earth](https://frida.earth/)** — the interactive learning environment. Adjust policies and scenarios in your browser and watch the feedbacks play out. |
| **Documentation** | **[metno.github.io/WorldTransFRIDA](https://metno.github.io/WorldTransFRIDA/)** — module overviews plus a full reference for every stock, flow, and parameter. |
| **Project** | [WorldTrans](https://worldtrans-horizon.eu/) |

## About the model

FRIDA deliberately trades spatial and sectoral specificity for *feedback complexity* — the
dynamics that arise when many interconnected processes act on one another. It is built with the
System Dynamics method, expressing real-world processes as a coupled system of differential
equations grounded in physical law, well-established empirical relationships, and leading theory
from economics and environmental psychology.

It is not an optimising model. Rather than assuming perfectly rational agents, it simulates how
people form and revise expectations and adjust their behavior under uncertainty. Because the
whole model runs in seconds, it can be executed as large ensembles that sample parametric
uncertainty across the entire human–climate system, so results carry explicit, quantified
confidence bounds rather than a false sense of precision. Each subsystem is calibrated against
historical observations from around 1980 onward, and validated both for the behavior it
reproduces and for the structural soundness of the processes generating it.

### The model's scope

Population, economic output, energy demand and the evolving fuel mix, agricultural production
and land use, the carbon cycle, radiative forcing, temperature, sea level, climate impacts,
dietary and transport behavior, and the financial system are all endogenous.

The only external drivers are the natural ones — solar variation and volcanic forcing — plus a set of policy levers: carbon pricing, energy taxes and subsidies, support for carbon
capture and removal, coastal adaptation spending, fiscal settings, and demand-side overrides.
These are available as deliberate "what-if" experiments, and even then the human system responds
to a policy rather than having an outcome imposed on it.

### Modules

The model is organised into nine top-level modules, each documented with a conceptual overview
and a complete variable reference on the
[documentation site](https://metno.github.io/WorldTransFRIDA/):

Climate · Demographics · Economy · Energy · Land Use & Agriculture · Resources ·
Behavioral Change · Behavioral Choices · Government Regulations

## Running the model

FRIDA is developed in
[Stella Architect](https://www.iseesystems.com/store/products/stella-architect.aspx). You can run
and explore it locally without purchasing Stella Architect using the free
[isee Player](https://www.iseesystems.com/softwares/player/iseeplayer.aspx) — or online, with no
install at all, at [frida.earth](https://frida.earth/).

## Publications

FRIDA and its components are documented in the Geoscientific Model Development
collection
**[The FRIDA model – a.k.a. "Feedback-based knowledge Repository for IntegrateD Assessments"](https://gmd.copernicus.org/articles/collection12.html)**,
which lists every paper as it is published, along with the citation to use for the
model as a whole. All papers are open access, with BibTeX/RIS export.

## Documentation website

**<https://metno.github.io/WorldTransFRIDA/>** — the published FRIDA documentation: a
paper-grounded overview of each module, plus a complete, auto-generated reference for every
stock, flow, and parameter in the model.

Use the version selector in the site header to switch between model versions:

| Version | Branch | Direct link |
|---|---|---|
| **v3.1** (current) | `main` | <https://metno.github.io/WorldTransFRIDA/main/> |
| v2.1 | `v2` | <https://metno.github.io/WorldTransFRIDA/v2/> |

The site is built with [MkDocs](https://www.mkdocs.org/) + [Material](https://squidfunk.github.io/mkdocs-material/)
and generated from the model files (`FRIDA.stmx`, `FRIDA_Modules/*.itmx`) and authored module
narratives. It rebuilds and republishes automatically on every push to `main` or `v2`.
Everything for the site lives in [`docs/`](docs/).

To extend a module's narrative, edit the matching `docs/science/<module>.md` partial. The
generated pages, `mkdocs.yml`, and the built site (`docs-site/`) are **not** tracked, and hand
edits to them are overwritten on the next build.

## Input data processing
<ul>
  <li>
    <a href="https://github.com/chrisdwells/FRIDA-emissions">Calibration Emissions, Concentrations, and Forcings</a>
  </li>
  <li>
    <a href="https://github.com/chrisdwells/calibrate-FRIDA-climate">Climate Module Calibration</a>
  </li>
  <li>
    <a href="https://github.com/chrisdwells/FRIDA-forcings">Simplified Climate Forcings</a>
  </li>
  <li>
    <a href="https://github.com/chrisdwells/FRIDA-misc-forcings">Miscellaneous Climate Forcings</a>
  </li>
  <li>
    <a href="https://github.com/lnnrtrmm/Carbon-Climate-Box-Model">Ocean Carbon Cycle Model</a>
  </li>
  <li>
    <a href="https://github.com/lnnrtrmm/FRISIA">Sea level Rise (Impacts) Model</a>
  </li>
  <li>
    <a href="https://github.com/jnnsbrr/frida_biosphere_data">Biosphere Data Processing</a>
  </li>
  <li>
    Climate Impacts processing
    <ul>
      <li><a href="https://github.com/chrisdwells/climate-labour-impacts">Labour Productivity</a></li>
      <li><a href="https://github.com/chrisdwells/climate-crops-impacts">Crop Yield</a></li>
      <li><a href="https://github.com/chrisdwells/temperature-mortality">Mortality</a></li>
      <li><a href="https://github.com/chrisdwells/climate-energy-supply">Energy Supply</a></li>
      <li><a href="https://github.com/chrisdwells/extremes-exposure">Exposure to Climate Extremes</a></li>
      <li><a href="https://github.com/chrisdwells/cdd-hdd">Cooling and Heating Degree Days</a></li>
      <li><a href="https://github.com/chrisdwells/FRIDA-climate-impacts">Uncertainty Parameter Sets</a></li>
    </ul>
  </li>
</ul>

## Output data processing
<ul>
  <li>
    <a href="https://github.com/BenjaminBlanz/WorldTransFrida-Uncertainty">Uncertainty Analysis</a>
  </li>
  <li>
    <a href="https://github.com/adakudlum/make_plots_from_FRIDA_output">Plotting</a>
  </li>
  <li>
    <a href="https://github.com/BenjaminBlanz/WorldTransFRIDA-SimpleDashboard">Simple Dashboard</a>
  </li>
  <li>
    <a href="https://frida.earth/">frida.earth</a> — the latest Interactive Learning Environment, hosted and ready to use
  </li>
  <li>
    <a href="https://github.com/BenjaminBlanz/WorldTransFRIDA-ILE">Interactive Learning Environment (repository)</a>
  </li>
  <li>
    <a href="https://github.com/alecceckert/FRIDA-IAMC-Post-Processing">Post Processing for Scenario Compass and IAM Diagnostics
    </a>
  </li>
</ul>
 
## Calibration Data

See the Documentation tab in the <a href="https://github.com/metno/WorldTransFRIDA/blob/main/Data/Calibration%20Data.csv">Calibration Data file</a>
 
## Standalone Climate Model

The standalone climate model based on the climate and land use components of FRIDA, <a href="https://github.com/chrisdwells/FRIDA-Clim">FRIDA-Clim</a>
