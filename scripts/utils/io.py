import json
from pathlib import Path

import torch

def save_json(data, filename: Path):
    filename.parent.mkdir(parents=True, exist_ok=True)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_json(filename: Path):
    with open(filename) as f:
            return json.load(f)

def save_checkpoint(model, optimizer, epoch, filename):
    filename.parent.mkdir(parents=True, exist_ok=True)

    torch.save(
        {
            "epoch": epoch,
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
        },
        filename,
    )

def load_checkpoint(model, optimizer, filename):
    checkpoint = torch.load(filename)
    model.load_state_dict(checkpoint["model"])
    optimizer.load_state_dict(checkpoint["optimizer"])
    return checkpoint["epoch"]
