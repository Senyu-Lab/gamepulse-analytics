
from pathlib import Path

import pandas as pd

from src.data.preprocessing import (
    export_processed_datasets,
    load_all_datasets,
)


PROJECT_ROOT = Path(__file__).resolve().parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

EXPECTED_ROWS = {
    "games-index.csv": 85041,
    "ccu-daily-top2000.csv": 193981,
    "health-tiers.csv": 85020,
}


def verify_processed_datasets() -> None:
    # Verify exported CSV files
    for filename, expected_count in EXPECTED_ROWS.items():
        file_path = PROCESSED_DIR / filename
        df = pd.read_csv(file_path)

        print(f"\n{'=' * 50}")
        print(f"Verifying: {filename}")
        print("=" * 50)

        print("Rows:", len(df))
        print("Expected rows:", expected_count)
        print("Row count correct:", len(df) == expected_count)
        print("Columns:", df.columns.tolist())
        print("Missing values:")
        print(df.isna().sum())

        assert len(df) == expected_count, (
            f"Unexpected row count in {filename}"
        )


def inspect_loaded_datasets() -> None:
    # Inspect preprocessed DataFrames
    datasets = load_all_datasets()

    for name, df in datasets.items():
        print(f"\n{'=' * 50}")
        print(f"Dataset: {name}")
        print("=" * 50)

        print("Shape:", df.shape)
        print("\nData types:")
        print(df.dtypes)
        print("\nMissing values:")
        print(df.isna().sum())


def main() -> None:
    export_processed_datasets()
    verify_processed_datasets()
    inspect_loaded_datasets()


if __name__ == "__main__":
    main()
