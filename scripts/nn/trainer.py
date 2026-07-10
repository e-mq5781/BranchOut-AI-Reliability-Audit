import torch
from tqdm.auto import tqdm
from pathlib import Path

class Trainer:
    def __init__(
            self,
            model,
            optimizer,
            criterion,
            train_loader,
            val_loader,
            device,
    ):
        self.model = model.to(device)
        self.optimizer = optimizer
        self.criterion = criterion

        self.train_loader = train_loader
        self.val_loader = val_loader
        
        self.device = device

    def train_epoch(self):
        self.model.train()

        total_loss = 0.0
        correct = 0
        total = 0

        progress = tqdm(
                self.train_loader,
                desc="Training",
                leave=False,
        )

        for x, y in progress:
            x = x.to(self.device)
            y = y.to(self.device)

            self.optimizer.zero_grad()

            logits = self.model(x)

            loss = self.criterion(logits, y)

            loss.backward()

            self.optimizer.step()

            total_loss += loss.item()

            predictions = logits.argmax(dim=1)

            correct += (predictions == y).sum().item()
            total += y.size(0)

            progress.set_postfix(
                    loss=f"{loss.item():.4f}",
                    acc=f"{correct / total:.3f}",
            )

        return (
                total_loss / len(self.train_loader),
                correct / total,
        )

    @torch.no_grad()
    def validate(self):
        self.model.eval()
        
        total_loss = 0.0
        correct = 0
        total = 0
         
        progress = tqdm(
                self.val_loader,
                desc="Validation",
                leave=False,
        )

        for x, y in progress:

            x = x.to(self.device)
            y = y.to(self.device)

            logits = self.model(x)

            loss = self.criterion(logits, y)

            total_loss += loss.item()

            predictions = logits.argmax(dim=1)

            correct += (predictions == y).sum().item()
            total += y.size(0)

            progress.set_postfix(
                    loss=f"{loss.item():.4f}",
                    acc=f"{correct / total:.3f}",
            )

        return (
            total_loss / len(self.val_loader),
            correct / total,
        )

    def fit(self, epochs):
        best_acc = 0.0

        epoch_bar = tqdm(range(epochs), desc="Epochs")

        for _ in epoch_bar:
            train_loss, train_acc = self.train_epoch()
            val_loss, val_acc = self.validate()

            if val_acc > best_acc:
                best_acc = val_acc
                self.save_checkpoint("checkpoints/best.pt")


            epoch_bar.set_postfix(
            train_loss=f"{train_loss:.4f}",
            train_acc=f"{train_acc:.3f}",
            val_loss=f"{val_loss:.4f}",
            val_acc=f"{val_acc:.3f}",
)

    def save_checkpoint(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        torch.save(
                self.model.state_dict(),
                path,
        )
