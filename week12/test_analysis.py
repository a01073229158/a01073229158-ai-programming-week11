from pathlib import Path

import pandas as pd

from analysis import 정제


ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA = pd.read_csv(ROOT_DIR / "scores_2026.csv", encoding="utf-8")
MINI_DATA = pd.read_csv(ROOT_DIR / "mini.csv", encoding="utf-8")


def test_cleaned_data_has_100_rows() -> None:
    assert len(정제(RAW_DATA)) == 100


def test_cleaned_class_names_are_expected() -> None:
    cleaned = 정제(RAW_DATA)
    assert set(cleaned["반"].unique()) == {"1반", "2반"}


def test_grouped_score_sum_matches_total() -> None:
    cleaned = 정제(RAW_DATA)
    grouped_sum = cleaned.groupby("반")["점수"].sum().sum()
    assert grouped_sum == cleaned["점수"].sum()


def test_mini_class_one_average_is_80() -> None:
    cleaned = 정제(MINI_DATA)
    class_one_average = cleaned.loc[cleaned["반"] == "1반", "점수"].mean()
    assert class_one_average == 80.0
