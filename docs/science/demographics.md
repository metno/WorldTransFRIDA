The Demographics module represents how the global human population changes over time. Population is the starting point of FRIDA's human system: it is a primary driver of demand for goods and services, and therefore an upstream driver of the economic activity, food and energy use, and emissions that ultimately shape the climate. The module itself produces no direct emissions; its influence on the climate is entirely mediated through the other human modules. In the other direction, the climate feeds back onto demographics by adding temperature-driven mortality on top of the baseline death rates.

### Age-cohort population structure

Population is modelled as a continuous ageing chain rather than a single aggregate stock. People are tracked as they age through a sequence of cohorts, with each cohort subject to its own mortality. Conceptually this behaves like a pipeline: individuals enter as newborns, flow forward through successive age groups as they grow older, and leave the chain through death at any stage or by ageing out of the oldest group.

The continuous cohorts are organised into seven age categories chosen to capture the age structure that matters most for mortality and for the labour force:

- Infants
- Aged 1–20
- Aged 20–40
- Aged 40–60
- Aged 60–65
- Aged 65–75
- Aged over 75

These brackets allow age-specific death rates to be applied, and they provide the resolution needed to apply climate-driven mortality more strongly to the older, more vulnerable groups. The cohort structure is initialised from observed global population-by-age data for the model's start year, so that the simulated age distribution begins from a realistic baseline and then evolves endogenously.

### Births and fertility

New entrants to the population arrive through births, which are governed by an endogenous fertility rate rather than an imposed trajectory. The fertility rate is computed from a calibrated relationship driven by two development indicators:

- **GDP per person** — a proxy for material standard of living.
- **Female literacy / educational achievement** — a proxy for women's education and autonomy.

The relationship reflects the well-established demographic-transition pattern: as incomes rise and female education improves, fertility falls, with birth rates declining in an approximately exponential fashion as living standards increase. Because both drivers are produced elsewhere in FRIDA (GDP per person in the Economy module, with education tied to development), fertility responds dynamically to the simulated path of development rather than being fixed in advance. Multiplying the fertility rate by the relevant population gives the birth flow that feeds the youngest cohort.

### Mortality and net population change

Each age cohort carries its own mortality rate, so deaths are concentrated where they realistically occur — highest among infants and the oldest groups, lowest in the middle-aged working cohorts. These baseline rates are not static: they evolve over time to capture secular improvements in survival as health, nutrition, and living conditions improve.

Net population change at any moment is the balance of three processes:

- **Births** adding to the youngest cohort,
- **Ageing** moving people forward from one cohort to the next, and
- **Deaths** removing people from every cohort.

The total population is simply the sum across all cohorts, and its trajectory emerges from the interaction of these flows rather than being prescribed.

### Temperature-driven mortality

On top of baseline mortality, FRIDA adds a climate impact channel for temperature-related deaths, capturing the fact that both extreme heat and extreme cold raise mortality. The effect is driven by the global mean surface temperature anomaly relative to pre-industrial levels and is split into two components:

- A **heat** effect, which increases deaths as warming proceeds.
- A **cold** effect, which is reduced by warming (fewer cold-related deaths).

Each component is represented as a smooth function of the temperature anomaly, and because the underlying relationships were built from daily temperature–mortality data, short-term events such as heatwaves are implicitly captured rather than only long-term means. On balance, rising temperatures increase net heat-related deaths faster than they reduce cold-related deaths, so the overall effect of warming is added mortality.

These temperature impacts are age-stratified. The association between temperature extremes and death is much stronger for older people, so the heat and cold effects are scaled up for the oldest age bands relative to younger groups, with cold sensitivity rising especially steeply with age. The resulting additional deaths are added to the death rates of the individual cohorts, so climate change directly reshapes the population's size and age structure. A further, smaller source of climate-driven death — fatalities from sea-level-rise-driven coastal storm surges — is also added into the cohort death rates.

### Coupling to the rest of FRIDA

Population links the Demographics module outward to every other part of the human system:

- **Labour and the economy** — the working-age cohorts supply labour to the Economy module, where, together with capital and productivity, they set the economy's production capacity. A larger or younger workforce expands potential output; an ageing or shrinking population constrains it.
- **Food and energy demand** — population, alongside GDP per person, scales the demand for food, feed, and other land-based products in the Land Use and Agriculture module and the demand for energy in the Energy module.
- **Emissions and the climate** — by driving these demands, population indirectly drives the resource use, land-use change, and energy production responsible for the bulk of anthropogenic emissions, closing the loop back to the Climate module.

Because GDP per person both shapes fertility and is itself shaped by the labour the population supplies, demographics sits inside a feedback loop with the economy: development lowers birth rates, while population growth and ageing in turn influence economic output and therefore the very development that drives fertility.
