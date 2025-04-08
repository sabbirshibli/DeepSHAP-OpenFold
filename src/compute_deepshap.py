import shap
import torch
import torch.nn as nn
import numpy as np
from Bio import SeqIO

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

def compute_shap():
    record = next(SeqIO.parse("data/protein.fasta", "fasta"))
    sequence = str(record.seq)
    encoded = one_hot_encode(sequence)
    X = torch.tensor(encoded, dtype=torch.float32)

    model = MLP(input_dim=20)
    model.load_state_dict(torch.load("models/surrogate_model.pt"))
    model.eval()

    background = X[np.random.choice(X.shape[0], 5, replace=False)]
    explainer = shap.DeepExplainer(model, background)
    shap_values = explainer.shap_values(X)

    shap_sum = np.array(shap_values).sum(axis=2).flatten()  # [residues]
    np.save("results/shap_values.npy", shap_sum)
    print("SHAP values saved to results/shap_values.npy")

if __name__ == "__main__":
    compute_shap()
