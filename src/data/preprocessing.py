
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_games_index() -> pd.DataFrame:
    # Load game metadata
    file_path = RAW_DATA_DIR / "games-index.csv"
    df = pd.read_csv(file_path)

    # Convert column types
    df["app_id"] = df["app_id"].astype("Int64")
    df["name"] = df["name"].astype("string")
    df["slug"] = df["slug"].astype("string")
    df["release_date"] = pd.to_datetime(
        df["release_date"],
        errors="coerce",
    )
    df["is_free"] = df["is_free"].astype("boolean")
    df["total_positive"] = df["total_positive"].astype("Int64")
    df["total_negative"] = df["total_negative"].astype("Int64")
    df["health_tier"] = df["health_tier"].astype("string")

    return df


def load_ccu_data() -> pd.DataFrame:
    # Load daily concurrent player data
    file_path = RAW_DATA_DIR / "ccu-daily-top2000.csv"
    df = pd.read_csv(file_path)

    # Convert column types
    df["app_id"] = df["app_id"].astype("Int64")
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
    )
    df["max_players"] = df["max_players"].astype("Int64")

    return df


def load_health_tiers() -> pd.DataFrame:
    # Load game health tier data
    file_path = RAW_DATA_DIR / "health-tiers.csv"
    df = pd.read_csv(file_path)

    # Convert column types
    df["app_id"] = df["app_id"].astype("Int64")
    df["slug"] = df["slug"].astype("string")
    df["tier"] = df["tier"].astype("string")
    df["current_players"] = df["current_players"].astype("Int64")

    return df


def load_all_datasets() -> dict[str, pd.DataFrame]:
    # Load all datasets
    return {
        "games_index": load_games_index(),
        "ccu_data": load_ccu_data(),
        "health_tiers": load_health_tiers(),
    }
