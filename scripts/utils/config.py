from pathlib import Path

# Set up directories
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_DIR = PROJECT_ROOT / "database"
DATASET_DIR = PROJECT_ROOT / "datasets"
MODEL_DIR = PROJECT_ROOT / "models"
CHECKPOINT_DIR = PROJECT_ROOT / "checkpoints"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

DATABASE_PATH = DATASET_DIR / "prompts.db"


# Embedding model stuff
#TODO: find a good embedding model here, set EMBEDDING_MODEL and EMBEDDING_SIZE


# Neureal network configs
MODEL_EMBEDDING_SIZE = 64
HIDDEN_SIZE = 512
NUM_OUTPUTS = 19
DROPOUT = 0.2

# Training configs
LEARNING_RATE = 1e-4
WEIGHT_DECAY = 1e-5
BATCH_SIZE = 32
EPOCHS = 100
TRAIN_SPLIT = 0.80
VALIDATION_SPLIT = 0.10
TEST_SPLIT = 0.10
RANDOM_SEED = 42
