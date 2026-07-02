# June 2026 Parliament Vote Forecasts

Pre-vote forecasts for a set of European Parliament procedures scheduled in June 2026. Each forecast was generated and published **before** the corresponding vote took place.

## Contents

Each top-level folder is named by procedure file number and holds the forecast for that procedure:

- `2023-0226/`
- `2024-0577/`
- `2025-0259/`
- `2025-0580/`
- `2025-0581/`
- `2025-2097/`
- `2026-0050/`

Supporting files:

- `predicted_votes_summary.csv` — consolidated forecast across all procedures
- `result.csv` — forecast vs. actual results with accuracy metrics
- `procedures.csv` — procedure reference list
- `plot_piecharts.py` — generates the per-procedure forecast charts
- `compute_results.py` — computes accuracy metrics against actual votes

## Results

Actual votes were recorded for 5 of the 7 procedures (2023-0226 and 2026-0050 had no recorded actual votes).

| Procedure | Title | Predicted | Actual | Match | MEP Accuracy |
|-----------|-------|-----------|--------|-------|-------------|
| 2024-0577 | Research Fund for Coal and Steel | For | For | ✓ | 81.1% |
| 2025-0259 | EU–Liberia Voluntary Partnership Agreement | For | For | ✓ | 59.8% |
| 2025-0580 | Excise duty on tobacco (recast) | For | Against | ✗ | 26.7% |
| 2025-0581 | Excise duty on tobacco (general) | For | For | ✓ | 30.7% |
| 2025-2097 | Immunity of Daniel Attard | Against | For | ✗ | 46.1% |

**Category match: 3/5 (60%)**

MEP-level accuracy is the percentage of MEPs whose individual predicted position (For/Against/Abstain) matched their actual vote, among MEPs who cast a vote.

---
[www.praevisa.eu](https://www.praevisa.eu)
