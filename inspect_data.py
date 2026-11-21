
import csv
from pathlib import Path

from datetime import datetime
from collections import defaultdict


DATA_DIR = Path(__file__).resolve().parent / "data" / "raw"

FILES = [
    "games-index.csv",
    "ccu-daily-top2000.csv",
    "health-tiers.csv",
]

UNIQUE_APP_ID_FILES = {
    "games-index.csv",
    "health-tiers.csv",
}



def inspect_csv(file_path: Path):
    print(f"\n{'=' * 50}")
    print(f"File: {file_path.name}")
    print("=" * 50)

    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        print("Columns:", reader.fieldnames)

        row_count = 0
        missing_counts = {}
        seen_app_ids = set()
        duplicate_app_ids = set()

        for column in reader.fieldnames:
            missing_counts[column] = 0

        for row in reader:
            row_count += 1

            if row_count <= 3:
                print(f"Sample {row_count}:", row)

            # Check missing values
            for column in reader.fieldnames:
                if row.get(column) is None or not row[column].strip():
                    missing_counts[column] += 1

            # Check duplicate app_id
            if file_path.name in UNIQUE_APP_ID_FILES:
                app_id = row["app_id"]

                if app_id in seen_app_ids:
                    duplicate_app_ids.add(app_id)
                else:
                    seen_app_ids.add(app_id)

        print("Total rows:", row_count)

        print("\nMissing Values:")
        for column, count in missing_counts.items():
            print(f"  {column}: {count}")

        if file_path.name in UNIQUE_APP_ID_FILES:
            print("\nDuplicate app_id count:", len(duplicate_app_ids))

            if duplicate_app_ids:
                print("Duplicate app_id samples:",
                      list(duplicate_app_ids)[:10])



def inspect_relationships():
    print(f"\n{'=' * 50}")
    print("Relationship Check")
    print("=" * 50)

    def load_app_ids(filename):
        file_path = DATA_DIR / filename

        with file_path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            return {row["app_id"] for row in reader}

    games_ids = load_app_ids("games-index.csv")
    health_ids = load_app_ids("health-tiers.csv")

    games_file = DATA_DIR / "games-index.csv"

    with games_file.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        missing_tier_ids = {
            row["app_id"]
            for row in reader
            if not row["health_tier"].strip()
        }

    matched_ids = games_ids & health_ids
    only_in_games = games_ids - health_ids
    only_in_health = health_ids - games_ids

    print("Games index app_ids:", len(games_ids))
    print("Health tiers app_ids:", len(health_ids))
    print("Matched app_ids:", len(matched_ids))
    print("Only in games-index:", len(only_in_games))
    print("Only in health-tiers:", len(only_in_health))

    if only_in_games:
        print("Games-only samples:", list(only_in_games)[:10])

    if only_in_health:
        print("Health-only samples:", list(only_in_health)[:10])

    print("Missing health_tier IDs:", len(missing_tier_ids))
    print(
        "Missing tier IDs match games-only IDs:",
        missing_tier_ids == only_in_games
    )


def inspect_ccu_data():
    file_path = DATA_DIR / "ccu-daily-top2000.csv"

    print(f"\n{'=' * 50}")
    print("CCU Data Check")
    print("=" * 50)

    dates = []
    seen_keys = set()
    duplicate_keys = set()
    duplicate_rows = 0
    invalid_dates = 0

    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            app_id = row["app_id"]
            date_str = row["date"]

            # Check date format
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                dates.append(date_str)
            except ValueError:
                invalid_dates += 1

            # Check duplicate composite keys
            key = (app_id, date_str)

            if key in seen_keys:
                duplicate_keys.add(key)
                duplicate_rows += 1
            else:
                seen_keys.add(key)

    print("Earliest date:", min(dates) if dates else "N/A")
    print("Latest date:", max(dates) if dates else "N/A")
    print("Invalid date count:", invalid_dates)
    print("Duplicate (app_id, date) combinations:", len(duplicate_keys))
    print("Duplicate rows:", duplicate_rows)

    if duplicate_keys:
        print("Duplicate key samples:", list(duplicate_keys)[:10])


def investigate_current_players():
    file_path = DATA_DIR / "health-tiers.csv"

    print(f"\n{'=' * 50}")
    print("Current Players Missing Value Investigation")
    print("=" * 50)

    tier_stats = defaultdict(lambda: {
        "total": 0,
        "missing": 0,
        "present": 0,
    })

    missing_samples = []
    present_samples = []

    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            tier = row["tier"]
            current_players = row["current_players"].strip()

            tier_stats[tier]["total"] += 1

            if not current_players:
                tier_stats[tier]["missing"] += 1

                if len(missing_samples) < 5:
                    missing_samples.append(row)
            else:
                tier_stats[tier]["present"] += 1

                if len(present_samples) < 5:
                    present_samples.append(row)

    for tier, stats in sorted(tier_stats.items()):
        missing_rate = stats["missing"] / stats["total"] * 100

        print(f"\nTier: {tier}")
        print("  Total:", stats["total"])
        print("  Missing:", stats["missing"])
        print("  Present:", stats["present"])
        print(f"  Missing rate: {missing_rate:.2f}%")

    print("\nMissing Samples:")
    for row in missing_samples:
        print(row)

    print("\nPresent Samples:")
    for row in present_samples:
        print(row)


def investigate_release_date():
    file_path = DATA_DIR / "games-index.csv"

    print(f"\n{'=' * 50}")
    print("Release Date Missing Value Investigation")
    print("=" * 50)

    missing_count = 0
    samples = []

    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if not row["release_date"].strip():
                missing_count += 1

                if len(samples) < 10:
                    samples.append(row)

    print("Missing release_date:", missing_count)

    print("\nMissing Samples:")
    for row in samples:
        print(row)


def investigate_release_date():
    file_path = DATA_DIR / "games-index.csv"
    ccu_path = DATA_DIR / "ccu-daily-top2000.csv"

    print(f"\n{'=' * 50}")
    print("Release Date Missing Value Investigation")
    print("=" * 50)

    tier_stats = defaultdict(int)
    free_stats = defaultdict(int)
    missing_app_ids = set()

    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if not row["release_date"].strip():
                missing_app_ids.add(row["app_id"])
                tier_stats[row["health_tier"]] += 1
                free_stats[row["is_free"]] += 1

    ccu_app_ids = set()

    with ccu_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            ccu_app_ids.add(row["app_id"])

    matched_ccu = missing_app_ids & ccu_app_ids

    print("Missing release_date:", len(missing_app_ids))

    print("\nBy health_tier:")
    for tier, count in sorted(tier_stats.items()):
        print(f"  {tier}: {count}")

    print("\nBy is_free:")
    for is_free, count in sorted(free_stats.items()):
        print(f"  {is_free}: {count}")

    print("\nCCU Coverage:")
    print("  Matched games:", len(matched_ccu))
    print("  Not found in CCU:", len(missing_app_ids - ccu_app_ids))


def main():
    for filename in FILES:
        file_path = DATA_DIR / filename

        if not file_path.exists():
            print(f"[Missing] {filename}")
            continue


        inspect_csv(file_path)

    inspect_relationships()
    inspect_ccu_data()
    investigate_current_players()
    investigate_release_date()
    investigate_release_date()

if __name__ == "__main__":
    main()
