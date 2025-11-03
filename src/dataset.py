# data generation function
import pandas as pd
import numpy as np
import random
import uuid
from datetime import datetime, timedelta

def generate_synthetic_transactions(
    num_customers=100,
    start_date="2024-01-01",
    end_date="2024-03-31",
    seed=42
):
    random.seed(seed)
    np.random.seed(seed)

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    num_days = (end_date - start_date).days

    customers = [f"CUST_{i:04d}" for i in range(1, num_customers + 1)]
    transaction_types = ["POS", "Online", "Transfer", "ATM"]
    merchant_categories = ["Groceries", "Electronics", "Utilities", "Fashion", "Restaurants"]
    locations = ["Lagos", "Abuja", "Port Harcourt", "Ibadan", "Kano"]

    all_transactions = []

    for cust in customers:
        num_txns = np.random.randint(20, 80)  # smaller volume
        txn_times = sorted([
            start_date + timedelta(minutes=np.random.randint(0, num_days * 24 * 60))
            for _ in range(num_txns)
        ])

        for txn_time in txn_times:
            txn_type = random.choice(transaction_types)
            merchant_cat = random.choice(merchant_categories) if txn_type in ["POS", "Online"] else np.nan
            amount = np.random.uniform(10, 3000)
            declined = np.random.choice([0, 1], p=[0.95, 0.05])

            # Fraud logic
            fraud_prob = 0.02
            if txn_type == "Online" and amount > 1500:
                fraud_prob = 0.08
            elif txn_type == "Transfer" and amount > 2000:
                fraud_prob = 0.10
            elif declined == 1:
                fraud_prob = 0.15

            is_fraud = np.random.choice([0, 1], p=[1 - fraud_prob, fraud_prob])

            ord = {
                "transaction_id": str(uuid.uuid4())[:8],
                "customer_id": cust,
                "transaction_time": txn_time,
                "transaction_amount": round(amount, 2),
                "transaction_type": txn_type,
                "merchant_category": merchant_cat,
                "transaction_location": random.choice(locations),
                "is_declined": declined,
                "is_fraud": is_fraud
            }
            all_transactions.append(ord)

    df = pd.DataFrame(all_transactions).sort_values(by="transaction_time").reset_index(drop=True)
    return df


# --- Generate dataset ---
df = generate_synthetic_transactions()



