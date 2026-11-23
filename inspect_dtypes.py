
from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).parent / "data" / "raw"

FILES = [
    "games-index.csv",
    "ccu-daily-top2000.csv",
    "health-tiers.csv",
]


def inspect_dtypes(filename: str) -> None:
    # Load CSV data
    file_path = DATA_DIR / filename
    df = pd.read_csv(file_path)

    print(f"\n{'=' * 60}")
    print(f"Dataset: {filename}")
    print("=" * 60)

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nSample data:")
    print(df.head(3).to_string(index=False))


def main() -> None:
    for filename in FILES:
        inspect_dtypes(filename)
    df = pd.read_csv(DATA_DIR / "health-tiers.csv")

    values = df["current_players"].dropna()

    print("\ncurrent_players value validation:")
    print("Non-integer values:", (values % 1 != 0).sum())
    print("Negative values:", (values < 0).sum())
    print("Minimum:", values.min())
    print("Maximum:", values.max())


if __name__ == "__main__":
    main()
