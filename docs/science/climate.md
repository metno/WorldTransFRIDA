The Climate module is FRIDA's representation of the physical Earth system. It closes the central feedback loop of the model: the social and economic modules generate climate drivers (emissions, irrigation water, land-use change), the Climate module converts these into radiative forcing and a temperature response, and the resulting temperature and sea-level changes flow back out as impact drivers that reshape the human system. The same physics can also be run as a standalone simple climate model, in which case all drivers are supplied exogenously rather than computed within FRIDA.

The module is deliberately a "minimal required climate": it simulates only the components needed to reproduce historical and plausible future global climate dynamics, prioritising legibility, fast runtime, and feedbacks over process detail. Its radiative-forcing and temperature core follows the structure of the FaIR simple climate model, but it adds a full process-based carbon cycle across atmosphere, ocean, and land, a reduced set of forcing species so that each can be simulated endogenously, a dynamic sea-level model, and a complete recalibration.

### The causal chain

The module is organised as a left-to-right chain:

- **Emissions and drivers** are aggregated into total global fluxes per species.
- **Atmospheric concentrations** are computed for each tracked gas.
- **Effective radiative forcing (ERF)** is derived from those concentrations and from other drivers.
- **The energy balance model** turns total forcing into a temperature change, taking up heat into the ocean.
- **Temperature** then feeds back onto the carbon cycle, the forcings, and the sea-level model.

### Emissions and climate drivers

Within the coupled model, seven anthropogenic drivers arrive from the other FRIDA modules: emissions of CO2, CH4, SO2, N2O, and HFCs (expressed as a single HFC134a-equivalent species), plus water vapour from irrigation and the change in surface albedo from land use. Only solar, volcanic, and Montreal Protocol gas forcings (and the Montreal gases' effect on stratospheric ozone) are imposed exogenously, since they are independent of the social system. A few minor forcers whose process-level drivers are not resolved at FRIDA's sectoral detail (NOx, VOCs, CO emissions, and black-carbon deposition on snow) are "infilled" using simple linear regressions on the species that are tracked.

### Effective radiative forcing

Twelve ERF categories are summed to drive the energy balance. CO2 forcing uses a combined logarithmic and square-root function of concentration; CH4 and N2O use square-root parameterisations; HFC and the minor gases scale with concentration. Aerosol forcing is split into aerosol–radiation (linear in SO2 emissions) and aerosol–cloud (logarithmic) terms, with SO2 acting as a calibrated proxy for all aerosol contributors so the present-day total matches the best-estimate value. Ozone forcing responds to CH4, N2O, and Montreal gases plus the infilled reactive species, and weakens with warming as a warmer atmosphere produces more of the OH radical that destroys tropospheric ozone. Two land-use forcings are computed process-based rather than from cumulative emissions: an albedo forcing from the area-weighted mix of cropland, grassland, and forest, and a net forcing from irrigation water vapour (positive as a greenhouse gas, but with a larger negative low-cloud effect). Further terms cover stratospheric water vapour from CH4 oxidation, black carbon on snow, the natural volcanic forcing (offset to zero over the historical mean and scaled by an efficacy factor), and the time-varying solar forcing.

### Energy balance model

Total ERF drives a three-layer energy balance model. The first layer represents the surface and ocean mixed layer and is calibrated against observed global mean surface temperature; the lower two layers represent the intermediate and deep ocean. Heat is exchanged between adjacent layers according to their heat capacities and transfer coefficients, with a deep-ocean uptake efficacy factor tuning the transient response. This formulation produces both the surface temperature anomaly and the ocean heat uptake that feeds the sea-level model.

### Ocean carbon cycle

The ocean is a four-box model: warm (low-latitude) and cold (high-latitude) surface boxes, an intermediate layer, and a deep box sized to a fixed total ocean volume. Carbon is redistributed by mixing, overturning circulation, and a biological pump that exports organic carbon downward from the surface. The two surface boxes exchange CO2 with the atmosphere according to the difference between atmospheric and oceanic partial pressures, which requires solving seawater carbonate chemistry; FRIDA's small timestep lets this solver converge in a single iteration. Surface temperature, salinity, and alkalinity scale linearly with the global temperature anomaly, so warming modulates ocean uptake.

### Land carbon cycle and terrestrial carbon balance

Land is divided into cropland, grassland, young and mature forest, and a small degraded stock. Net primary productivity per area depends on temperature and CO2 (CO2 fertilisation), with cropland production additionally driven by human inputs in the coupled model. Forest aboveground biomass scales with temperature through a quadratic relationship capturing both growth gains and idealised loss processes. Plant litter feeds soil carbon held in fast- and slow-decomposing pools whose decay accelerates with temperature; clearing forest releases its biomass. Land-use transitions move land and soil carbon between types, with committed soil-carbon changes released through a decaying legacy flux. Summed over all processes (plus a small constant peatland sink), these give the terrestrial carbon balance, which is split diagnostically into a natural "land carbon sink" and human-driven "food and land-use" emissions.

### Atmospheric concentrations

Atmospheric CO2 is the running balance of anthropogenic emissions, the land flux, and the air–sea flux. CH4 and N2O are tracked as single atmospheric boxes that accumulate emissions and decay with variable lifetimes; CH4's lifetime shortens with warming and with other reactive species, while N2O's depends on cumulative emissions. HFC134a-eq decays with a fixed lifetime.

### Sea level rise

Global mean sea-level rise is the sum of five contributions, with no feedback back onto the climate. Thermal expansion is linear in ocean heat content from the energy balance model. Mountain glaciers and the Greenland and Antarctic ice sheets are functions of the global temperature, the ice sheets resolving both surface mass balance and solid-ice discharge with optional high-impact thresholds. Land water storage is driven by population, or in the coupled model directly from modelled groundwater withdrawal and hydropower. Sea level continues to rise even when temperature stabilises or declines, making it a distinct impact driver.

### Calibration, units, and uncertainty

Both the standalone and coupled forms are calibrated against observations. A pre-industrial spinup equilibrates the land and ocean carbon stocks; a large prior ensemble varying carbon-cycle, forcing, and energy-balance parameters is then filtered against historical temperature, air–sea CO2 flux, and NPP, and constrained so that equilibrium climate sensitivity, transient climate response, aerosol forcing, ocean heat content, CO2 concentration, and the present-day temperature anomaly match observed and assessed ranges. The result is a posterior set of parameter combinations that propagate uncertainty through every output, so temperature, sea level, and carbon fluxes are reported as median values with percentile ranges. Climate quantities use standard physical units (temperature anomalies in kelvin relative to a 1750 or 1850–1900 baseline, concentrations in ppm or ppb, forcings in W m⁻², carbon stocks and fluxes in GtC), and a surface-temperature offset is carried so anomalies can be expressed against the policy-relevant pre-industrial reference.
