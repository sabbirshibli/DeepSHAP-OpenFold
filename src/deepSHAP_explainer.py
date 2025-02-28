import torch
import shap
import numpy as np
from openfold.model.model import AlphaFold

class DeepSHAPAlphaFold:
    def __init__(self, model_path):
        self.model = AlphaFold.load_model(model_path)
        self.model.eval()
        self.explainer = shap.DeepExplainer(self.model, self._generate_baseline())

    def _generate_baseline(self, seq_len=400):
        return torch.zeros((1, seq_len, 20))

    def explain(self, input_sequence):
        inputs = self._encode_sequence(input_sequence)
        shap_values = self.explainer.shap_values(inputs)
        return shap_values

    def _encode_sequence(self, sequence):
        amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
        return torch.tensor([[amino_acids.index(aa) for aa in sequence]], dtype=torch.float32)

if __name__ == "__main__":
    model_path = "openfold_checkpoint.pth"
    explainer = DeepSHAPAlphaFold(model_path)
    sequence = "MESFFSRSTSIVSKLSFLALWIVFLISSSSFTSTEAYDALDPEGNITMKWDVMSWTPDGYVAVVTMFNFQKYRHIQSPGWTLGWKWAKKEVIWSMVGAQTTEQGDCSKYKGNIPHCCKKDPTVVDLLPGTPYNQQIANCCKGGVMNSWVQDPATAASSFQISVGAAGTTNKTVRVPRNFTLMGPGPGYTCGPAKIVRPTKFVTTDTRRTTQAMMTWNITCTYSQFLAQRTPTCCVSLSSFYNETIVGCPTCACGCQNNRTESGACLDPDTPHLASVVSPPTKKGTVLPPLVQCTRHMCPI RVHWHVKQNYKEYWRVKITITNFNYRLNYTQWNLVAQHPNLDNITQIFSFNYKSLTPYAGLNDTAMLWGVKFYNDFLSEAGPLGNVQSEILFRKDQSTFTFEKGWAFPRRIYFNGDNCVM PPPDSYPFLPNGGSRSQFSFVAAVLLPLLVFFFFSA"
    shap_values = explainer.explain(sequence)
    np.save("results/shap_values.npy", shap_values)
