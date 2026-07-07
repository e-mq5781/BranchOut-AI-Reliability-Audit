import sys
from pathlib import Path

# Navigate up two levels (from 'ingest' to 'scripts') to find the 'database' folder
scripts_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(scripts_dir))

import os

import pandas as pd
from database.db import connect
from sklearn.model_selection import train_test_split

with connect() as conn:
    df = pd.read_sql("SELECT * FROM prompts", conn)

temp_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
# test_size = 0.25 since temp_df is 80% of the original dataset
train_df, val_df = train_test_split(temp_df, test_size=0.25, random_state=42)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATASETS_DIR = PROJECT_ROOT / "datasets"
outputs = {
    DATASETS_DIR / "train.csv": train_df,
    DATASETS_DIR / "val.csv": val_df,
    DATASETS_DIR / "test.csv": test_df,
}
for path, dataset_df in outputs.items():
    os.makedirs(
        os.path.dirname(path), exist_ok=True
    )  # Make sure the directory exists before saving the file
    dataset_df.to_csv(path, index=False)


def export_dataset(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Exported dataset to {path}")
