import os
import sys
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from database import connect

def load_prompts():
    with connect() as conn:
        df = pd.read_sql("SELECT * FROM prompts", conn)

    return df

def split_dataset(df):
    temp_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    # test_size = 0.25 since temp_df is 80% of the original dataset
    train_df, val_df = train_test_split(temp_df, test_size=0.25, random_state=42)
    return train_df, test_df, val_df


def export_dataset(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Exported dataset to {path}")


if __name__ == "__main__":
    df = load_prompts()

    train_df, test_df, val_df = split_dataset(df)

    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    DATASETS_DIR = PROJECT_ROOT / "datasets"
    outputs = {
        DATASETS_DIR / "train.csv": train_df,
        DATASETS_DIR / "val.csv": val_df,
        DATASETS_DIR / "test.csv": test_df,
    }
    for path, dataset_df in outputs.items():
        export_dataset(dataset_df, path)
