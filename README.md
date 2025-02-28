# DeepSHAP for OpenFold - Explainable AI for AlphaFold2 Predictions

This repository contains an implementation of **DeepSHAP** to interpret protein structure predictions made by **OpenFold**, an open-source reimplementation of AlphaFold2.

## 📌 Features
- Integrates DeepSHAP with OpenFold to explain AlphaFold2 predictions.
- Identifies key amino acids influencing protein structure.
- Provides visualizations of SHAP values for interpretability.

## 🔧 Installation
```sh
git clone https://github.com/sabbirshibli/DeepSHAP-OpenFold.git
cd DeepSHAP-OpenFold
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```
## 🚀 Running the experiment
```sh
python src/run_experiment.py --input data/protein.fasta --output results/
python src/visualization.py --input results/shap_values.npy
```

## 📜 License
Licensed under the **MIT License**.

## 🔗 Reference
This work is part of our research on explainability in protein structure prediction. Citation details will be updated after publication.
