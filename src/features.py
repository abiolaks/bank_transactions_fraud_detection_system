import pandas as pd


def engineer_features(df):
    df = df.copy()

    # Ensure time is datetime
    df["transaction_time"] = pd.to_datetime(df["transaction_time"])

    # Sort by customer and time
    df = df.sort_values(["customer_id", "transaction_time"])

    # Basic time-based features
    df["transaction_hour"] = df["transaction_time"].dt.hour
    df["transaction_day_of_week"] = df["transaction_time"].dt.weekday

    # Initialize rolling features
    df["customer_num_txn_1d"] = 0
    df["customer_num_txn_7d"] = 0
    df["customer_avg_amount_7d"] = 0.0
    df["time_since_last_txn"] = 0.0
    df["num_unique_locations_1h"] = 0
    df["customer_account_age_days"] = 0

    # Process per customer
    for cust_id, group in df.groupby("customer_id"):
        group = group.sort_values("transaction_time")

        for i, row in group.iterrows():
            t = row["transaction_time"]

            past_1d = group[
                (group["transaction_time"] < t)
                & (group["transaction_time"] >= t - pd.Timedelta(days=1))
            ]
            past_7d = group[
                (group["transaction_time"] < t)
                & (group["transaction_time"] >= t - pd.Timedelta(days=7))
            ]
            past_1h = group[
                (group["transaction_time"] < t)
                & (group["transaction_time"] >= t - pd.Timedelta(hours=1))
            ]

            df.at[i, "customer_num_txn_1d"] = len(past_1d)
            df.at[i, "customer_num_txn_7d"] = len(past_7d)
            df.at[i, "customer_avg_amount_7d"] = (
                past_7d["transaction_amount"].mean() if not past_7d.empty else 0
            )
            df.at[i, "time_since_last_txn"] = (
                (t - past_7d["transaction_time"].max()).total_seconds() / 60
                if not past_7d.empty
                else 0
            )
            df.at[i, "num_unique_locations_1h"] = past_1h[
                "transaction_location"
            ].nunique()
            df.at[i, "customer_account_age_days"] = (
                t - group["transaction_time"].min()
            ).days

    return df


# Example u


def main():
    """
    This function contains the main logic of the program.
    """
    df = pd.read_csv("../data/raw/base_bank_transactions.csv")
    df_feat = engineer_features(df)
    df_feat.to_csv("../data/interim/engineered_bank_transactions.csv", index=False)


if __name__ == "__main__":
    main()
