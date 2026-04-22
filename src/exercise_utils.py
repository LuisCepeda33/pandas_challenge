from pathlib import Path

import pandas as pd


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def raw_data_dir() -> Path:
    return project_root() / "data" / "raw"


def processed_data_dir() -> Path:
    return project_root() / "data" / "processed"


def ensure_processed_dir() -> Path:
    path = processed_data_dir()
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_processed_csv(df: pd.DataFrame, filename: str) -> Path:
    destination = ensure_processed_dir() / filename
    df.to_csv(destination, index=False)
    return destination
