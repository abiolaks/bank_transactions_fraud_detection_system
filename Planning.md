| Phase                                     | Deliverable                                                   | Tools                        |
| ----------------------------------------- | ------------------------------------------------------------- | ---------------------------- |
| **Phase 1: Offline model training**       | Generate synthetic dataset, train and evaluate XGBoost        | Python, scikit-learn, MLflow |
| **Phase 2: Real-time simulator + stream** | Kafka + Python producer                                       | Kafka, Python                |
| **Phase 3: Model serving**                | FastAPI service exposing `/predict`                           | FastAPI, joblib              |
| **Phase 4: Real-time scoring pipeline**   | Python consumer reading Kafka, calling FastAPI, writing to DB | Python, psycopg2             |
| **Phase 5: Streamlit dashboard**          | Displays alerts, labels, metrics                              | Streamlit                    |
| **Phase 6: Feedback & retraining**        | Export labels, retrain model                                  | Python, cron job             |





## Step-by-Step Feature Engineering Plan
### 1. Base Data (What We Already Have)

From the generation script, each record currently includes:

Column	Description
transaction_id	Unique ID for the transaction
customer_id	Customer identifier
transaction_time	Timestamp of transaction
transaction_amount	Transaction value
transaction_type	POS, Online, Transfer, etc.
merchant_category	Merchant type (may be NaN for transfers)
transaction_location	City where it occurred
is_declined	1 if declined, 0 if successful
is_fraud	Target label

That’s a good base, but not enough for an ML model.

### 2. Create Time-Derived Features

We’ll extract the following temporal patterns:

Feature	Description
transaction_hour	Hour of day (e.g., 0–23)
transaction_day_of_week	Day of week (0=Mon, 6=Sun)

Fraud patterns often vary by hour (e.g., midnight spikes).

### 3. Rolling Behavioral Features (per customer)

Using each customer’s historical transactions up to the current one, we compute:

Feature	Description
customer_num_txn_1d	Number of transactions in last 1 day
customer_num_txn_7d	Number of transactions in last 7 days
customer_avg_amount_7d	Average transaction amount in last 7 days
time_since_last_txn	Seconds since customer’s previous transaction
num_unique_locations_1h	Number of distinct locations in past 1 hour

These show spending frequency, intensity, and diversity — powerful indicators of abnormal behavior.

### 4. Account-Age Derived Feature
Feature	Description
customer_account_age_days	Days since customer’s first transaction

You can compute it easily by subtracting transaction_time from that customer’s earliest transaction date.

### 5. Combined Final Schema
Column	Type	Source
transaction_id	str	base
customer_id	str	base
transaction_time	datetime	base
transaction_amount	float	base
transaction_type	str	base
merchant_category	str	base
transaction_location	str	base
is_declined	int	base
transaction_hour	int	derived
transaction_day_of_week	int	derived
customer_num_txn_1d	int	rolling
customer_num_txn_7d	int	rolling
customer_avg_amount_7d	float	rolling
time_since_last_txn	float	rolling
num_unique_locations_1h	int	rolling
customer_account_age_days	int	derived
is_fraud	int	label