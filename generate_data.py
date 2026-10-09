import pandas as pd
from faker import Faker
import random
from datetime import datetime



fake = Faker()


def generate_mock_orders(num_orders=100):
    orders=[]

    for _ in range(num_orders):
        order = {
            "order_id": fake.uuid4(),
            "customer_id": fake.uuid4(),
            "customer_name": fake.name(),
            "product_category": random.choice(["Electronics", "Clothing", "Home & Kitchen", "Books", "Toys"]),
            "price": round(random.uniform(5.0, 500.0), 2),
            "quantity": random.randint(1, 10),
            "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": random.choice(["Pending", "Shipped", "Delivered", "Cancelled"])
        }
        orders.append(order)

    df = pd.DataFrame(orders)
    return df

if __name__ == "__main__":
    num_orders = 100  # You can change this number to generate more or fewer orders
    mock_orders_df = generate_mock_orders(num_orders)
    file_name = "data/daily_mock_orders.parquet"
    mock_orders_df.to_parquet(file_name, index=False)
    print(f"Generated {num_orders} mock orders and saved to {file_name}")