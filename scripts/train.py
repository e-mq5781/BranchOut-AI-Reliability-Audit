import torch
from torch import nn
from torch.optim import Adam

from dataset import build_dataloaders
from nn.layers import PromptClassifier
from nn.trainer import Trainer

if __name__ == "__main__":
    train_loader, val_loader = build_dataloaders(
            "embeddings/prompts.npz"
    )

    model = PromptClassifier(
            input_dim=1024,
            hidden_dim=512,
            num_classes=19
    )

    criterion = nn.CrossEntropyLoss()

    optimizer = Adam(
            model.parameters(),
            lr=1e-3,
    )

    trainer = Trainer(
        model=model,
        optimizer=optimizer,
        criterion=criterion,
        train_loader=train_loader,
        val_loader=val_loader,
        device="cuda" if torch.cuda.is_available() else "cpu",
    )

    trainer.fit(epochs=30)
