import argparse
import pandas as pd
import py3Dmol
from Bio.PDB import PDBParser

def get_residue_indices(pdb_file):
    """Extracts residue indices (1-based) from PDB file."""
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("X", pdb_file)
    residues = []
    for model in structure:
        for chain in model:
            for residue in chain:
                if 'CA' in residue:  # Only include standard residues
                    res_id = residue.get_id()[1]
                    residues.append(res_id)
    return residues

def map_shap_to_structure(pdb_file, shap_csv, output_html):
    df = pd.read_csv(shap_csv)
    residue_indices = get_residue_indices(pdb_file)

    if len(df) != len(residue_indices):
        raise ValueError("SHAP length does not match residue count in PDB.")

    view = py3Dmol.view(width=800, height=600)
    with open(pdb_file, 'r') as f:
        pdb = f.read()
    view.addModel(pdb, "pdb")

    max_shap = df['SHAP'].abs().max()

    for idx, row in df.iterrows():
        shap_score = row['SHAP']
        norm = (shap_score + max_shap) / (2 * max_shap)  # scale to [0,1]
        color = f"rgb({int(255*(1-norm))},{int(255*norm)},0)"  # Red-Green scale
        resi = residue_indices[idx]
        view.setStyle({'resi': str(resi)}, {'cartoon': {'color': color}})

    view.zoomTo()
    view.setBackgroundColor("white")

    # Export to standalone HTML
    with open(output_html, 'w') as f:
        f.write(view._make_html())
    print(f"3D SHAP visualization saved to {output_html}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdb", required=True, help="Path to input PDB file")
    parser.add_argument("--shap", required=True, help="Path to annotated SHAP CSV")
    parser.add_argument("--output", required=True, help="Path to save HTML visualization")
    args = parser.parse_args()

    map_shap_to_structure(args.pdb, args.shap, args.output)
