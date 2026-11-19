"""12주차 성적 데이터 정제와 요약 분석."""

from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / "scores_2026.csv"
MINI_FILE = ROOT_DIR / "mini.csv"


def 정제(df: pd.DataFrame) -> pd.DataFrame:
    """명세한 규칙에 따라 점수 데이터를 정제하고 단계별 행 수를 출력한다."""
    required_columns = {"학번", "이름", "반", "과목", "점수"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        raise ValueError(f"필수 열이 없습니다: {sorted(missing_columns)}")

    cleaned = df.copy()
    cleaned["점수"] = pd.to_numeric(cleaned["점수"], errors="raise")

    # 점수가 비어 있는 행을 제외한다.
    cleaned = cleaned.dropna(subset=["점수"]).copy()
    print(f"점수 결측 제거 후: {len(cleaned)}행")

    # 모든 열이 같은 중복 행은 첫 행만 남긴다.
    cleaned = cleaned.drop_duplicates().copy()
    print(f"완전 중복 제거 후: {len(cleaned)}행")

    # 반과 과목의 앞뒤 공백을 제거한다.
    cleaned["반"] = cleaned["반"].str.strip()
    cleaned["과목"] = cleaned["과목"].str.strip()
    print(f"공백 정리 후: {len(cleaned)}행")

    # 유효한 점수 범위 밖의 행을 제외한다.
    cleaned = cleaned[cleaned["점수"].between(0, 100)].copy()
    print(f"점수 범위 정리 후: {len(cleaned)}행")
    return cleaned.reset_index(drop=True)


def 반별평균(df: pd.DataFrame) -> pd.Series:
    """반별 통계표를 출력하고 반별 평균 Series를 반환한다."""
    summary = df.groupby("반")["점수"].agg(
        개수="count",
        합계="sum",
        평균="mean",
        중앙값="median",
        최댓값="max",
    )
    summary[["평균", "중앙값"]] = summary[["평균", "중앙값"]].round(2)
    print(summary)
    return summary["평균"]


def 분석(df: pd.DataFrame) -> None:
    """정제 데이터의 필터·그룹 분석 결과를 출력한다."""
    math_rows = df[df["과목"] == "수학"]
    high_score_rows = df[(df["반"] == "1반") & (df["점수"] >= 90)]
    print(f"수학 행 수: {len(math_rows)}")
    print(f"1반 90점 이상 행 수: {len(high_score_rows)}")

    print("\n반별 점수 평균:")
    print(df.groupby("반")["점수"].mean().round(2))
    print("\n과목·반별 점수 평균:")
    print(df.groupby(["과목", "반"])["점수"].mean().round(2))
    print("\n반별 통계:")
    반별평균(df)


def main() -> None:
    raw_data = pd.read_csv(DATA_FILE, encoding="utf-8")
    cleaned_data = 정제(raw_data)
    분석(cleaned_data)


if __name__ == "__main__":
    main()
