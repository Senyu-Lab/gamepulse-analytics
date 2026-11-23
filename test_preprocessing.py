
from src.data.preprocessing import load_all_datasets


def main():
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

        print("\nSample:")
        print(df.head(3).to_string(index=False))


if __name__ == "__main__":
    main()
