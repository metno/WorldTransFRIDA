The Government Regulations module is where FRIDA's climate and economic policy levers live. It does not generate policy from first principles; instead it holds the exogenous, scenario-defined settings that a user chooses, and it converts those settings into signals that the rest of the model responds to endogenously. In FRIDA's design, the processes that *create* taxes and subsidies are out of scope, but their *effects* are fully represented. This means that with one exception, the module never overrides behavior. It changes the incentives, prices, and constraints that the human actors in the model face, and those actors then react through the same feedback structures that govern the baseline.

The module is the natural home for "what-if" policy experiments. A baseline run (the Endogenous Model Behavior scenario) introduces no additional policy, so it behaves like an SSP-style baseline. A mitigation scenario is built by switching on policy structures or changing the levers held here over time.

### Kinds of policy represented

The module exposes levers across several domains:

- **Energy and carbon pricing.** Energy taxes and subsidies, including a carbon tax, which raises the effective cost of carbon-intensive fuels relative to low-carbon alternatives.
- **Support for low-carbon energy and carbon management.** Subsidies and public research-and-development support that lower the relative cost of renewables, nuclear, and the carbon capture technologies (end-of-pipe capture, bioenergy with carbon capture, and direct air capture). For carbon management, the levers take the form of desired capture rates and storage shares, plus the maximum share of private investment that may flow to capture and storage.
- **Land-use policy.** Control over forestation, irrigation, and non-agricultural water use.
- **Fiscal and macroeconomic settings.** Government austerity behavior via a public debt-to-GDP threshold, central-bank inflation and unemployment targets, taxes on profits, wages, and wealth, and sea-level-rise adaptation spending.
- **Demand-side behavior.** Levers on food and energy demand and on diet shift. Explicit dietary and energy-demand overrides are the one place where the module directly substitutes for endogenous behavior rather than nudging it.

### How a carbon price or regulation propagates

A carbon price enters as an addition to the effective cost of fossil-derived energy. In the Energy module, investment in new capacity is allocated across coal, oil, gas, biofuel, hydropower, solar, wind, and nuclear in proportion to their relative marginal costs, with priority given to the least-cost sources. Shifting relative costs through a carbon tax or a subsidy therefore redirects investment toward low-carbon sources, and because the sources that attract more investment can supply more energy, market shares and the fuel mix change over time. Less fossil combustion means lower emissions feeding the Emissions sub-module, and hence a lower trajectory of greenhouse-gas concentrations, radiative forcing, and surface temperature.

The same price signal also propagates through the economy. Higher energy costs raise the average marginal net cost of energy, which feeds the Economy module and can show up as inflation; mitigation scenarios typically show an initial rise in the cost of energy that eases as low-carbon technologies mature through learning-by-doing. On the behavioral side, prices and incomes are inputs to the perceived accessibility of food and energy consumption, so fiscal levers also reshape demand.

Carbon-management policy works through a desired-capture pathway: the levers set desired storage shares and capture fractions, which the Resources/CCS structure turns into desired capacity additions and investment, subject to a budget cap and physical limits. The resulting captured carbon feeds back to the Emissions sub-module, reducing net additions to the atmosphere.

### Building scenarios and the link to fiscal/monetary policy

Scenarios are specified by setting these levers, often as values that ramp between target years (for example, rising capture or storage shares in 2030, 2050, and 2070). Low, medium, and high variants are commonly produced by scaling a central pathway up or down.

Crucially, policy is not free. Taxes and subsidies affect government budgets, so a subsidy must be offset by adjustments to spending elsewhere to avoid excessive debt. This couples the Government Regulations module directly to the fiscal and monetary machinery in the Economy module, where the government funds spending through taxes and borrowing and cuts expenditure once public debt-to-GDP exceeds its threshold, and where the central bank pursues its inflation and unemployment targets. In this way the policy levers set here are constrained and partly absorbed by the same stock-flow-consistent government and central-bank sectors that drive the rest of the economy.
