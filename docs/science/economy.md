### Overview

The Economy module represents the global economy as a **Schumpeterian, stock-flow-consistent (SFC) system operating in disequilibrium**. Rather than reducing the economy to an aggregate production function with an exogenous damage function, it builds output, employment, prices, and finance from the interaction of disaggregated institutional sectors — households (split into workers and owners), firms, banks, the central bank, and government. All internal processes are simulated in nominal (monetary) terms; real quantities are recovered by deflating with an endogenous price level. The module both stands alone as a macroeconomic model of growth under environmental constraints and couples tightly to FRIDA's Climate, Demographics, Energy, and Land Use modules.

Three design commitments shape everything below:

- **Stock-flow consistency.** Every flow of money leaves one account and enters another; nothing appears or disappears unaccounted for. Deposits, loans, savings, equity, and public debt are tracked as explicit stocks, and the difference between matching stocks (for example, bank loans minus deposits) defines residual balances such as bank equity.
- **Disequilibrium.** There is no market-clearing assumption. Income circulates, adjusts with lags, and overshoots; behavior is governed by adjustment rules and gradually shifting targets rather than by instantaneous optimisation. This lets short-run mechanisms (financial fragility) and long-run mechanisms (innovation) interact and produce endogenous business cycles.
- **Endogenous growth.** Growth in scale and growth in productivity both arise from inside the model — from credit creation, deficit spending, and innovation — not from an imposed trend.

The module does not optimise a welfare function. Policy levers (tax rates, central-bank reactivity, transfer shares) are inputs, and outcomes emerge from the feedback structure rather than from an assumed social planner.

### Circular flow of income

The Circular Flow sub-model is the accounting backbone. Households are split by income source: **labour income** accumulates in worker savings, while **ownership income** (profits, rent, bank profits) accumulates in owner savings. Both are conceptualised as deposit accounts in the aggregate banking system. A share of each group's income is consumed and the rest saved, but the consumption decision is driven by the gap between current savings and a **dynamic savings goal** that adjusts with a lag as income changes. Workers spend a larger share immediately; owners save more. Inflation raises nominal consumption as households try to preserve their standard of living.

Consumption flows into firms' checking accounts. From there firms pay **wages, rent, and profits** back to households, and these flows are taxed to fund government. On its own this loop would settle into a stationary equilibrium — savings goals met, no growth. Growth therefore enters from two injections: **private investment** financed by bank lending, and **government deficit spending**. Whether an injection raises real output or only the price level depends on available slack and productivity growth.

### Finance, debt, and the cost of credit

Finance is modelled as a single aggregate intermediary that creates money endogenously: extending a loan simultaneously creates a bank asset (the loan) and a deposit liability (new money in firms' accounts). Banks aim to grow their balance sheet toward a reference growth rate, tempered by an **equity target** and by **lending standards** — an index of screening strictness that tightens as defaults rise and loosens as they fall.

New loans are classified at origination as performing or non-performing (a *failure rate* governs the split), or as **exploratory** (innovation finance). Performing loans mature into safe loans and shed their risk premium; non-performing loans eventually default. Loans can also fail through several channels: interest-rate hikes (affecting all classes), sea-level-rise damages, R&D-driven obsolescence of existing assets, and GDP deceleration (for exploratory loans). The failure rate itself rises with looser lending standards, with investment growing faster than GDP, and with rising surface temperature anomaly. When the bank asset-to-liability ratio falls below a threshold, the government bails out the sector by issuing debt.

### Innovation and productivity

Following the Schumpeterian view, productivity growth is endogenous and disruptive. It has two sources:

- **Exploratory lending** to new entrants, which expands when credit growth outpaces real output and contracts when bank profit growth slows.
- **Incumbent R&D**, represented as firms reallocating existing (safe) assets toward exploratory uses. Firms' innovation orientation rises sharply when cash-reserve growth slows and declines gradually when reserves grow.

Both feed potential productivity growth (weighting exploratory investment more heavily), which materialises after a diffusion delay. The same process embodies **creative destruction**: R&D renders a share of existing assets obsolete, causing safe loans to fail and displacing workers even as economy-wide productivity rises. Realised labour productivity is further reduced by climate: rising temperature lowers productivity according to each worker's heat exposure, with sectoral shares (agriculture, industry, services) — themselves a function of GDP — determining the economy-wide effect.

### Employment, wages, and inflation

The Employment sub-model partitions the working-age population into non-active, unemployed, and employed. Labour demand (desired hires) is proportional to total public and private investment divided by the wage rate. Wages respond **asymmetrically** to the supply/demand balance — rising readily when labour is scarce, falling only sluggishly when it is slack — and rise when inflation outpaces nominal wage growth. Firing arises from loan defaults, from missed profits falling below an interest-linked threshold, and from productivity-driven displacement.

Inflation combines two forces: **demand-pull**, when private income plus government deficit spending grows faster than the economy's expansion potential (productivity plus employment growth); and **cost-push input shocks** transmitted from the Energy and Land Use modules (food supply-demand imbalances, fertiliser and land-use scarcity, marginal energy cost). Inflationary pressures outweigh deflationary ones, reflecting price stickiness. GDP is computed by the nominal expenditure approach (consumption plus investment, public and private; trade nets out globally) and deflated to real terms by the price index.

### Government and central bank

The Government sub-model collects taxes on wages, profits, and rent and recycles them as public investment, consumption, and transfers. Total spending is governed by the **debt-to-GDP ratio**: below one, spending exceeds revenue; as the ratio climbs above one, spending contracts toward a floor. Deficits are financed by issuing debt to the banking sector, and bank bailouts add a second debt-creating channel. Transfers (child support, pensions, unemployment welfare) are **countercyclical** and demographically driven — they grow with unemployment and with ageing — and are indexed to wages.

The Central Bank sets the policy rate with a Taylor-style rule targeting roughly 2% inflation and 5% unemployment, weighting inflation more heavily and adjusting gradually. The private safe rate is a moving average of the policy rate; the risky rate adds a **risk premium** that tracks the perceived default rate. The government debt rate is likewise a smoothed policy rate plus a premium that switches on only when debt-to-GDP exceeds one. This risk-premium channel is a key route by which climate stress (higher defaults) raises the cost of finance even when the safe rate falls.

### Private insurance

Insurance enters as part of the ownership side of the circular flow and the finance sector's risk pricing rather than as a separate optimising agent: climate-driven losses raise loan failure and the perceived default rate, widening risk premia and tightening credit, so that the cost of bearing physical risk is transmitted through asset balances and the price of investment finance.

### Sea-level-rise impacts and adaptation

A dedicated coastal sub-model tracks **coastal assets** and **coastal population** as stocks that grow with coastal GDP and population but are eroded by sea-level rise. A single aggregated **flood-protection height** is the form of adaptation; investment in raising it is derived from the protection needed to offset expected sea-level rise over the next 50 years, scaled by political will and capped at a fraction of coastal GDP. Assets and people are lost through storm-surge damage, **planned retreat** (anticipating future exposure), and **forced retreat** (inundation). Adaptation costs comprise protection construction, maintenance, and land-opportunity cost; storm-surge damage; relocation and demolition; and flooding (lost immobile assets and land). A behavioral feedback reduces asset growth where future flood exposure is expected, which can produce a peak-and-decline in surge damages as exposed assets are not replaced.

These coastal outcomes feed back into the Economy module through six channels:

- Storm-surge damage and assets lost to retreat or inundation **cause safe-loan failures** in Finance, tightening lending standards and triggering layoffs.
- Storm-surge fatalities raise the global death rate (via Demographics).
- People affected by storm surges suffer a temporary **productivity reduction**.
- Relocation costs are added to **owner consumption** in the circular flow.
- Net flood-protection spending is treated as **government expenditure** that adds to GDP without being productive investment.
- Coastal exposure raises **perceived climate risk**, shifting food demand in the Land Use module.

### Calibration and uncertainty

The module contains hundreds of equations with several dozen state variables and is calibrated against 1980–2023 data for GDP, investment, consumption, government expenditure, the debt-to-GDP ratio, inflation, unemployment, and wages, drawn from international statistical sources. Calibration minimises squared error across a set of payoff elements using a derivative-free optimiser; parameters lacking empirical bounds are given wide ranges. Because the model's single endogenous business-cycle mechanism must absorb historical variance that real economies generate from many exogenous shocks (pandemics, wars), the calibrated cycles are illustrative of one structural mechanism rather than reproductions of specific historical events. Accordingly, uncertainty is foregrounded: a large Sobol-sequence ensemble samples the parameter space, and results are reported as median trajectories with confidence intervals rather than point forecasts. The ensemble reveals robust qualitative patterns — nominal aggregates keep rising, real growth slows late in the horizon as climate impacts raise loan failures, ageing swells transfer burdens, and rising public debt tightens fiscal space — that emerge endogenously from the feedback structure rather than from imposed assumptions.
