# AI Data Analytics Assistant

> A business-facing data + AI teaching demo: turn a natural-language question into governed analytics.  
> **Synthetic data · No API key · No database credential**

## From question to insight

```mermaid
flowchart LR
A[Business question] --> B[Intent routing]
B --> C[Governed metric]
C --> D[Sales dataset]
D --> E[Aggregation]
E --> F[KPI + table + chart]
```

## Dashboard concept

| KPI | Definition |
|---|---|
| Revenue | Quantity × Unit price |
| Cost | Quantity × Unit cost |
| Gross profit | Revenue − Cost |

```mermaid
flowchart TD
A[Which product has highest revenue?] --> B[Metric: Revenue]
C[Show revenue by region] --> D[Dimension: Region]
E[Show monthly sales trend] --> F[Dimension: Month]
G[Highest gross profit?] --> H[Metric: Gross Profit]
B --> I[Analytics engine]
D --> I
F --> I
H --> I
I --> J[Visual result]
```

## Questions available in the demo

**Product performance** — Which product has the highest revenue?  
**Regional analysis** — Show revenue by region.  
**Trend analysis** — Show monthly sales trend.  
**Profitability** — Which product has the highest gross profit?

The Streamlit app displays headline KPIs, a result table and a chart from the same governed metric definitions.

## Why this matters for AI analytics

```mermaid
flowchart LR
A[Natural language] --> B[Semantic definitions]
B --> C[Validated query logic]
C --> D[Data]
D --> E[Answer]
```

The baseline deliberately uses deterministic routing. This makes it possible to explain the next step—Text-to-SQL—without pretending that unrestricted LLM-generated SQL is automatically safe.

## Actual dashboard results

These charts are calculated from the repository's 1,800-row synthetic sales dataset (fixed seed = 7).

### Revenue by product

```mermaid
xychart-beta
    title "Revenue by product"
    x-axis ["Laptop","Monitor","Headset","Keyboard"]
    y-axis "Revenue" 0 --> 1700000
    bar [1586642,481869,189625,129852]
```

### Monthly revenue trend

```mermaid
xychart-beta
    title "Monthly revenue trend"
    x-axis ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    y-axis "Revenue" 0 --> 260000
    line [165847,206169,204786,189326,172859,247685,213314,234632,179427,219395,151109,203440]
```

The same governed definitions—Revenue, Cost and Gross Profit—are used by the Streamlit dashboard.

## Quick start
```bash
python -m venv .venv
pip install -r requirements.txt
python src/generate_sales.py
streamlit run app.py
```

## Learning roadmap
Deterministic routing → semantic layer → DuckDB → Text-to-SQL → SQL validation → execution → audit

## Topics we can discuss
KPI design · dimensions and metrics · pandas aggregation · visualization · semantic layer · natural-language analytics · Text-to-SQL concepts · AI guardrails

## Privacy & security
The dataset is fully synthetic. No API keys, credentials, private database connections or company information are included.
