import torch

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

        for x, y in self.train_loader:
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

        for x, y in self.val_loader:

            x = x.to(self.device)
            y = y.to(self.device)

            logits = self.model(x)

            loss = self.criterion(logits, y)

            total_loss += loss.item()

            predictions = logits.argmax(dim=1)

            correct += (predictions == y).sum().item()
            total += y.size(0)

        return (
            total_loss / len(self.val_loader),
            correct / total,
        )

    def fit(self, epochs):
        best_acc = 0.0

        for epoch in range(epochs):
            train_loss, train_acc = self.train_epoch()
            val_loss, val_acc = self.validate()

            if val_acc > best_acc:
                best_acc = val_acc
                self.save_checkpoint("checkpoints/best.pt")

            print(
                    f"Epoch {epoch+1:3d}  | "
                    f"Train Loss {train_loss:.4f} "
                    f"Train Acc {train_acc:.3f} | "
                    f"Val Loss {val_loss:.4f} "
                    f"Val Acc {val_acc:.3f}"
            )

    def save_checkpoint(self, path):
        torch.save(
                self.model.state_dict(),
                path,
        )
