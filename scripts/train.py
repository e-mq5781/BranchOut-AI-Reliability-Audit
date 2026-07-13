import torch
from torch.optim import Adam

from dataset import build_dataloaders
from nn.layers import PromptClassifier
from nn.trainer import Trainer
from nn.losses import get_loss

if __name__ == "__main__":
    train_loader, val_loader, _ = build_dataloaders(
            "embeddings/prompts.npz"
    )

    model = PromptClassifier(
            input_size=1024,
            num_rubric_classes=19,
            dropout=0.2
    )

    criterion = get_loss("cross_entropy")

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

    trainer.fit(epochs=30, patience=5)
