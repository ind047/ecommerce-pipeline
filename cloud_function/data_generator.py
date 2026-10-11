# cloud_function/data_generator.py
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)

CUSTOMER_POOL = [
    {"customer_id": fake.uuid4(), "customer_name": fake.name()}
    for _ in range(300)
]

def generate_mock_orders(num_orders=5000):
    orders = []
    for _ in range(num_orders):
        customer = random.choice(CUSTOMER_POOL)   # inside the loop!
        orders.append({
            "order_id": fake.uuid4(),
            "customer_id": customer["customer_id"],
            "customer_name": customer["customer_name"],
            "product_category": random.choice(["Electronics", "Clothing", "Home & Kitchen", "Books", "Toys"]),
            "price": round(random.uniform(5.0, 500.0), 2),
            "quantity": random.randint(1, 10),
            "order_date": (datetime.now() - timedelta(minutes=random.randint(0, 1440))).strftime("%Y-%m-%d %H:%M:%S"),
            "status": random.choice([...]),
        })
    return pd.DataFrame(orders)