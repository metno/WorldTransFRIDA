### Overview

The Resources module represents two material-and-emissions systems that sit at the interface between the human economy and the carbon cycle: carbon capture and storage / carbon dioxide removal (CCS/CDR), and the production and stock of concrete. Both are simulated endogenously, as stock-flow systems driven by investment, demand, cost dynamics, and policy, rather than prescribed as exogenous pathways. The module draws fossil-fuel and bioenergy emissions from the Emissions and Energy modules, takes policy levers from the Government Regulations module, and returns captured, stored, and emitted carbon flows that feed back into the carbon cycle and surface temperature.

### CCS and CDR technologies

The CCS sub-model represents three distinct capture pathways, disaggregated because their feedstocks, costs, and policy rationales differ:

- **End-of-pipe carbon capture (EOPC)** captures CO₂ at fossil-fuel combustion point sources (coal, oil, gas). Only the share of each fuel's emissions arising at accessible point sources is treated as capturable, reflecting that much oil use is in dispersed mobile sources while coal is concentrated in centralized power generation.
- **Bioenergy with carbon capture and storage (BECCS)** captures process and combustion emissions from biofuel production. Because the biomass first absorbed atmospheric CO₂ during growth, capturing and storing it yields net-negative emissions. BECCS is additionally constrained by the crop supply-to-demand balance in the Land Use and Agriculture module, so energy cropping cannot crowd out food.
- **Direct air carbon capture (DACC)** draws CO₂ directly from ambient air. It is not limited by concentrated emission streams; its desired flow is set as a fraction of the cumulative atmospheric CO₂ anomaly, making it a removal technology that targets excess atmospheric carbon rather than current emissions.

EOPC and BECCS capture is capped at the physically capturable emission flow, so the system never attributes more capture to a source than is emitted there.

### Capacity, investment, and cost dynamics

Each pathway's capture capacity is a stock that grows through an investment-driven installation flow and is depleted by depreciation over assumed infrastructure lifetimes. Investment is set in two stages. First, policy-set desired storage shares translate into a desired annual capture volume per pathway, which is converted into desired capacity additions by comparing required capacity to installed capacity and spreading the gap over a capacity-building time. Second, total investment across all three technologies is budget-constrained: the available budget is a policy-set share of real private investment, supplemented by baseline public R&D. When desired investment exceeds the budget, each pathway is scaled down proportionally, so resource constraints bind endogenously.

Installation cost per unit of capacity follows the same floor-plus-reducible form used for renewable energy. Two opposing endogenous effects modulate the reducible part: learning-by-doing lowers cost as cumulative capacity grows (with technology-specific learning rates), while a "stepping-on-toes" effect raises cost during rapid simultaneous expansion, capturing materials bottlenecks and duplicated effort.

DACC carries an explicit energy cost. Its energy requirement per tonne of CO₂ is multiplied by the marginal cost of clean energy drawn endogenously from the Energy module, so DACC's economics are tied to the pace of the broader energy transition. The total DACC budget therefore covers both capture equipment and the power infrastructure needed to run it, both counted against the CCS budget. This coupling can produce energy-price spikes that perversely prolong fossil use during large DACC build-outs.

### Storage and leakage

Captured CO₂ from all three pathways accumulates in a single stored-CO₂ stock representing geological storage. Storage is a finite global resource base, and storage cost rises through an exponential scarcity multiplier as cumulative injection depletes it. A leakage mechanism couples finance to physical integrity: when the cost of maintaining storage for the accumulated stock exceeds the available budget, the unaffordable fraction sets a leakage rate, and a corresponding flow returns stored carbon to the atmosphere. This represents the real-world risk of site monitoring and abandonment under financial constraint, a dynamic usually absent from integrated assessment treatments of CCS.

### Concrete and process emissions

The Concrete sub-model tracks the global in-use stock of concrete across four stocks: new and old residential-and-service buildings, and new and old infrastructure. Demand for buildings is built from desired useful floor area, a logarithmic function of GDP per person scaled by population and converted to concrete via a concrete-per-floor-area intensity. Infrastructure demand is a regression on population, GDP per capita, and their interaction. In each case, the gap between desired and installed stock drives a construction flow, smoothed over an adjustment time.

Concrete moves through a lifecycle: new structures age into the old stock at a cutpoint of half their average lifetime, old structures are eventually decommissioned, and both deteriorate continuously through wear. New construction and maintenance (replacing deteriorated material) together constitute total yearly concrete use.

Each tonne of concrete produced carries process and material CO₂ emissions, computed from construction-plus-maintenance throughput times a CO₂ intensity specific to building versus infrastructure mixes. These emissions feed the carbon cycle. The model represents the production-side emissions of cement and concrete; it does not credit any carbonation re-uptake as a CO₂ sink — carbonation appears only as a corrosion mechanism that, with chloride exposure, shortens concrete service life.

### Climate feedbacks and coupling

Both sub-models are two-way coupled to the climate:

- Rising surface temperature shortens concrete service life, accelerating aging, deterioration, and the replacement construction (and its emissions) needed to hold stocks. Extreme-weather storm damage, valued from coastal-asset damages in the Climate module, adds to deterioration of older structures.
- CCS capture and storage flows reduce net atmospheric CO₂ additions, while leakage returns carbon; DACC directly draws down atmospheric concentration. Concrete production adds CO₂. These flows close the loop to warming.
- Investment for CCS competes with other claims on private capital, so climate damages that reduce productive capacity can constrain the very mitigation they are meant to fund.

### Role in mitigation scenarios

CCS technologies act as policy levers whose effectiveness depends strongly on deployment timing, system interactions, and resource constraints. Early EOPC deployment cuts gross fossil emissions soonest and yields the strongest near-term climate response; BECCS is limited by land and biomass; and DACC achieves large stored volumes but its heavy energy demand offsets part of its climate benefit. No single option suffices, so deep decarbonization requires a diversified, early-action portfolio combining capture, removal, renewables, and firm low-carbon generation, with concrete demand and its process emissions modulated by building longevity and maintenance policies.
