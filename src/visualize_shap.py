import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_shap(csv_file):
    df = pd.read_csv(csv_file)

    plt.figure(figsize=(12, 5))
    sns.barplot(x='Index', y='SHAP', data=df, palette='coolwarm')
    plt.xlabel("Residue Index")
    plt.ylabel("SHAP Value")
    plt.title("SHAP Value per Amino Acid")
    plt.tight_layout()
    plt.savefig("results/shap_barplot.png")

    plt.figure(figsize=(12, 1))
    sns.heatmap([df['SHAP']], cmap='coolwarm', cbar=True, xticklabels=df['AminoAcid'], yticklabels=['SHAP Heatmap'])
    plt.tight_layout()
    plt.savefig("results/shap_heatmap.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    plot_shap(args.input)
