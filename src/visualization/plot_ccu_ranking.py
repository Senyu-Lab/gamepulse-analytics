from pathlib import Path

import duckdb
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "data" / "gamepulse.duckdb"
SQL_PATH = PROJECT_ROOT / "src" / "analysis" / "ccu_ranking.sql"
OUTPUT_PATH = PROJECT_ROOT / "docs" / "images" / "ccu-ranking.png"


def plot_ccu_ranking() -> None:
    sql = SQL_PATH.read_text(encoding="utf-8")

    with duckdb.connect(str(DATABASE_PATH), read_only=True) as conn:
        df = conn.execute(sql).fetchdf()

    df = df.sort_values("peak_ccu")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(11, 6))

    ax.barh(df["name"], df["peak_ccu"])
    ax.set_title("Top 10 Games by Peak CCU")
    ax.set_xlabel("Peak concurrent players")
    ax.set_ylabel("Game")
    ax.ticklabel_format(
        axis="x",
        style="plain",
    )

    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=150)
    plt.close(fig)

    print(f"Chart saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    plot_ccu_ranking()