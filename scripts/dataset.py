import os

import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("dataset.csv")  # <----update this name

temp_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
# test_size = 0.25 since temp_df is 80% of the original dataset
train_df, val_df = train_test_split(temp_df, test_size=0.25, random_state=42)

outputs = {
    "datasets/train.csv": train_df,
    "datasets/val.csv": val_df,
    "datasets/test.csv": test_df,
}
for path, df in outputs.items():
    os.makedirs(
        os.path.dirname(path), exist_ok=True
    )  # Make sure the directory exists before saving the file
    df.to_csv(path, index=False)

def export_dataset(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Exported dataset to {path}")

