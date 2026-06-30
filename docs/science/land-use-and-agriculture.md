The Land Use & Agriculture module is FRIDA's representation of the terrestrial biosphere: how human demand for food, feed, fibre and energy is translated into land use and production, and how the resulting flows of carbon, water and nutrients feed back to the climate, the carbon cycle, and indicators of biodiversity. It follows the structure of dynamic global vegetation models such as LPJmL, but rebuilt as a simplified, fully endogenous, global system-dynamics model with no spatial disaggregation. Carbon enters the land through plant growth, is partly harvested for human use, and the remainder cycles through litter and soil before returning to the atmosphere. Around this carbon-and-water backbone sit nine coupled sub-models, spanning demand (Food Demand, Animal Products), allocation (Land Use), the three production systems (Crop, Grass, Forest), the supporting cycles (Land Nutrients, Freshwater, Soil carbon), and the diagnostic Biosphere Indicators.

### From demand to land

Demand originates outside the biosphere. **Food Demand** scales with population and per-capita income from the Demographics and Economy modules and with diet preferences from the Behavioral Change module, splitting into demand for vegetal calories and for animal products. **Animal Products** converts the animal-product demand into requirements for feed (grown as crops) and for grazing (supplied by grassland), and is the dominant source of agricultural non-CO2 emissions: ruminant digestion and manure produce methane and nitrous oxide.

These demands drive production through two levers: **productivity** (yield per area) and **land area**. When supply plus reserves falls short of demand, pressure builds to expand the relevant land system, while intensification raises yields on existing land. Diet therefore propagates strongly through the module — less meat lowers feed-crop demand, intensification pressure, and the associated nutrient and methane flows.

### Land allocation and land-use change

The **Land Use** sub-model allocates global habitable land among five stocks — cropland, grassland, young forest, mature forest, and a small degraded-land stock — treated as a compartment model with dynamic transition rates. The young/mature forest split captures the long delay (decades) between planting and a forest reaching its mature carbon density.

Land-use change (LUC) moves area between these stocks in several directions at once:

- **Cropland** expands by clearing mature forest and grassland when crop supply lags demand, and is depleted by fallowing to grassland, reforestation, degradation under intensified cropping, and any exogenous government forestation.
- **Grassland** expands to maintain its grazing/non-grazing ratio as animal-product demand grows, and is depleted by conversion to cropland, degradation, and (re)forestation.
- **Degraded land** accumulates degraded cropland and grassland and is only recovered through forestation policy.
- **Forest** receives all reforestation and matures from young to mature stock with a long calibrated delay; mature forest is cut for timber, which returns area to young forest. Total forest is capped at its roughly-1750 extent.

Because production is the product of productivity and area, LUC is the second route to meeting demand; under endogenous behavior, rising food and animal-product demand expands cropland and grassland at the expense of forest over the century, generating large land-use-change emissions.

### Crop yields and climate impacts

Plant growth in all three systems is built on a generalised multi-linear regression for net primary productivity (NPP), originally fit to gridded crop-model output. Baseline NPP is scaled by the global temperature anomaly and atmospheric CO2: a positive linear CO2-fertilisation term, a positive linear temperature term, and a negative quadratic temperature term that reproduces the non-linear heat-damage seen in temperature-response curves. For cropland, three additional terms add the effects of soil carbon, irrigation, and fertilisation, so intensification raises crop NPP. On **Crop** and **Grass** land carbon turns over annually; on **Forest** it accumulates as aboveground biomass, with young forest allocating more NPP to growth and mature-forest growth tapering toward a temperature-dependent stable density.

The single aggregated crop yield is the harvested fraction of crop NPP, set by a **harvest index** that depends on end use (lowest for food, higher for feed, highest for whole-plant energy crops) and that rises with productivity to mimic improved crop breeds. The climate impact on yield is calibrated from multi-model crop simulations under systematically perturbed temperature, CO2, water and nitrogen: yield change is linear in CO2 concentration with first- and second-order temperature effects, so warming and CO2 fertilisation pull in opposite directions. The same response also scales bioenergy-crop output. Residues not harvested become litter; high biomass use therefore leaves less litter to build soil carbon.

### Nutrients and freshwater

**Land Nutrients** represents fertilisation — the dominant intensification channel alongside irrigation. Total nitrogen and phosphorus application combines synthetic fertiliser with manure recycled from animal husbandry; manure substitution and ruminant numbers tie nutrient flows back to diet. Fertilisation raises crop NPP but the surplus drives the nitrogen and phosphorus loads used as biogeochemical-flow indicators.

**Freshwater** is a global bookkeeping stock of available water supply, recharged naturally and by technological discovery (deeper wells, reservoirs) and drawn down by withdrawals. Non-agricultural withdrawal scales with population and income; agricultural withdrawal is the irrigated cropland area times a per-area rate that falls with improving irrigation efficiency and rises with warming-driven evapotranspiration. A small unsustainable fraction draws on groundwater, whose decline contributes to sea-level rise and couples to the Climate module; irrigation also returns water vapour and surface-albedo changes as climate forcings.

### Soil carbon

Litter from each land system decomposes into soil organic carbon (SOC), emitting some carbon directly as CO2. Each of cropland, grassland and forest carries its own fast- and slow-decomposing SOC pools with different mean residence times; decay accelerates with temperature, so warming releases stored soil carbon — a positive feedback to the carbon cycle. Because emissions are proportional to stock size and stocks integrate litter input, an unchanging land system tends toward equilibrium. LUC breaks that equilibrium: shifting SOC between systems and reducing carbon input (e.g. forest to cropland) makes the land a CO2 source, while afforestation makes it a sink.

### Biosphere Indicators

The **Biosphere Indicators** sub-model quantifies five of the nine planetary boundaries from these processes, each via a control variable:

- **Land-system change** — deforested area as a fraction of estimated Holocene forest cover (the difference between that baseline and current young-plus-mature forest).
- **Biosphere integrity** — human appropriation of NPP (HANPP) as the functional-integrity proxy; the higher the share of biomass used, the greater HANPP and the implied biodiversity loss.
- **Freshwater use** — consumptive water use, taken as a roughly constant fraction of total withdrawal.
- **Biogeochemical flows** — nitrogen and phosphorus loads from fertiliser and manure.
- **Climate change** — CO2 concentration and radiative forcing from the Climate module.

Together these indicators let FRIDA approximate biodiversity trends from its three main pressures — land-use change, direct exploitation, and climate change — even without spatial or taxonomic detail, and they close the module's loop back to the Climate module through land-use, soil, and agricultural greenhouse-gas emissions, surface albedo, and irrigation water vapour.
