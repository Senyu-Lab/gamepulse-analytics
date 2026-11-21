
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data" / "raw"

FILES = [
    "games-index.csv",
    "ccu-daily-top2000.csv",
    "health-tiers.csv",
]


def inspect_csv(file_path: Path):
    print(f"\n{'=' * 50}")
    print(f"File: {file_path.name}")
    print("=" * 50)

    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        print("Columns:", reader.fieldnames)

        row_count = 0
        for row in reader:
            row_count += 1
            if row_count <= 3:
                print(f"Sample {row_count}:", row)

        print("Total rows:", row_count)


def main():
    for filename in FILES:
        file_path = DATA_DIR / filename

        if not file_path.exists():
            print(f"[Missing] {filename}")
            continue

        inspect_csv(file_path)


if __name__ == "__main__":
    main()
