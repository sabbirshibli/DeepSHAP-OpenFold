import os
import sys
import json
import torch
import pickle
import argparse
import subprocess
from pathlib import Path

def run_openfold(fasta_path, out_dir):
    openfold_dir = Path(__file__).resolve().parent.parent / "openfold"
    os.makedirs(out_dir, exist_ok=True)

    # Run OpenFold prediction
    command = [
        "python", str(openfold_dir / "run_pretrained_openfold.py"),
        "--fasta_paths", fasta_path,
        "--output_dir", out_dir,
        "--model_device", "cuda:0",
        "--config_preset", "model_1_ptm"
    ]
    print("Running OpenFold...")
    subprocess.run(command, check=True)

    # Locate pkl result
    pkl_file = next(Path(out_dir).rglob("*.pkl"), None)
    if pkl_file is None:
        raise FileNotFoundError("OpenFold output .pkl file not found.")

    print(f"Parsing OpenFold output: {pkl_file}")
    with open(pkl_file, "rb") as f:
        data = pickle.load(f)

    plddt = data["plddt"].tolist()
    output_json = Path(out_dir) / "openfold_output.json"
    with open(output_json, "w") as f:
        json.dump({"plddt": plddt}, f)

    print(f"Extracted pLDDT saved to {output_json}")
    return output_json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fasta", required=True, help="Path to input FASTA")
    parser.add_argument("--out", default="data", help="Output directory")
    args = parser.parse_args()

    run_openfold(args.fasta, args.out)
