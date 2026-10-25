from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import pandas as pd
from sklearn.datasets import load_iris, load_wine


DATA_DIR = Path("data")
IRIS_COLUMNS = list(load_iris(as_frame=True).frame.columns)
WINE_COLUMNS = list(load_wine(as_frame=True).frame.columns)
FEATURE_COLUMNS = ["sepal_area", "petal_area"]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_common(path: Path, frame: pd.DataFrame, rows: int) -> None:
    if any(str(column).startswith("Unnamed:") for column in frame.columns):
        raise ValueError(f"{path}: обнаружен безымянный столбец индекса")
    if len(frame) != rows:
        raise ValueError(f"{path}: ожидалось {rows} строк, получено {len(frame)}")
    if frame.isna().sum().sum() != 0:
        raise ValueError(f"{path}: обнаружены пропущенные значения")


def validate_iris(path: Path, frame: pd.DataFrame) -> None:
    validate_common(path, frame, 150)
    valid_columns = [IRIS_COLUMNS, IRIS_COLUMNS + FEATURE_COLUMNS]
    if list(frame.columns) not in valid_columns:
        raise ValueError(f"{path}: неправильный набор или порядок столбцов")
    if FEATURE_COLUMNS[0] in frame.columns:
        expected_sepal = frame["sepal length (cm)"] * frame["sepal width (cm)"]
        expected_petal = frame["petal length (cm)"] * frame["petal width (cm)"]
        if not (frame["sepal_area"] - expected_sepal).abs().le(1e-9).all():
            raise ValueError(f"{path}: неправильные значения sepal_area")
        if not (frame["petal_area"] - expected_petal).abs().le(1e-9).all():
            raise ValueError(f"{path}: неправильные значения petal_area")
    sorted_copy = frame.sort_values(IRIS_COLUMNS, kind="mergesort").reset_index(drop=True)
    if not frame.equals(sorted_copy):
        raise ValueError(f"{path}: строки не отсортированы детерминированно")


def validate_wine(path: Path, frame: pd.DataFrame) -> None:
    validate_common(path, frame, 178)
    if list(frame.columns) != WINE_COLUMNS:
        raise ValueError(f"{path}: неправильный набор или порядок столбцов")
    sorted_copy = frame.sort_values(WINE_COLUMNS, kind="mergesort").reset_index(drop=True)
    if not frame.equals(sorted_copy):
        raise ValueError(f"{path}: строки не отсортированы детерминированно")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expect", choices=["iris", "both"], default="both")
    args = parser.parse_args()

    expected = {"iris.csv"} if args.expect == "iris" else {"iris.csv", "wine.csv"}
    actual = {path.name for path in DATA_DIR.glob("*.csv")} if DATA_DIR.exists() else set()
    if actual != expected:
        raise FileNotFoundError(f"ожидались {sorted(expected)}, найдены {sorted(actual)}")

    for path in sorted(DATA_DIR.glob("*.csv")):
        frame = pd.read_csv(path)
        if path.name == "iris.csv":
            validate_iris(path, frame)
        elif path.name == "wine.csv":
            validate_wine(path, frame)
        print(
            f"{path.as_posix()} | sha256={sha256_file(path)} | "
            f"rows={len(frame)} | columns={len(frame.columns)} | "
            f"names={list(frame.columns)} | missing={int(frame.isna().sum().sum())}"
        )


if __name__ == "__main__":
    main()
