import torch

# Returns best available torch device
def get_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")

    return torch.device("cpu")

# this did not need to be its own file, but i thought there might be more code, but ig not, and i'm too lazy to make it not be its own file
