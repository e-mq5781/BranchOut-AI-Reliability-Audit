import random

import numpy as np
import torch

# Set essentially every single random thing to use the seed that i can think of
def set_seed(seed: int) -> None:
    random.seed(seed) # python random library
    np.random.seed(seed) # numpy
    torch.manual_seed(seed) # pytorch
    torch.cuda.manual_seed_all(seed) # nvidia pytorch
    torch.backends.cudnn.deterministic = True # make it actually use the seed
    torch.backends.cudnn.benchmark = False # don't find and cache best convolution algos for determinism bc it can change
