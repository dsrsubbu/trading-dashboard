# Project Structure & Cleanup Guide

## Overview
This document explains the cleaned-up project structure and organizational decisions made.

---

## Directory Structure (Post-Cleanup)

```
trading-dashboard/
├── src/                          # (Future: move core modules here)
│
├── data/                         # Generated data & outputs
│   ├── nse_raw/                 # Raw NSE Bhavcopy files
│   ├── bse_raw/                 # Raw BSE Bhavcopy files
│   └── combined_dashboard_live.csv
│
├── logs/                         # Structured logs (auto-generated)
│   └── trading_dashboard_YYYYMMDD.log
│
├── watchlist/                    # Watchlist & trade records
│   ├── active_watchlist.csv
│   └── closed_trades.csv
│
├── deprecated/                   # Old/superseded scripts (archive)
│   ├── audit_phase*.py
│   ├── test_*.py
│   ├── check_*.py
│   ├── auto_update.py
│   └── ...
│
├── tests/                        # Unit tests (pytest)
│   ├── conftest.py
│   ├── test_progressive_screener.py
│   ├── test_config.py
│   └── __init__.py
│
├── config.py                     # Centralized configuration
├── progressive_screener.py       # 12-condition screening logic
├── auto_update_smart.py          # Main pipeline (canonical)
├── nse_downloader_fixed_nov2025.py  # NSE downloader (canonical)
├── bse_downloader_working.py     # BSE downloader (canonical)
├── data_downloader_improved.py   # Improved downloader utils
├── dashboard_full.py             # Streamlit UI (primary)
├── watchlist_manager.py          # Watchlist management
├── requirements.txt              # Python dependencies
├── README.md                     # Quick-start guide
└── CLEANUP.md                    # This file
```

---

## What Was Removed/Archived

### ✅ Root-level Artifacts (DELETED)
- `bse['ATW_1M']`, `bse['DELIV_PER_1W']`, etc. — REPL debug output
- `df`, `df.columns` — Debug variable dumps
- `SC_CODE` — Stray config file
- `100000`, `20`, `50`, etc. — Numeric debug files
- **Total removed:** ~25 files

### 📦 Deprecated Scripts (MOVED to `/deprecated`)
- **Audit scripts:** `audit_phase*.py`, `audit_test*.py`, `audit_pipeline*.py`
  - Kept separate for historical debugging reference
  - Use only if you need to re-verify old logic
- **Check scripts:** `check_bse.py`, `check_data.py`, `check_columns.py`, etc.
  - Replaced by improved diagnostics in main pipeline
- **Test scripts:** `test_bse.py`, `test_download.py`, `test_scanner/`
  - Replaced by proper pytest suite in `/tests`
- **Old downloaders:** `bse_downloader.py`, `bse_downloader_fixed.py`, `data_downloader.py`
  - Use canonical: `bse_downloader_working.py`, `data_downloader_improved.py`
- **Old auto_update:** `auto_update.py`, `auto_update_smart2.py`
  - Use canonical: `auto_update_smart.py`

---

## Key Changes Made

### 1. **Structured Logging** ✅
- Added `Config.setup_logger()` in `config.py`
- All scripts now log to `logs/trading_dashboard_YYYYMMDD.log`
- Includes file + console handlers with timestamps
- **Usage:** `logger = Config.setup_logger(__name__)`

### 2. **Holidays Configuration** ✅
- Moved hardcoded holidays from `auto_update_smart.py` to `config.py`
- **Update annually:** Edit `Config.TRADING_HOLIDAYS` each year
- Auto-used by pipeline via `Config.TRADING_HOLIDAYS`

### 3. **Type Hints** ✅
- Added type annotations to `ProgressiveSpiker` class
- Improves IDE autocomplete and type checking
- Future: expand to all core functions

### 4. **Unit Tests** ✅
- Created `/tests` folder with pytest suite
- `test_progressive_screener.py` — 5 tests for 12-condition logic
- `test_config.py` — Configuration validation
- Run with: `pytest tests/ -v`

### 5. **Requirements Updated** ✅
- Added development dependencies:
  - `pytest` — Unit testing
  - `black` — Code formatting
  - `flake8` — Linting
  - `pylint` — Advanced linting

---

## Canonical Versions (Use These)

| Purpose | File | Status |
|---------|------|--------|
| NSE Download | `nse_downloader_fixed_nov2025.py` | ✅ Canonical |
| BSE Download | `bse_downloader_working.py` | ✅ Canonical |
| Data Utils | `data_downloader_improved.py` | ✅ Canonical |
| Auto-Update Pipeline | `auto_update_smart.py` | ✅ Canonical |
| Dashboard UI | `dashboard_full.py` | ✅ Canonical |
| Screener Logic | `progressive_screener.py` | ✅ Canonical |

---

## Next Steps (Recommendations)

### Short-term (1-2 days)
- [ ] Run `pytest tests/ -v` to verify test suite
- [ ] Format code with `black .`
- [ ] Run `flake8 *.py --max-line-length=100`
- [ ] Test `python auto_update_smart.py` — should log to `logs/`

### Medium-term (1-2 weeks)
- [ ] Add more unit tests for downloaders & normalization
- [ ] Migrate core logic to `/src` folder (optional refactoring)
- [ ] Add GitHub Actions CI to run tests on push
- [ ] Add data validation schema checks

### Long-term
- [ ] Create `CONTRIBUTING.md` for collaboration guidelines
- [ ] Document watchlist & win-rate API
- [ ] Add REST API wrapper (Flask/FastAPI) for external access
- [ ] Add Docker support for deployment

---

## How to Use Deprecated Folder

If you need to recover old logic:

```bash
# Search deprecated audit scripts
ls deprecated/audit_phase*.py

# Run an old test script
python deprecated/test_bse.py

# Inspect old downloader logic
cat deprecated/auto_update.py | grep "def download"
```

**Do NOT rely on deprecated scripts for production.** They exist only for historical reference.

---

## Troubleshooting

### Tests fail with import errors
```bash
cd trading-dashboard
pip install -r requirements.txt
pytest tests/ -v
```

### Logs not appearing
- Check `logs/` directory exists: `ls logs/`
- Run `python auto_update_smart.py` — creates log files automatically
- Check log level: `Config.LOG_LEVEL` in `config.py`

### Holiday calendar needs update for 2026
1. Edit `config.py`
2. Update `Config.TRADING_HOLIDAYS` list with 2026 holidays
3. Commit and push

---

## File Sizes (Post-Cleanup)

```
Before: ~50 MB (with duplicate scripts and artifacts)
After:  ~15 MB (cleaned up)
Reduction: 70% ✅
```

---

*Last updated: 2025-12-31*
