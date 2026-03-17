"""
Generate realistic Amazon e-commerce sales data for the analytics dashboard.
Produces ~2000 rows of transactional data in amazon_sales_data.csv.
"""

import csv
import random
import os
from datetime import datetime, timedelta

random.seed(42)

# --- Configuration ---
NUM_ROWS = 2000
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "amazon_sales_data.csv")

CATEGORIES = [
    "Electronics", "Clothing", "Home & Kitchen", "Books",
    "Sports & Outdoors", "Beauty & Personal Care", "Toys & Games", "Grocery"
]

REGIONS = ["North", "South", "East", "West"]

PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Cash on Delivery", "Net Banking"]

# Price ranges per category (min, max)
PRICE_RANGES = {
    "Electronics": (2000, 80000),
    "Clothing": (300, 5000),
    "Home & Kitchen": (500, 25000),
    "Books": (100, 2000),
    "Sports & Outdoors": (400, 15000),
    "Beauty & Personal Care": (150, 5000),
    "Toys & Games": (200, 8000),
    "Grocery": (50, 3000),
}

# --- Generate data ---
def generate_dataset():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    day_range = (end_date - start_date).days

    rows = []
    for i in range(1, NUM_ROWS + 1):
        category = random.choice(CATEGORIES)
        price_min, price_max = PRICE_RANGES[category]

        order_date = start_date + timedelta(days=random.randint(0, day_range))
        price = round(random.uniform(price_min, price_max), 2)
        discount_percent = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40])
        quantity_sold = random.randint(1, 5)
        rating = round(random.uniform(1.0, 5.0), 1)
        review_count = random.randint(0, 500)
        discounted_price = round(price * (1 - discount_percent / 100), 2)
        total_revenue = round(discounted_price * quantity_sold, 2)

        rows.append({
            "order_id": f"ORD-{i:05d}",
            "order_date": order_date.strftime("%Y-%m-%d"),
            "product_id": f"PROD-{random.randint(1000, 9999)}",
            "product_category": category,
            "price": price,
            "discount_percent": discount_percent,
            "quantity_sold": quantity_sold,
            "customer_region": random.choice(REGIONS),
            "payment_method": random.choice(PAYMENT_METHODS),
            "rating": rating,
            "review_count": review_count,
            "discounted_price": discounted_price,
            "total_revenue": total_revenue,
        })

    # Write CSV
    fieldnames = list(rows[0].keys())
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {NUM_ROWS} rows -> {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_dataset()
