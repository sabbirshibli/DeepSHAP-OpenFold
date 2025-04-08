import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import json
from Bio import SeqIO
from sklearn.model_selection import train_test_split

AA_LIST = 'ACDEFGHIKLMNPQRSTVWY'

def one_hot_encode(seq):
    aa_dict = {aa: i for i, aa in enumerate(AA_LIST)}
    encoding = np.zeros((len(seq), len(AA_LIST)))
    for i, aa in enumerate(seq):
        if aa in aa_dict:
            encoding[i, aa_dict[aa]] = 1
    return encoding

class MLP(nn.Module):
    def __init__(self, input_dim):
        super(MLP, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)

def train():
    record = next(SeqIO.parse("data/protein.fasta", "fasta"))
    sequence = str(record.seq)
    inputs = one_hot_encode(sequence)

    with open("data/openfold_output.json") as f:
        data = json.load(f)
        plddt = np.array(data["plddt"])

    if len(plddt) != len(sequence):
        raise ValueError(f"Length mismatch: {len(plddt)} pLDDT vs {len(sequence)} residues.")

    X_train, X_val, y_train, y_val = train_test_split(inputs, plddt, test_size=0.2, random_state=42)

    model = MLP(input_dim=20)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    X_train = torch.tensor(X_train, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.float32)
    X_val = torch.tensor(X_val, dtype=torch.float32)
    y_val = torch.tensor(y_val, dtype=torch.float32)

    for epoch in range(100):
        model.train()
        optimizer.zero_grad()
        output = model(X_train)
        loss = criterion(output, y_train)
        loss.backward()
        optimizer.step()

        if epoch % 10 == 0:
            model.eval()
            val_loss = criterion(model(X_val), y_val).item()
            print(f"Epoch {epoch}: Train Loss = {loss.item():.4f}, Val Loss = {val_loss:.4f}")

    torch.save(model.state_dict(), "models/surrogate_model.pt")
    print("Model saved to models/surrogate_model.pt")

if __name__ == "__main__":
    train()
