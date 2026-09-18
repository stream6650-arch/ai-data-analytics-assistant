# AI Data Analytics Assistant

A local teaching demo of **business question → governed metric → analysis → visualization**. No API key is required.

## Flow
Business Question → Intent / Metric Selection → Synthetic Sales Data → Analytics → Table + KPI + Chart

## Quick start
```bash
python -m venv .venv
pip install -r requirements.txt
python src/generate_sales.py
streamlit run app.py
```

## Metric definitions
- Revenue = quantity × unit price
- Cost = quantity × unit cost
- Gross profit = revenue − cost

## Why deterministic first?
The baseline uses deterministic intent routing, so it is reproducible and cannot generate arbitrary SQL. It provides a safe baseline for teaching Text-to-SQL, semantic definitions and SQL validation.

## Privacy & security
Synthetic data only. No API keys, credentials, private database connections or company data.