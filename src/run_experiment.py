import argparse
import numpy as np
from deepSHAP_explainer import DeepSHAPAlphaFold

parser = argparse.ArgumentParser(description="Run OpenFold with DeepSHAP")
parser.add_argument("--input", type=str, required=True, help="Input protein sequence (FASTA)")
parser.add_argument("--output", type=str, required=True, help="Output directory")

args = parser.parse_args()

model_path = "openfold_checkpoint.pth"
explainer = DeepSHAPAlphaFold(model_path)

with open(args.input, "r") as file:
    sequence = file.read().strip()

shap_values = explainer.explain(sequence)
np.save(f"{args.output}/shap_values.npy", shap_values)

print("DeepSHAP analysis completed. Results saved.")
