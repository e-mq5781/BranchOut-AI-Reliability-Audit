import torch
from dataset import build_dataloaders

def get_test_loader():
    _, _, test_loader = build_dataloaders("embeddings/prompts.npy", batch_size=32)

    return test_loader

def evaluate(model, test_loader):
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for input, label in test_loader:
            outputs = model(input)
            _, predicted = torch.max(outputs, 1)
            total += label.size(0)
            correct += (predicted == label).sum().item()
    return correct/total
