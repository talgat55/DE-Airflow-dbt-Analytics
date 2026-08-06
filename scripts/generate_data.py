import random
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker()

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"

def generate_customers(count: int = 500) -> pd.DataFrame:
    rows = []

    for customer_id in range(1, count + 1):
        rows.append(
            {
                "customer_id": customer_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.unique.email(),
                "country": fake.country(),
                "city": fake.city(),
                "registered_at": fake.date_time_between(
                    start_date="-2y",
                    end_date="now",
                ),
            }
        )

    return pd.DataFrame(rows)

def generate_products(count: int = 100) -> pd.DataFrame:
    categories = [
        "Electronics",
        "Clothes",
        "Books",
        "Home",
        "Beauty",
        "Sports",
    ]

    rows = []

    for product_id in range(1, count + 1):
        word = fake.word().strip().title()
        product_name = word or f"Product {product_id}"

        rows.append(
            {
                "product_id": product_id,
                "product_name": product_name,
                "category": random.choice(categories),
                "price": round(random.uniform(10, 1500), 2),
                "created_at": fake.date_time_between(
                    start_date="-2y",
                    end_date="now",
                ),
            }
        )

    return pd.DataFrame(rows)

def generate_orders(
    customers: pd.DataFrame,
    count: int = 1000
) -> pd.DataFrame:
    statuses = [
        "created",
        "paid",
        "shipped",
        "delivered",
        "cancelled",
    ]

    customer_ids = customers["customer_id"].tolist()
    rows = []
    for order_id in range(1, count + 1):
        rows.append(
            {
                "order_id": order_id,
                "customer_id": random.choice(customer_ids),
                "order_status": random.choice(statuses),
                "order_created_at": fake.date_time_between(
                    start_date="-1y",
                    end_date="now",
                ),
            }
        )

    return pd.DataFrame(rows)

def generate_order_items(
    orders: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    product_ids = products["product_id"].tolist()
    product_prices = dict(
        zip(products["product_id"], products["price"])
    )

    rows = []
    order_item_id = 1

    for order_id in orders["order_id"]:
        items_count = random.randint(1, 5)

        for _ in range(items_count):
            product_id = random.choice(product_ids)
            quantity = random.randint(1, 4)
            unit_price = product_prices[product_id]

            rows.append(
                {
                    "order_item_id": order_item_id,
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": unit_price,
                }
            )

            order_item_id += 1

    return pd.DataFrame(rows)

def generate_payments(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
) -> pd.DataFrame:
    methods = [
        "card",
        "cash",
        "paypal",
        "bank_transfer",
    ]

    payment_statuses = [
        "success",
        "failed",
        "refunded",
    ]

    order_totals = (
        order_items.assign(
            line_total=(
                order_items["quantity"]
                * order_items["unit_price"]
            )
        )
        .groupby("order_id")["line_total"]
        .sum()
        .to_dict()
    )

    rows = []

    for payment_id, order in enumerate(
        orders.itertuples(index=False),
        start=1,
    ):
        paid_at = None

        if order.order_status != "created":
            paid_at = fake.date_time_between(
                start_date=order.order_created_at,
                end_date="now",
            )

        rows.append(
            {
                "payment_id": payment_id,
                "order_id": order.order_id,
                "payment_method": random.choice(methods),
                "payment_status": random.choice(payment_statuses),
                "amount": round(
                    order_totals.get(order.order_id, 0),
                    2,
                ),
                "paid_at": paid_at,
            }
        )

    return pd.DataFrame(rows)

def save_csv(
    dataframe: pd.DataFrame,
    filename: str,
) -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    file_path = RAW_DATA_DIR / filename
    dataframe.to_csv(file_path, index=False)

    print(
        f"Saved {filename}:"
        f"{len(dataframe)} rows"
    )

def generate_all() -> None:
    customers = generate_customers()
    products = generate_products()
    orders = generate_orders(customers)
    order_items = generate_order_items(orders, products)
    payments = generate_payments(orders, order_items)

    save_csv(customers, "customers.csv")
    save_csv(products, "products.csv")
    save_csv(orders, "orders.csv")
    save_csv(order_items, "order_items.csv")
    save_csv(payments, "payments.csv")


if __name__ == "__main__":
    generate_all()