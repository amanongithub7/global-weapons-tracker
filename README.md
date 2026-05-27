# Global Weapons Tracker 🕊️

Global Weapons Tracker surfaces defense industry data: countries and regional
entities, their weapons producers, supply chains, and trade flows. By tracking
who builds weapons, who buys them, and where the money flows, this project seeks
to provide the data infrastructure needed to hold these exploitative and violent
systems accountable. See [motivation](#motivation-🌍) for stats on the human and
environmental toll of warfare.

## Quick Start 📝

First, clone this repository onto your computer of choice. Then, run the
following commands from within the `global-weapons-tracker/` directory. After
this, global-weapons-tracker will be installed on your system as a CLI tool.

```bash
make install
source .venv/bin/activate
gwt --help
# OR
global-weapons-tracker --help
```

## Usage 🧑‍💻

> To access the CLI, you can use either `global-weapons-tracker` or `gwt`. `gwt`
> is configured by some zsh plugins and other programs to be an alias for git
> worktree.

### Look up a country or entity's weapons producers

```bash
gwt entity usa
gwt entity russia
gwt entity india
```

### Look up a company and its supply chain

```bash
gwt company "Lockheed Martin"
gwt company "Rheinmetall"
gwt company "Hindustan Aeronautics"
```

### Query weapons trade flows

```bash
gwt trade --from "usa"
gwt trade --to "india"
gwt trade --from "russia" --to "china"
```

### List available data

```bash
gwt list entities
gwt list companies
```

## Data Format 📊

- **Entities**: `data/countries-and-entities/<slug>.yaml` — per-entity files
  with producers, exports, imports, and cited sources
- **Companies**: `data/companies/<slug>.yaml` — per-company files with key
  programs, suppliers, subsidiaries, and sources
- **Trade flows**: `data/trade/trade_flows.csv` — bilateral transfer records
  with estimated values and category

All data points include a `sources` field with URLs to the original source
(primarily SIPRI, company annual reports, government publications).

## Adding Data ❇️

1. Create a new YAML file in `data/countries-and-entities/` or `data/companies/`
2. Follow the schema of existing files
3. Always include a `sources` array with verifiable citations
4. For trade flows, append rows to `data/trade/trade_flows.csv`

## Data Sources ℹ️

- [SIPRI Arms Transfers Database](https://www.sipri.org/databases/armstransfers)
- [SIPRI Top 100](https://www.sipri.org/research/armament-and-disarmament/arms-transfers-and-military-spending/arms-production/military-spending-and-arms-production-sipri-top-100)
- Company annual reports and investor relations pages
- National defense ministry / export reports

## Roadmap 🗺️

- Web-based map visualization of trade flows
- Supply chain graph rendering
- Historical time-series data
- More countries and companies

## Motivation 🌍

The global weapons industry is a major driver of human suffering, environmental
destruction, and wealth extraction — three interconnected crises that this
project aims to make visible through open data.

### Human Cost ☠️

Armed conflict is a leading contributor to the global burden of disease. Beyond
direct battlefield deaths, conflicts kill indirectly through the collapse of
healthcare infrastructure, displacement, famine, and epidemic outbreaks. A study
by Imperial College London found that wars were associated with 29.4 million
indirect civilian deaths globally between 1990 and 2017, with indirect mortality
often exceeding direct combat fatalities by ratios of 3:1 to 15:1 [1]. Brown
University's Costs of War project estimates that post-9/11 conflicts in
Afghanistan, Iraq, Syria, Yemen, and Pakistan have caused 4.5–4.7 million deaths
(direct and indirect) as of 2023, with indirect deaths accounting for 3.6–3.8
million of that total [2, 3]. Every day, explosive remnants of war, ranging from
landmines to cluster munition duds, continue to kill and maim civilians long
after active fighting ends [4].

### Environmental Cost 🧯

Militaries are among the world's largest institutional emitters of greenhouse
gases, yet they are exempt from mandatory emissions reporting under the Kyoto
and Paris agreements [5, 6]. The U.S. Department of Defense is the single
largest institutional consumer of hydrocarbons on Earth, emitting an estimated
636 million metric tons of CO₂ equivalent between 2010 and 2019 — more than the
entire national emissions of Sweden or Portugal [7, 8]. If all the world's
militaries were a country, they would rank as the fourth-largest greenhouse gas
emitter globally [5]. Explosive weapons deposit heavy metals, depleted uranium,
white phosphorus, and other toxic substances into soil and water, contaminating
ecosystems for generations [9, 10]. The United Nations recognizes that "armed
conflicts use large quantities of munitions containing heavy metals and depleted
uranium, and explosive chemicals, all toxic even in modest quantities, with
devastating impacts on the environment" [11].

### Profit Motive 🪎

The weapons industry is a $679 billion-a-year business. In 2024, the SIPRI Top
100 arms-producing companies posted their highest combined arms revenues ever, a
26% increase over the prior decade [12]. Global military expenditure reached
$2.7 trillion in 2024 and $2.9 trillion in 2025 — the steepest growth since the
Cold War [13, 14]. The industry is dominated by a handful of publicly traded
corporations that exist primarily to enrich shareholders: Lockheed Martin
returned $3.0 billion in share buybacks alone in FY2025, alongside $13.35 per
share in dividends, while maintaining a net profit margin above 6% [15]. SIPRI
notes that rising military expenditure "diverts resources from social
expenditure" and comes at the direct expense of progress on the UN Sustainable
Development Goals [16].

By tracking who builds weapons, who buys them, and where the money flows, this
project seeks to provide the data infrastructure needed to hold these systems
accountable.

#### References

1. Jawad, M., et al. (2020). "Estimating indirect mortality impacts of armed
   conflict in civilian populations." _BMC Medicine_.
   [PMC7487992](https://pmc.ncbi.nlm.nih.gov/articles/PMC7487992/)
2. Savell, S. (2023). "How Death Outlives War: The Reverberating Impact of the
   Post-9/11 Wars on Human Health." Costs of War, Brown University.
   [how-death-outlives-war](https://costsofwar.watson.brown.edu/papers/how-death-outlives-war)
3. Costs of War, Brown University. "Human Costs."
   [costs/human](https://costsofwar.watson.brown.edu/costs/human)
4. UNICEF. "Conflict-related deaths per 100,000 population."
   [CME_CNFLCT](https://data.unicef.org/indicator-profiles/CME_CNFLCT)
5. American Academy of Arts and Sciences. (2025). "The Environmental Impacts of
   Modern Wars."
   [amacad.org](https://www.amacad.org/news/carbon-footprint-military-environmental-impacts-war)
6. Crawford, N. C. (2019). "Pentagon Fuel Use, Climate Change, and the Costs of
   War." Costs of War, Brown University.
   [PDF](https://watson.brown.edu/costsofwar/files/cow/imce/papers/2019/Summary_Pentagon%20Fuel%20Use%2C%20Climate%20Change%2C%20and%20the%20Costs%20of%20War%20%281%29.pdf)
7. Thombs, R. (2025). "US military carbon footprint." _PLOS Climate_. Via
   [BBC Science Focus](https://www.sciencefocus.com/news/us-military-carbon-footprint)
8. Earth.org. "The Environmental Impact of the US Military."
   [earth.org](https://earth.org/us-military-pollution/)
9. Costs of War, Brown University. "Environmental Costs."
   [costs/environmental](https://costsofwar.watson.brown.edu/costs/environmental)
10. United Nations. "How conflict impacts our environment."
    [un.org](https://www.un.org/en/peace-and-security/how-conflict-impacts-our-environment)
11. United Nations. Ibid.
12. Scarazzato, L., et al. (2025). "The SIPRI Top 100 Arms-producing and
    Military Services Companies, 2024." SIPRI.
    [DOI: 10.55163/XPGD6816](https://www.sipri.org/publications/2025/sipri-fact-sheets/sipri-top-100-arms-producing-and-military-services-companies-2024)
13. Liang, X., et al. (2025). "Trends in World Military Expenditure, 2024."
    SIPRI.
    [DOI: 10.55163/AVEC8366](https://www.sipri.org/publications/2025/sipri-fact-sheets/trends-world-military-expenditure-2024)
14. SIPRI. (2026). "Global military spending rise continues." Press release, 27
    April 2026.
    [sipri.org](https://www.sipri.org/media/press-release/2026/global-military-spending-rise-continues-european-and-asian-expenditures-surge)
15. Lockheed Martin financial data via
    [Stock Titan](https://www.stocktitan.net/financials/LMT) and
    [Macrotrends](https://www.macrotrends.net/stocks/charts/LMT/lockheed-martin/net-profit-margin)
16. Tian, N. & Liang, X. (2025). "Rebalancing Military Spending Towards
    Achieving Sustainable Development." SIPRI.
    [DOI: 10.55163/ZCIE5196](https://www.sipri.org/publications/2025/policy-reports/rebalancing-military-spending-towards-achieving-sustainable-development)
