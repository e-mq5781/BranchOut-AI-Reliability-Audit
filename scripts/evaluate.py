import torch
from dataset import build_dataloaders
from nn.losses import get_loss
from tqdm.auto import tqdm

def get_test_loader(batch_size):
    _, _, test_loader = build_dataloaders("embeddings/prompts.npz", batch_size=batch_size)

    return test_loader

def evaluate(model, test_loader):
    model.eval()
    correct = 0
    total = 0
    total_loss = 0.0
    criterion = get_loss("cross_entropy")

    progress = tqdm(
        test_loader,
        desc="Evaluation",
        leave=False
    )
    with torch.no_grad():
        for input, label in progress:
            logits = model(input)

            loss = criterion(logits, label)
            total_loss += loss.item() * label.size(0) #in case the last_batch is less than 32 because drop_last=False by default

            predicted = logits.argmax(dim=1)
            total += label.size(0)
            correct += (predicted == label).sum().item()

            progress.set_postfix(
                loss=f"{loss.item():.4f}",
                acc=f"{correct / total:.3f}"
            )
    return (
        total_loss / total,
        correct / total
    )
