# E-commerce Sales & Marketing Analytics

Portfolio project analyzing e-commerce sales, customer behavior, product performance, and marketing channel efficiency.

## Business Goal

Identify which products, regions, and marketing channels drive the strongest revenue, customer value, and return on ad spend. The project also highlights operational trends and opportunities for budget optimization.

## Tools Used

- SQL for business analysis queries
- Python for data cleaning, KPI calculation, and visualization
- Pandas, NumPy, Matplotlib
- CSV datasets

## Key Questions

- Which product categories generate the most revenue and profit?
- Which marketing channels have the strongest return on ad spend?
- How do customer segments differ by order value and repeat purchase behavior?
- Which regions show the strongest growth trends?
- Where should marketing budget be reallocated based on CAC, LTV, ROI, and payback?

## Project Structure

```text
data/
  customers.csv
  products.csv
  orders.csv
  order_items.csv
  marketing_spend.csv
sql/
  analysis_queries.sql
src/
  generate_data.py
  analyze.py
outputs/
  charts/
  kpi_summary.csv
```

## Main KPIs

- Revenue
- Gross profit
- Average order value
- Conversion rate
- Customer acquisition cost
- Return on ad spend
- LTV/CAC ratio
- Repeat customer rate

## Insights Summary

Run the analysis script to generate the latest KPI summary and charts:

```bash
python3 src/generate_data.py
python3 src/analyze.py
```

Generated outputs are saved in `outputs/`.

## Resume Bullet

Built an e-commerce analytics project using SQL and Python to analyze sales, product performance, customer segments, CAC, LTV, ROI, and marketing channel efficiency; created KPI summaries and visualizations to recommend budget optimization opportunities.
