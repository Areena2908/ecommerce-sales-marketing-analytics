from pathlib import Path
import random
import csv
from datetime import date, timedelta

random.seed(42)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

regions = ["Northeast", "Midwest", "South", "West"]
channels = ["Organic Search", "Paid Search", "Email", "Referral", "Social"]
categories = {
    "Home Decor": ["Ceramic Vase", "Wall Art", "Table Lamp", "Throw Pillow"],
    "Kitchen": ["Cookware Set", "Glass Storage", "Coffee Mug Set", "Cutting Board"],
    "Furniture": ["Accent Chair", "Side Table", "Bookshelf", "Storage Bench"],
    "Bedding": ["Sheet Set", "Duvet Cover", "Weighted Blanket", "Pillow Set"],
}

def write_csv(path, rows, fieldnames):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

customers = []
for i in range(1, 801):
    customers.append({
        "customer_id": f"C{i:04d}",
        "signup_date": date(2025, 1, 1) + timedelta(days=random.randint(0, 500)),
        "region": random.choice(regions),
        "customer_segment": random.choices(
            ["New Homeowner", "Apartment", "Family", "Designer"],
            weights=[28, 34, 26, 12],
        )[0],
    })

products = []
pid = 1
for category, names in categories.items():
    for name in names:
        price = random.randint(25, 240)
        cost = round(price * random.uniform(0.42, 0.68), 2)
        products.append({
            "product_id": f"P{pid:03d}",
            "product_name": name,
            "category": category,
            "unit_cost": cost,
            "list_price": price,
        })
        pid += 1

orders = []
order_items = []
start = date(2025, 1, 1)
for oid in range(1, 2401):
    order_date = start + timedelta(days=random.randint(0, 514))
    customer = random.choice(customers)
    channel = random.choices(channels, weights=[34, 20, 18, 16, 12])[0]
    item_count = random.choices([1, 2, 3, 4], weights=[52, 30, 14, 4])[0]
    selected_products = random.sample(products, item_count)
    total = 0
    for product in selected_products:
        quantity = random.choices([1, 2, 3], weights=[78, 18, 4])[0]
        unit_price = round(float(product["list_price"]) * random.uniform(0.86, 1.06), 2)
        total += quantity * unit_price
        order_items.append({
            "order_item_id": f"OI{len(order_items)+1:05d}",
            "order_id": f"O{oid:05d}",
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price": unit_price,
        })
    orders.append({
        "order_id": f"O{oid:05d}",
        "customer_id": customer["customer_id"],
        "order_date": order_date,
        "marketing_channel": channel,
        "total_amount": round(total, 2),
        "order_status": random.choices(["Completed", "Returned", "Cancelled"], weights=[92, 5, 3])[0],
    })

marketing_spend = []
month = date(2025, 1, 1)
while month <= date(2026, 5, 1):
    month_key = month.strftime("%Y-%m")
    for channel in channels:
        base = {
            "Organic Search": 1800,
            "Paid Search": 7200,
            "Email": 1300,
            "Referral": 950,
            "Social": 4300,
        }[channel]
        marketing_spend.append({
            "month": month_key,
            "channel": channel,
            "spend": round(base * random.uniform(0.82, 1.18), 2),
        })
    if month.month == 12:
        month = date(month.year + 1, 1, 1)
    else:
        month = date(month.year, month.month + 1, 1)

write_csv(DATA / "customers.csv", customers, ["customer_id", "signup_date", "region", "customer_segment"])
write_csv(DATA / "products.csv", products, ["product_id", "product_name", "category", "unit_cost", "list_price"])
write_csv(DATA / "orders.csv", orders, ["order_id", "customer_id", "order_date", "marketing_channel", "total_amount", "order_status"])
write_csv(DATA / "order_items.csv", order_items, ["order_item_id", "order_id", "product_id", "quantity", "unit_price"])
write_csv(DATA / "marketing_spend.csv", marketing_spend, ["month", "channel", "spend"])

print(f"Generated data in {DATA}")
