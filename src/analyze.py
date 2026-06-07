from pathlib import Path
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
CHARTS = OUT / "charts"
OUT.mkdir(exist_ok=True)
CHARTS.mkdir(parents=True, exist_ok=True)

customers = pd.read_csv(DATA / "customers.csv", parse_dates=["signup_date"])
products = pd.read_csv(DATA / "products.csv")
orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
items = pd.read_csv(DATA / "order_items.csv")
spend = pd.read_csv(DATA / "marketing_spend.csv")

orders_completed = orders[orders["order_status"] == "Completed"].copy()
items_enriched = items.merge(products, on="product_id", how="left")
items_enriched["revenue"] = items_enriched["quantity"] * items_enriched["unit_price"]
items_enriched["gross_profit"] = items_enriched["quantity"] * (items_enriched["unit_price"] - items_enriched["unit_cost"])
order_detail = items_enriched.merge(orders_completed, on="order_id", how="inner")
order_detail = order_detail.merge(customers, on="customer_id", how="left")
order_detail["month"] = order_detail["order_date"].dt.to_period("M").astype(str)

monthly = order_detail.groupby("month", as_index=False).agg(
    revenue=("revenue", "sum"),
    gross_profit=("gross_profit", "sum"),
    orders=("order_id", "nunique"),
)
monthly["average_order_value"] = monthly["revenue"] / monthly["orders"]

category = order_detail.groupby("category", as_index=False).agg(
    revenue=("revenue", "sum"),
    gross_profit=("gross_profit", "sum"),
    units_sold=("quantity", "sum"),
).sort_values("revenue", ascending=False)

channel_revenue = order_detail.groupby("marketing_channel", as_index=False).agg(
    revenue=("revenue", "sum"),
    customers=("customer_id", "nunique"),
)
channel_spend = spend.groupby("channel", as_index=False).agg(spend=("spend", "sum"))
channel = channel_revenue.merge(channel_spend, left_on="marketing_channel", right_on="channel", how="left")
channel["roas"] = channel["revenue"] / channel["spend"]
channel["cac"] = channel["spend"] / channel["customers"]
channel["ltv_cac_ratio"] = (channel["revenue"] / channel["customers"]) / channel["cac"]
channel = channel.sort_values("roas", ascending=False)

regional = order_detail.groupby("region", as_index=False).agg(
    revenue=("revenue", "sum"),
    orders=("order_id", "nunique"),
)

kpis = pd.DataFrame([{
    "total_revenue": round(order_detail["revenue"].sum(), 2),
    "gross_profit": round(order_detail["gross_profit"].sum(), 2),
    "orders": orders_completed["order_id"].nunique(),
    "customers": orders_completed["customer_id"].nunique(),
    "average_order_value": round(order_detail["revenue"].sum() / orders_completed["order_id"].nunique(), 2),
    "best_roas_channel": channel.iloc[0]["marketing_channel"],
    "best_roas": round(channel.iloc[0]["roas"], 2),
}])

kpis.to_csv(OUT / "kpi_summary.csv", index=False)
monthly.to_csv(OUT / "monthly_revenue.csv", index=False)
category.to_csv(OUT / "category_performance.csv", index=False)
channel.to_csv(OUT / "channel_performance.csv", index=False)

plt.figure(figsize=(10, 5))
plt.plot(monthly["month"], monthly["revenue"], marker="o")
plt.title("Monthly Revenue")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(CHARTS / "monthly_revenue.png", dpi=160)
plt.close()

plt.figure(figsize=(8, 5))
plt.bar(category["category"], category["revenue"])
plt.title("Revenue by Product Category")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(CHARTS / "category_revenue.png", dpi=160)
plt.close()

plt.figure(figsize=(8, 5))
plt.bar(channel["marketing_channel"], channel["roas"])
plt.title("Return on Ad Spend by Channel")
plt.ylabel("ROAS")
plt.tight_layout()
plt.savefig(CHARTS / "channel_roas.png", dpi=160)
plt.close()

plt.figure(figsize=(8, 5))
plt.bar(regional["region"], regional["revenue"])
plt.title("Revenue by Region")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(CHARTS / "regional_revenue.png", dpi=160)
plt.close()

print("Analysis complete. Outputs saved in outputs/.")
