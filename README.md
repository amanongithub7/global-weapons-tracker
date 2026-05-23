# Global Weapons Tracker 🕊️

Research defense industry data: countries and regional entities, their weapons
producers, supply chains, and trade flows.

## Quick Start 📝

```bash
make install
source .venv/bin/activate
python weapons_tracker.py --help
```

## Usage 🧑‍💻

### Look up a country or entity's weapons producers

```bash
python weapons_tracker.py entity usa
python weapons_tracker.py entity russia
python weapons_tracker.py entity india
```

### Look up a company and its supply chain

```bash
python weapons_tracker.py company "Lockheed Martin"
python weapons_tracker.py company "Rheinmetall"
python weapons_tracker.py company "Hindustan Aeronautics"
```

### Query weapons trade flows

```bash
python weapons_tracker.py trade --from "usa"
python weapons_tracker.py trade --to "india"
python weapons_tracker.py trade --from "russia" --to "china"
```

### List available data

```bash
python weapons_tracker.py list entities
python weapons_tracker.py list companies
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
