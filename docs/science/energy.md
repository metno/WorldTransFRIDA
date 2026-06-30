### Overview

The Energy module simulates global energy supply and demand, the transition from fossil fuels to renewable and nuclear sources, and the greenhouse-gas emissions that result. Unlike integrated assessment models that solve for a cost-optimal pathway, FRIDA's Energy module simulates the system's evolution from calibrated decision rules, market signals (prices and costs), and policy interventions (taxes, subsidies, regulations). Energy investment is therefore an emergent property of the system structure rather than the output of a forward-looking optimization, and the logic of the energy transition arises from interacting constraints and feedbacks. The module operates in continuous time at global scope, capturing the inertia of capital stocks, delays in investment decisions, and the physical constraints of resource extraction and capacity expansion.

The module's structure can be followed along two strands that meet at the supply–demand imbalance. The first follows the money: how total energy investment is determined, how it is allocated across technologies, and how each technology converts that capital into energy supply. The second is demand, built up from GDP per capita and adjusted by climate-driven heating and cooling. The imbalance between the two strands drives investment, closing the central loop.

### Energy demand

Total demand is the product of population and per-person energy demand. Following the International Energy Agency's sectoral structure, per-person demand is disaggregated across three sectors — **buildings** (residential and commercial/public services), **transport**, and **industry and other** — each evolving as a function of GDP. This split is an intermediate step toward a fuller demand-side representation: it does not resolve the full complexity of sectoral drivers, but it turns the module into a place to explore how macroeconomic trends and broad policy shifts move demand, and to test stylised scenarios such as efficiency improvements or structural economic change by adjusting the GDP–demand relationship of individual sectors.

- **Sectoral baselines.** Each sector uses a power-function regression on GDP, chosen to capture both the slow rise in energy consumption over the first decades and the continued long-term growth in demand through and beyond the end of the century.
- **Buildings and climate.** The buildings sector retains the model's representation of heating and cooling, keeping demand tied to the global surface temperature anomaly so this end use is accounted for where it matters most. Warming maps to cooling degree days (a linear function of the anomaly) and heating degree days (an exponential decay, capturing the nonlinear fall in space-heating needs as temperatures rise); these indices are converted to energy units using intensity coefficients.
- **Induced demand.** A perceived-cheapness effect adjusts demand with the relative change in the marginal net cost of energy: as energy becomes relatively cheaper, use is induced upward, and vice versa. The relevant price is a first-order smoothing of the average marginal net cost rather than an instantaneous value, representing price stickiness.
- **Transport dynamics.** Transport demand is computed endogenously through the same behavioral framework used for dietary choice, rather than from GDP alone, internalising the estimate and reducing reliance on predetermined scenarios. Sector-specific drivers act as promoters or deterrents: greater exposure to particulate emissions raises health risk and suppresses transport energy use — especially where the supply mix is fossil-heavy — while a cleaner mix with a higher renewable share tends to increase consumption. The same structure can be extended to the buildings and industry sectors.

### Energy supply

Supply is built from modular sub-models spanning fossil (coal, oil, gas), renewable (solar, wind, hydropower, biofuels), and nuclear technologies. Each links capital accumulation, endogenous technological change, and climate-driven infrastructure damage. Capacity expands through investment-driven build flows, depreciates over assumed lifetimes, and is reduced by capital damaged from rising surface temperature, so climate impacts propagate directly into infrastructure integrity.

### Energy investment

A single Energy Investment sub-model sets both the total volume of investment entering the system and its split across competing technologies, representing the aggregated behavior of global energy investors.

**Total volume.** The aggregate investment decision is driven by the relative mismatch between supply and demand, normalized by total supply, and is governed by a proportional–integral–derivative (PID) controller whose goal is to invest only what is needed to close the gap. The proportional term reacts to the current mismatch, the integral term to accumulated imbalance, and the derivative term anticipates future imbalances from the rate of change. The three weights are calibrated against observed supply and investment over 1980–2023, so investment responds to current disequilibrium, persistent small imbalances, and rapid shifts alike. Conceptually this mirrors control-theoretic behavior in which agents regulate a perceived system state rather than maximize an objective.

**Allocation across technologies.** Investment is allocated primarily on each technology's marginal cost of supplying an additional unit of output, computed endogenously within each supply sub-model from production costs, existing capital stocks, learning effects, and technology-specific characteristics. Because pure cost minimization does not reproduce observed diversification, a cost "spread" lets a portion of investment flow to higher-cost options. The spread orders opportunities cheapest-first and apportions capital by a calibrated "width": a width of zero gives fully cost-minimizing behavior, an infinite width spreads investment evenly, and intermediate values favor cheaper options without excluding others. Time-dependent, technology-specific cost adjustment factors capture the monetary equivalent of non-cost preferences and historical policy that are not otherwise represented.

**Policy levers.** Forward-looking taxes and subsidies can be applied to emissions from individual technologies, to whole technology classes, or to decommissioning rates of extraction capital; all act by modifying the effective marginal costs that drive allocation. The framework also supports structural constraints such as a fossil-fuel moratorium beginning in a chosen year, after which new fossil investment halts and capital is reallocated to remaining options.

### Renewable energy

Solar, wind, hydropower, and biofuels share a common stock-flow and endogenous cost-learning architecture, each with additional structure.

- **Solar and wind** use a multi-vintage conveyor for capital, so capacity is tracked by age cohort to represent aging, productivity, and eventual decommissioning. The reducible installation cost falls with cumulative construction along a power-law learning-by-doing curve. This reinforcing loop is tempered by a "stepping on toes" mechanism in which unit costs rise with the ratio of current to perceived cumulative construction, capturing duplicative effort and bottlenecks during rapid expansion. A floor cost for capacity rises with the solar-and-wind share of total output, representing the growing marginal costs of grid stabilization and storage at high penetration of variable renewables — a balancing feedback on growth. Generation equals accumulated capacity times technology-specific full-load hours. For wind, full-load hours are no longer held constant but respond endogenously to climate change, which mainly acts on the frequency distribution of wind speeds rather than on long-run averages: a rising mean wind speed pushes full-load hours up, while more frequent and longer-lasting low-wind episodes (calms) pull them down, so the net effect on annual wind generation is the balance of these two opposing climate signals.
- **Hydropower** is centered on a capacity stock with installation as inflow and two outflows: linear depreciation over an assumed lifetime and climate-driven capital damage. Output is capacity times an efficiency that is itself modulated by climate change (altered river discharge and evaporation). Installation costs follow a linear function that rises with installed capacity, representing the move from prime to marginal sites; the install rate equals investment divided by these capacity-dependent costs, slowing growth as good sites are used up.
- **Biofuels** evolve through the same learning and stepping-on-toes cost dynamics, but their production is constrained by the ratio of crop supply to demand, so energy-related crop demand cannot crowd out food. Crops required are derived from available production capital and crop energy density, linking energy to land use. Biofuel primary energy is converted to secondary energy using oil-conversion capacity, integrating it into the liquid-fuel supply chain as a drop-in substitute.

### Fossil energy

Coal, oil, and gas share an identical structure parameterized per fuel, each split into primary extraction and secondary conversion.

- **Extraction.** Extraction capital evolves through gross investment, depreciation, and an explicit decommissioning flow that reflects regulatory constraints or climate damage. Extraction is governed by two opposing forces: resource depletion raises marginal costs as cumulative extraction grows and lower-quality reserves are accessed, while continued extraction drives learning-by-doing that lowers costs. The interaction of geological limits and technological progress determines how fossil competitiveness evolves and whether scarcity accelerates or delays the transition.
- **Conversion.** Extracted fuel feeds secondary conversion, represented by a constant-elasticity-of-substitution (CES) production function with fuel input and conversion capital as factors, plus a time-varying total factor productivity term reproducing historical gains in fuel-to-energy efficiency. Conversion capital has no explicit decommissioning term because emissions track extracted (burned) fuel rather than conversion efficiency — though efficiency still changes how much extraction, and thus burning, is needed for a given output.

Abrupt cuts in fossil production, for example from policy shocks, can strand assets in the secondary fossil sectors, so transition risks feed back into investment choices and into loan defaults in FRIDA's economy module.

### Nuclear energy

Nuclear capacity grows through installation and is depleted by physical depreciation and climate-driven capital damage (the latter a catchall with wide uncertainty, including near-zero damage). Output is capacity times efficiency, where efficiency is reduced by warming via the share of thermal plants cooled by rivers: as cooling-water temperatures rise, the thermal cycle's efficiency degrades nonlinearly. Installation costs use the same floor-plus-reducible structure as solar and wind, with learning-by-doing, stepping-on-toes, and optional taxes or subsidies.

### Efficiency reduction in power plants and climate damages

Climate feedbacks enter supply in two ways. First, capacity stocks across all technologies lose capital to climate-driven damage tied to the surface temperature anomaly, shortening effective asset life. Second, the efficiency of thermal plants (fossil and nuclear) and of hydropower declines with warming — thermal through cooling-water constraints, hydropower through changed discharge and evaporation. The energy supply sector is therefore both a driver of climate change and constrained by it.

### Coupling, prices, and emissions

The module exchanges flows with the rest of FRIDA:

- **Emissions.** Combustion of coal, oil, gas, and biofuels produces emissions tracked for four species (CO₂, CH₄, N₂O, SO₂), which feed the climate module and drive warming.
- **Economy.** Energy investments form part of gross investment in the economy module; the supply–demand imbalance and the marginal net cost of energy feed inflation; fossil-asset stranding affects defaults; and taxes and subsidies move the government budget.
- **Drivers in.** Economic development, population, and climatic conditions set baseline demand, while climate conditions also reduce thermal and hydro plant efficiency.

### Energy units

Demand, supply, and capacity are tracked in consistent physical energy units across carriers, with climatic heating and cooling indices converted into the same units via intensity coefficients so that all sources, sinks, and the supply–demand imbalance are directly comparable. Where physical relationships are not fully known, parameters carry calibrated uncertainty ranges constrained by comparison to historical observations, enabling large ensemble runs that reveal the range of plausible century-scale outcomes.
