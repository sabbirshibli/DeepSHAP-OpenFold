import argparse
import numpy as np
import pandas as pd
from Bio import SeqIO

def load_fasta_sequence(fasta_file):
    record = next(SeqIO.parse(fasta_file, "fasta"))
    return str(record.seq)

def annotate_shap(shap_file, fasta_file, output_file, ptm_dict=None):
    shap_values = np.load(shap_file)
    sequence = load_fasta_sequence(fasta_file)

    if shap_values.shape[0] != len(sequence):
        raise ValueError("SHAP values and sequence length mismatch.")

    data = {
        'Index': list(range(1, len(sequence) + 1)),
        'AminoAcid': list(sequence),
        'SHAP': shap_values.tolist(),
        'PTM': ['' for _ in sequence]
    }

    if ptm_dict:
        for idx, label in ptm_dict.items():
            if idx < len(sequence):
                data['PTM'][idx] = label

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Annotated SHAP output written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--shap", required=True)
    parser.add_argument("--fasta", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    ptm_dict = {4: "Phospho", 10: "Ubiquitin"}
    annotate_shap(args.shap, args.fasta, args.output, ptm_dict)
