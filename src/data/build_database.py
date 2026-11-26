
from pathlib import Path

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DATABASE_PATH = PROJECT_ROOT / "data" / "gamepulse.duckdb"

DATASETS = {
    "games_index": "games-index.csv",
    "ccu_daily": "ccu-daily-top2000.csv",
    "health_tiers": "health-tiers.csv",
}


def build_database() -> None:
    with duckdb.connect(str(DATABASE_PATH)) as conn:
        for table_name, filename in DATASETS.items():
            file_path = PROCESSED_DIR / filename

            if not file_path.exists():
                raise FileNotFoundError(file_path)

            conn.execute(
                f"""
                CREATE OR REPLACE TABLE {table_name} AS
                SELECT *
                FROM read_csv_auto(?, header = true)
                """,
                [str(file_path)],
            )

            row_count = conn.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            ).fetchone()[0]

            print(f"{table_name}: {row_count} rows")


if __name__ == "__main__":
    build_database()
