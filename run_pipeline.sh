#!/bin/bash

set -e  # Stop on error

FASTA="data/protein.fasta"
PDB="results/example.pdb"
OPENFOLD_OUTPUT="data/openfold_output.json"
SHAP_OUTPUT="results/shap_values.npy"
ANNOTATED_CSV="results/mapped_shap.csv"
STRUCTURE_HTML="results/shap_3d_visualization.html"
REPORT_HTML="results/annotated_report.html"

echo "🔁 STEP 1: Run OpenFold on $FASTA"
python src/run_openfold_inference.py --fasta $FASTA --out data/

echo "✅ OpenFold prediction complete: $OPENFOLD_OUTPUT"

echo "🧠 STEP 2: Train surrogate model"
python src/train_surrogate_model.py

echo "✅ Model trained and saved"

echo "🔍 STEP 3: Compute DeepSHAP values"
python src/compute_deepshap.py

echo "✅ SHAP values saved to $SHAP_OUTPUT"

echo "🧬 STEP 4: Annotate SHAP values with sequence and PTMs"
python src/annotate_shap.py --shap $SHAP_OUTPUT --fasta $FASTA --output $ANNOTATED_CSV

echo "✅ Annotated CSV generated: $ANNOTATED_CSV"

echo "📊 STEP 5: Visualize SHAP barplot and heatmap"
python src/visualize_shap.py --input $ANNOTATED_CSV

echo "✅ Visualizations saved"

echo "🧪 STEP 6: Map SHAP to structure and export interactive HTML viewer"
python src/structure_overlay.py --pdb $PDB --shap $ANNOTATED_CSV --output $STRUCTURE_HTML

echo "✅ 3D viewer HTML created: $STRUCTURE_HTML"

echo "📄 STEP 7: Generate final HTML report"
python src/report_generator.py --input $ANNOTATED_CSV --output $REPORT_HTML --shap3d $STRUCTURE_HTML

echo "✅ Report saved to $REPORT_HTML"

echo "🎉 All steps completed successfully!"
