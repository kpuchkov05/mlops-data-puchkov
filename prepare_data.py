from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.datasets import load_iris, load_wine


DATA_DIR = Path("data")
CSV_OPTIONS = {"index": False, "lineterminator": "\n", "float_format": "%.10g"}


def sorted_frame(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.sort_values(list(frame.columns), kind="mergesort").reset_index(drop=True)


def save_frame(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, **CSV_OPTIONS)


def prepare_base() -> None:
    iris = sorted_frame(load_iris(as_frame=True).frame)
    save_frame(iris, DATA_DIR / "iris.csv")
    wine_path = DATA_DIR / "wine.csv"
    if wine_path.exists():
        wine_path.unlink()


def prepare_wine() -> None:
    wine = sorted_frame(load_wine(as_frame=True).frame)
    save_frame(wine, DATA_DIR / "wine.csv")


def prepare_iris_features() -> None:
    iris = sorted_frame(load_iris(as_frame=True).frame)
    iris["sepal_area"] = iris["sepal length (cm)"] * iris["sepal width (cm)"]
    iris["petal_area"] = iris["petal length (cm)"] * iris["petal width (cm)"]
    save_frame(iris, DATA_DIR / "iris.csv")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["base", "wine", "iris_features"])
    args = parser.parse_args()

    actions = {
        "base": prepare_base,
        "wine": prepare_wine,
        "iris_features": prepare_iris_features,
    }
    actions[args.mode]()


if __name__ == "__main__":
    main()
