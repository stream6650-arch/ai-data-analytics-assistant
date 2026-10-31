# AI Data Analytics Assistant

**English** | [繁體中文](README.zh-TW.md)

A deployable Streamlit sales analytics teaching demo. Includes headline KPIs,
product and regional comparisons, monthly trends, bilingual keyword questions,
filters, charts, and CSV downloads. No API keys or database credentials required.

## Run locally

Use Python 3.12 (also used in CI and recommended for hosting).

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

The app generates 1,800 synthetic 2025 sales records in memory with seed=7.
No manual data generation step or persistent filesystem is required. To export
an optional standalone CSV, run `python src/generate_sales.py`.

## Deploy on Streamlit Community Cloud

1. Sign in at https://share.streamlit.io/ and connect your GitHub account.
2. Choose **Create app**, repository `stream6650-arch/ai-data-analytics-assistant`.
3. Select the branch containing these files (normally `main` after merging the PR).
4. Set main file path to `app.py`; choose Python **3.12** in advanced settings.
5. Click **Deploy**. No Secrets settings are needed. Share the resulting app URL.

This application needs a running Python server; GitHub Pages cannot host it.
Hosting availability, quotas and pricing depend on the provider's current plan.

## Questions and metric definitions

Examples: “Which product has the highest revenue?”, “Show revenue by region”,
“Show monthly sales trend”, “Which product has the highest gross profit?”.
Traditional Chinese examples are included in the interface.

Revenue = quantity × unit price; cost = quantity × unit cost;
gross profit = revenue − cost; margin = total gross profit / total revenue.
All KPIs, charts, and downloads respect the product, region, and month filters.
Amounts use illustrative currency units, not a real company's financial data.

Routing uses an allowlisted metric (revenue, cost, gross profit) and dimension
(product, region, month), not an LLM. Unsupported questions show guidance and
manual selectors. Arbitrary SQL, forecasts, and customer analysis are not supported.

## Project layout

- `app.py`: Streamlit interface and CSV downloads.
- `src/generate_sales.py`: reproducible synthetic data and optional CSV export.
- `src/analytics.py`: metric allowlist, bilingual routing, aggregation.
- `.streamlit/config.toml`: theme and headless configuration.
- `tests/`: calculation and Streamlit interaction tests.
- `.github/workflows/test.yml`: Python 3.12 CI.

Run tests: `python -m unittest discover -s tests -v`.

The original documentation's historical chart totals could not be reproduced
because its generator was missing. This version replaces those static claims
with results calculated directly from the included generator.

Learning roadmap: deterministic routing → semantic layer → DuckDB → Text-to-SQL
→ SQL validation → execution → audit. Data is synthetic; no external AI calls,
private database connections, or company data are included.
