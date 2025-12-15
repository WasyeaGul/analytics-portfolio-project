"""
Banking Credit Risk Analytics
Goal: Explore and model probability of default (PD) using customer attributes.

How to run (later):
1) Download UCI Credit Card Default dataset
2) Save as: data/credit_card_default.csv
3) Run: python src/01_credit_risk_analysis.py
"""

import pandas as pd

DATA_PATH = "data/credit_card_default.csv"
TARGET_COL = "default_payment_next_month"

def main():
    print("=== Banking Credit Risk Analytics ===")
    print("Dataset: UCI Credit Card Default")

    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print(f"\nData file not found: {DATA_PATH}")
        print("Download the dataset and save it with that name, then rerun.\n")
        return

    print("\nShape:", df.shape)
    print("\nColumns:\n", df.columns)

    # Basic target rate
    if TARGET_COL in df.columns:
        default_rate = df[TARGET_COL].mean()
        print(f"\nOverall default rate: {default_rate:.2%}")

        # Quick segmentation examples (adjust column names if needed)
        for col in ["education", "marriage", "age"]:
            if col in df.columns:
                print(f"\nDefault rate by {col}:")
                print(df.groupby(col)[TARGET_COL].mean().sort_values(ascending=False).head(10))

    print("\nDone.")

if __name__ == "__main__":
    main()
