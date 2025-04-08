# DeepSHAP-OpenFold

This project integrates **OpenFold** and **DeepSHAP** to generate explainable residue-level attributions for predicted protein structures. It includes:

- OpenFold-based structure prediction and pLDDT extraction
- Training a surrogate MLP model on sequence → pLDDT
- DeepSHAP explanation of the surrogate model
- Annotation of SHAP values with sequence, PTMs
- Visualization: 2D sequence plots and 3D structure viewer
- Auto-generated interactive HTML reports

---

## 📁 Project Structure

```
DeepSHAP-OpenFold-Full/
├── openfold/                    # Full OpenFold repo (after setup)
├── data/                        # Input FASTA, output pLDDT
├── models/                      # Surrogate model checkpoint
├── results/                     # SHAP outputs, plots, report
├── src/                         # All pipeline scripts
├── notebooks/                   # (Optional) Jupyter demos
├── run_pipeline.sh              # One-click shell script
├── Makefile                     # Alternative DAG execution
├── Snakefile                    # Snakemake version
├── requirements.txt             # Python dependencies
├── environment.yml              # Conda environment (optional)
├── LICENSE                      # MIT License
├── CITATION.cff                 # Citation metadata
├── CONTRIBUTING.md              # Guidelines for contributors
├── CHANGELOG.md                 # Project changelog
└── README.md                    # You're here
```

---

## 📦 Environment Setup

This project requires a CUDA-compatible GPU. You will install **OpenFold**, **DeepSHAP**, and all dependencies via Conda and Pip.

### 1. Clone the Repository

```bash
git clone https://github.com/sabbirshibli/DeepSHAP-OpenFold.git
cd DeepSHAP-OpenFold
```

### 2. Run Setup Script

```bash
bash src/setup_openfold.sh
```

This will:
- Create Conda environment `openfold`
- Install PyTorch, DGL, ESM, and OpenFold
- Download pretrained weights
- Install all packages from `requirements.txt`

---

## 🚀 Full Pipeline (from FASTA to Report)

### 1. Prepare Input

Add your protein sequence to `data/protein.fasta`.

### 2. Run the Entire Pipeline

```bash
bash run_pipeline.sh
```

---

## 🔁 Alternative Execution Options

### ▶ Using Makefile

```bash
make         # run everything
make clean   # remove results
```

### ▶ Using Snakemake

```bash
snakemake --cores 1
```

---

## 🧪 Output Files

| File | Description |
|------|-------------|
| `data/openfold_output.json` | Extracted pLDDT values |
| `results/shap_values.npy` | SHAP values per residue |
| `results/mapped_shap.csv` | SHAP + AA + PTM mapping |
| `results/shap_barplot.png` | Per-residue SHAP barplot |
| `results/shap_heatmap.png` | Sequence SHAP heatmap |
| `results/shap_3d_visualization.html` | Py3Dmol 3D viewer |
| `results/annotated_report.html` | Full HTML report with all outputs |

---

## 💻 Requirements

Install from `requirements.txt`:
```bash
pip install -r requirements.txt
```

Or create a Conda env:
```bash
conda env create -f environment.yml
conda activate openfold
```

---

## 📜 License

MIT License © 2025 Sabbir Shibli

---

## 🔖 Citation

If you use this project, please cite it using the metadata in `CITATION.cff`.

---

## 🙋 Support

For issues or suggestions, open a GitHub issue or reach out to the maintainer.