# FRIDA
WorldTrans FRIDA model

This repository contains the FRIDA model (Feedback-based knowledge Repository for Integrated Assessments). More information can be found at our website.  

The model is being developed using <a href="https://www.iseesystems.com/store/products/stella-architect.aspx">Stella Architect</a>.

You can run and use the model locally without purchasing Stella Architect using the <a href="https://www.iseesystems.com/softwares/player/iseeplayer.aspx">isee Player</a>

This research was supported by the Horizon Europe research and innovation programs under grant agreement no. 101081661 (WorldTrans).

## Documentation website

A browsable [MkDocs](https://www.mkdocs.org/) + [Material](https://squidfunk.github.io/mkdocs-material/)
documentation site is generated from the model files (`FRIDA.stmx`, `FRIDA_Modules/*.itmx`)
and authored module narratives. Everything for the site lives in [`docs/`](docs/):

| Path | Purpose |
|---|---|
| `docs/gen_docs.py` | Generator — writes the pages and `mkdocs.yml`. |
| `docs/parse_frida_model.py` | Parses the XMILE model into modules, variables, equations, and connections. |
| `docs/science/*.md` | Authored, paper-grounded module overviews (inlined into the pages). |
| `docs/images/`, `docs/stylesheets/` | Diagrams and styling. |

The generated pages (`docs/index.md`, `docs/architecture.md`, `docs/conventions.md`,
`docs/modules/`), `mkdocs.yml`, and the built site (`docs-site/`) are **not** tracked —
regenerate them as below.

### Generating the docs-site

```bash
# one-time setup
python3 -m venv .venv
.venv/bin/python -m pip install mkdocs-material

# regenerate the pages + nav from the model (run after any model change)
.venv/bin/python docs/gen_docs.py

# live preview at http://127.0.0.1:8000/
.venv/bin/python -m mkdocs serve

# or build the static site into docs-site/
.venv/bin/python -m mkdocs build
```

To extend a module's narrative, edit the matching `docs/science/<module>.md` partial and
re-run `docs/gen_docs.py`; hand edits to the generated pages are overwritten.

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
    <a href="https://github.com/BenjaminBlanz/WorldTransFRIDA-ILE">Interactive Learning Environment</a>
  </li>
</ul>
 
## Calibration Data

See the Documentation tab in the <a href="https://github.com/metno/WorldTransFRIDA/blob/main/Data/Calibration%20Data.csv">Calibration Data file</a>
 
## Standalone Climate Model

The standalone climate model based on the climate and land use components of FRIDA, <a href="https://github.com/chrisdwells/FRIDA-Clim">FRIDA-Clim</a>
 