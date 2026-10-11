import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
from google.cloud import storage
import io
import functions_framework
from data_generator import generate_mock_orders

# fake = Faker()
# Faker.seed(42)  # Seed for reproducibility

# CUSTOMER_POOL = [{"customer_id":fake.uuid4(),"customer_name":fake.name()} for _ in range(300)]  # Pre-generate a pool of customer IDs

# def generate_mock_orders(num_order=5000):
#     orders = []
#     for _ in range(num_order):
#         customer = random.choice(CUSTOMER_POOL)
#         order = {
#             "order_id": fake.uuid4(),
#             "customer_id": customer["customer_id"],
#             "customer_name": customer["customer_name"],
#             "product_category": random.choice(["Electronics", "Clothing", "Home & Kitchen", "Books", "Toys"]),
#             "price": round(random.uniform(5.0, 500.0), 2),
#             "quantity": random.randint(1, 10),
#             "order_date": (datetime.now() - timedelta(minutes=random.randint(0, 1440))).strftime("%Y-%m-%d %H:%M:%S"),
#             "status": random.choice(["Pending", "Shipped", "Delivered", "Cancelled"])
#         }
#         orders.append(order)

#     df = pd.DataFrame(orders)
#     return df

@functions_framework.http
def run_pipeline(request):
    try:
        #1. Generate mock orders
        df = generate_mock_orders()

        #2. Write the DataFrame to an in-memory Parquet byte stream
        parquet_buffer = io.BytesIO()
        df.to_parquet(parquet_buffer, index = False)
        parquet_buffer.seek(0) # Move the cursor to the beginning of the stream

        #3. Stream it directly to your GCS bucket
        bucket_name = "ecommerce-data-pipeline-511117-raw-data"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"daily_mock_orders_{timestamp}.parquet"

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        blob.upload_from_file(parquet_buffer, content_type='application/octet-stream')

        return f"Successfully generated and uploaded {len(df)} mock orders to {bucket_name}/{file_name}", 200
    except Exception as e:
        return f"An error occurred: {str(e)}", 500