# VIT Placement Tracker

A Streamlit app for looking up per-company placement data — selections, campus-wise distribution, compensation, and eligibility criteria — across two batches (B.Tech 2025-2026 and 2024-2025), sourced from VIT's official [placement tracker](https://placements-tracker-btech2026.streamlit.app/).

## Repository Structure

- `app.py` — the Streamlit app.
- `companies_unified_db.json` — per-company database (selections, campus breakdown, eligibility) that `app.py` reads.
- `placement_data.xlsx` — Excel export of the same data, offered as a download from within the app.
- `.streamlit/config.toml` — theme configuration.

## Running Locally

```bash
pip install streamlit pandas openpyxl
streamlit run app.py
```

Opens at `http://localhost:8501`.

## Features

- Search or quick-select a company to see its 2026 vs 2025 offer counts, YoY trend, and average CTC.
- Campus-wise selection breakdown (Vellore, Chennai, Bhopal, Amaravati) per year.
- Eligibility criteria: CGPA cutoffs, 9-pointer vs non-9-pointer hiring split, eligible branches.
- 2026 hiring timeline (month-by-month offers and CTC) where available.
- "Explore all recruiters" directory table, filterable by name, with Excel/JSON download buttons.
