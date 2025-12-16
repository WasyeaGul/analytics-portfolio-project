"""
02_pandas_numpy_analysis.py
Beginner-friendly pandas + NumPy script.

What it does:
- Loads a CSV dataset
- Cleans basic issues (duplicates, column names)
- Creates a few simple credit-risk features
- Saves a new CSV you can use later in Power BI / Tableau
"""

from __future__ import annotations

import os
import numpy as np
import pandas as pd

# Change this if your CSV has a different name
DATA_PATH = os.path.join("data", "credit_card_default.csv")

# Change this if your target column has a different name
TARGET_COL = "default_payment_next_month"


def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Could not find the CSV at: {path}\n"
            "Put the dataset CSV inside the /data folder (or update DATA_PATH)."
        )
    return pd.read_csv(path)


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    return df


def clean_basic(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop_duplicates()
    return df


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    bill_cols = [c for c in df.columns if c.startswith("bill_amt")]
    pay_cols = [c for c in df.columns if c.startswith("pay_amt")]

    # Total + average bills
    if bill_cols:
        df["bill_total_6m"] = df[bill_cols].sum(axis=1)
        df["bill_avg_6m"] = df[bill_cols].mean(axis=1)

    # Total + average payments
    if pay_cols:
        df["pay_total_6m"] = df[pay_cols].sum(axis=1)
        df["pay_avg_6m"] = df[pay_cols].mean(axis=1)

    # Payment-to-bill ratio (avoid dividing by zero)
    if bill_cols and pay_cols:
        denom = np.where(df["bill_total_6m"].values == 0, np.nan, df["bill_total_6m"].values)
        df["pay_to_bill_ratio"] = df["pay_total_6m"].values / denom
        df["pay_to_bill_ratio"] = df["pay_to_bill_ratio"].clip(lower=0, upper=10)

    # Simple utilization: most recent bill / limit
    if "limit_bal" in df.columns and bill_cols:
        latest_bill = df[bill_cols[0]]  # usually BILL_AMT1 is most recent
        denom = np.where(df["limit_bal"].values == 0, np.nan, df["limit_bal"].values)
        df["utilization_recent"] = latest_bill.values / denom
        df["utilization_recent"] = df["utilization_recent"].clip(lower=0, upper=10)

    # Delinquency flag based on repayment status columns (PAY_0, PAY_2..PAY_6)
    pay_status_cols = [c for c in df.columns if c.startswith("pay_") and c.replace("pay_", "").isdigit()]
    if pay_status_cols:
        df["max_repayment_status"] = df[pay_status_cols].max(axis=1)
        df["any_delinquency_flag"] = (df["max_repayment_status"] > 0).astype(int)

    return df


def missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    ms = pd.DataFrame(
        {
            "missing_count": df.isna().sum(),
            "missing_pct": (df.isna().mean() * 100).round(2),
        }
    ).sort_values("missing_count", ascending=False)
    return ms


def main() -> None:
    df = load_data(DATA_PATH)
    df = standardize_columns(df)
    df = clean_basic(df)

    target = TARGET_COL.lower()
    if target not in df.columns:
        print("Target column not found.")
        print("Here are the columns I see:")
        print(df.columns.tolist())
        print("Update TARGET_COL in the script to match your dataset.")
    else:
        print(f"Target column found: {target}")

    df_feat = create_features(df)

    print("\nData shape (rows, columns):")
    print(df_feat.shape)

    print("\nMissing values (top 15 columns):")
    print(missing_summary(df_feat).head(15))

    feature_cols = [
        "bill_total_6m",
        "pay_total_6m",
        "pay_to_bill_ratio",
        "utilization_recent",
        "max_repayment_status",
        "any_delinquency_flag",
    ]
    feature_cols = [c for c in feature_cols if c in df_feat.columns]

    if feature_cols:
        print("\nFeature preview (first 10 rows):")
        print(df_feat[feature_cols].head(10))

    out_path = os.path.join("data", "credit_card_default_features.csv")
    df_feat.to_csv(out_path, index=False)
    print(f"\nSaved engineered dataset to: {out_path}")


if __name__ == "__main__":
    main()
