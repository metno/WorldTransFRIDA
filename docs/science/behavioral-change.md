### Overview

The Behavioral Change module gives FRIDA a fully endogenous, process-based
account of how people's consumption choices evolve as the human and climate
systems co-evolve. Rather than imposing demand-side change through external
narratives or fixed scenarios, it represents the internal social dynamics that
drive it: accumulating climate experience and knowledge reshape risk perception,
perception and social context reshape what people consider normal and desirable,
and changed intentions translate only gradually into changed behavior because of
habit, social diffusion, and the stickiness of culture. Demand and supply are
placed on an equal footing, so consumption both responds to and feeds back on
production, land use, and emissions.

The module is developed in greatest depth for **dietary behavior**, spanning the
sub-models for **Climate Risk Perception**, **Animal Products Demand**, and
**Total Food Demand**. The same feedback architecture is reused for two further
high-impact behaviors — **Transportation Energy Demand** and **Fertilizer
Demand** — and a dedicated **Behavior Change Policy** sub-model exposes levers
that shift any of these dynamics. Model output is reported as ensembles with
median and confidence ranges rather than single deterministic runs.

### How endogenous behavioral change is represented

Behavior is modelled as the outcome of three motivational processes, bounded by
two constraints:

- **Perceived accessibility** — affordability and availability, captured through
  income and scarcity rather than explicit prices.
- **Descriptive norm** — what others are perceived to be doing, including the
  *direction* in which that norm is trending.
- **Personal norms** — the standards people hold for themselves, shaped by
  social-cultural value, perceived health/consumption risk, and perceived
  climate-change risk.
- **Past behavior (habit)** and **accessibility** act as constraints: people
  cannot easily break habitual patterns, and they cannot act beyond what is
  affordable, available, or actually supplied.

These motivations are combined as a **weighted average**, reflecting that
different individuals and situations weight accessibility, social conformity, and
moral conviction differently. Crucially, the weights themselves are dynamic: as
income rises past a reference level, accessibility loses salience (modelled with
a logistic function) and weight shifts toward norms — a process-based explanation
for why demand growth slows at high income without needing an arbitrary cap.

### The stock-flow structure of gradual adoption

Gradual adoption is the central structural idea, implemented throughout with
**stocks that adjust toward an indicated target over a characteristic delay
time** (exponential smoothing). Desired demand is itself such a stock: its
indicated value is set by the weighted motivations, but it adjusts only slowly,
so a longer adjustment time represents stronger habitual inertia. Perceptions are
smoothed the same way — income, current consumption, risk, and climate signals
are all perceived with lags so that transient fluctuations do not immediately
rewrite behavior.

Two features give the dynamics their richness:

- **Reference dependence.** Many perceptions are judged not in absolute terms but
  relative to a slowly updating reference ("normal") condition, also modelled as
  a smooth of the perceived value over a longer horizon. As conditions persist,
  the reference catches up and the same absolute level feels less abnormal —
  capturing acclimatization and desensitization.
- **Diminishing response.** Where a perception drives behavior, it does so
  through a power function with an exponent typically below one, so response
  grows less than proportionally with magnitude (psychophysical numbing).

Actual demand is the smaller of desired demand and accessible demand, and actual
consumption is further capped by available supply, ensuring behavior stays
bounded by agency and by what the system can deliver.

### Dietary change and its links to land, agriculture, and emissions

Dietary behavior is decomposed into two endogenous dimensions:

- **Total Food Demand** sets overall desired caloric intake (the "diet").
- **Animal Products Demand** sets the share of that diet met by animal products
  (the "diet composition"); vegetal demand is the remainder.

The model does not segment the population into fixed categories such as
meat-eaters versus vegetarians; it tracks the evolving average per-capita intake
and composition, so dietary change can go in either direction depending on the
balance of feedbacks. For animal products, accessibility responds to *relative*
scarcity — the supply–demand balance of animal products versus all crops — used
as a proxy for relative price, so animal products become more desirable when they
are relatively less scarce. Total food demand, having no substitute, responds to
overall food scarcity, and a minimum caloric floor prevents modelled
malnourishment.

Per-capita demand, scaled by population, drives total demand and therefore
production in the Land Use and Agriculture module; production feeds back through
supply–demand balances into accessibility and norms, closing a two-way loop. From
there the dietary signal propagates into the climate system: animal production
drives CH₄ and N₂O emissions and grazing land use, while crop production — which
also serves animal feed and bioenergy — drives cropland change and N₂O from
fertilizer. Reduced or substituted demand therefore lowers emissions, cooling the
baseline climate, which in turn feeds back into risk perception.

### Climate risk perception as the human–climate link

Perceived climate-change risk is the key channel by which the climate system
reaches back into behavior. It is the product of an **experiential effect** and
a **cognitive effect**:

- The experiential effect accumulates perceived exposure to record-breaking
  extreme weather and to sea-level-rise flooding, each normalized to its own
  updating reference of "normal" exposure.
- The cognitive effect uses the perceived surface-temperature anomaly (smoothed
  over a long horizon to represent slow knowledge diffusion) as a proxy for
  climate knowledge, again judged against an updating reference.

Because the two combine multiplicatively, knowledge amplifies the felt risk of
events. Critically, the updating references mean perceived risk can *peak and
then decline* even as physical conditions worsen — the system desensitizes. This
makes climate-motivated dietary change a balancing loop that can weaken over
time, allowing reinforcing social-value and norm loops to reassert themselves and
producing the possibility of a reversal of sustainable change late in a run.

### Transportation energy demand and fertilizer demand

Transportation Energy Demand and Fertilizer Demand reuse the same behavioral
architecture, applying it to energy use per person and to nitrogen fertilizer
use. Each carries its own stock of desired demand that adjusts gradually toward a
target set by accessibility, descriptive norm, and personal norms, with personal
norms again shaped by perceived social value, consumption risk, and climate risk,
and with final demand taken as the smaller of the personally-moderated desired
demand and the accessibility-constrained demand.

They differ from dietary demand mainly in their accessibility drivers, which
reflect each behavior's economics. Both retain an income (GDP) response, but
transportation demand also responds to energy scarcity and to the climate-risk
attribution that accompanies the changing clean-energy share, while fertilizer
demand responds to relative scarcity and to natural-gas availability and price
(a key input cost) and is bounded by a sustainability ceiling on useful
fertilizer per unit of land. Through these channels both behaviors stay coupled
to the rest of FRIDA: transportation energy feeds energy-related emissions, and
fertilizer use is tied to crop production and contributes N₂O emissions, so a
worsening climate can damp these demands just as it damps dietary ones.

### Behavior change policy

The Behavior Change Policy sub-model is where interventions enter the otherwise
self-contained feedback structure. Because behavior emerges from perceptions,
norm weights, reference conditions, and adjustment delays, policy acts by
shifting these underlying determinants rather than by forcing demand directly.
The levers are grouped into a small set of policy types that can be targeted at
the food demands (and, for some, at climate-risk perception):

- **Value-shift** policies that move the perceived desirability of a behavior.
- **Consumption-risk** policies that strengthen awareness of health and
  overconsumption consequences.
- **Climate-attribution** policies that increase how strongly climate risk is
  connected to a behavior.
- **Cultural-revaluation** policies that change the social-cultural value
  attached to a practice over the long run.

Each policy is switched on from a start year and phases in over a time-to-effect,
with cultural revaluation acting most slowly — consistent with the modelled
stickiness of culture. This lets demand-side mitigation be assessed dynamically
and probabilistically inside the model rather than imposed from outside.

### Calibration approach

Parameters are estimated under deep uncertainty. The dietary sub-models are
calibrated by minimizing squared error against historical observations of
production and per-capita demand for animal and vegetal products and total food
over the recent historical period, with the food and climate-risk sub-models
calibrated jointly because no reliable time series exists for climate-risk
perception. Calibration is partial — done within the module to keep errors from
propagating — and is followed by reducing each parameter to a likely range and
running large multivariate ensembles, so results are presented as a median with
67 % and 95 % confidence intervals. The climate-risk parameters, lacking
quantitative validation data, are assessed qualitatively against the documented
historical trajectory of public climate concern.
