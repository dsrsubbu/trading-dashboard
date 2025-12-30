# Trading Dashboard

A compact trading data pipeline + Streamlit dashboard for NSE & BSE — downloads raw bhav and delivery files, normalizes + merges them, runs a 12-condition "Progressive Spike" screener, and provides a watchlist & performance reporting UI.

---

## Features ✅

- Data downloaders for NSE & BSE (bhav + delivery).
- Full auto-update pipeline with backfill and normalization (`auto_update_smart.py`).
- 12-condition Progressive Spike screener (`progressive_screener.py`).
- Streamlit UI (`dashboard_full.py`) with pages: Dashboard, Data Health, Signals, Verify Conditions, Watchlist, Win Rate.
- Watchlist management and trade recording (`watchlist_manager.py`).
- Audit & diagnostic scripts to validate formulas and merges (`audit_pipeline_faithful.py`, `verify_downloads.py`, `diagnose_bse_delivery_merge.py`).

---

## Quick start (Windows)

1. Create & activate venv:

   python -m venv venv
   venv\Scripts\activate.bat

2. Install dependencies:

   pip install -r requirements.txt

3. Populate data (network required):

   python auto_update_smart.py

   This writes `data/combined_dashboard_live.csv` and `data/dashboard_cloud.csv` (used by the dashboard).

4. Run the dashboard (UI):

   streamlit run dashboard_full.py

   Or use `run.bat` (Windows helper) which activates the venv and starts Streamlit.

---

## Important files & commands

- `requirements.txt` — dependencies (Streamlit, pandas, requests, bs4, python-dateutil)
- `auto_update_smart.py` — main pipeline (downloads, normalize, merge, compute metrics)
- `dashboard_full.py` — primary Streamlit app (recommended)
- `progressive_screener.py` — 12-condition logic
- `data_downloader_improved.py` — download helper (NSE/BSE)
- `watchlist_manager.py` — add/close/delete positions, export & win-rate
- `config.py` — directory & threshold configuration (auto-creates directories)

---

## How the 12 conditions work (summary)

- Baseline (3): Delivery % ≥ 50; Delivery Turnover ≥ ₹5,000,000; ATW ≥ ₹20,000.
- Progressive (9): For each metric (DELIV_PER, DELIVERY_TURNOVER, ATW): Today > 1W > 1M > 3M.

See `progressive_screener.py` for exact checks.

---

## Troubleshooting & Tips ⚠️

- If the dashboard shows missing data: run `python auto_update_smart.py` and inspect `data/` files.
- Use `audit_pipeline_faithful.py` to verify DELIVERY_TURNOVER and ATW formulas against raw files.
- BSE downloads can be flaky; fallback proxies exist in the downloader code (see `data_downloader_improved.py`).

---

## Next improvements (suggestions)

- Add unit tests for normalization/merge steps and a CI job for sanity checks.
- Add a short `CONTRIBUTING.md` and a cross-platform start script.

---

If you want, I can also add a short Quick Reference or a Troubleshooting checklist as a separate file.
