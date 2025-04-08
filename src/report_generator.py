import pandas as pd

def generate_html_report(shap_csv, output_file, shap_3d_html=None):
    df = pd.read_csv(shap_csv)

    html_header = """
    <html>
    <head>
        <title>SHAP Analysis Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1, h2 { color: #2c3e50; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 30px; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            th { background-color: #f2f2f2; }
            img { width: 90%; margin-top: 20px; }
            iframe { width: 100%; height: 600px; border: none; margin-top: 30px; }
        </style>
    </head>
    <body>
    """

    html_body = f"""
    <h1>DeepSHAP Analysis Report</h1>
    <h2>Top 10 Residues by SHAP Value</h2>
    {df.sort_values(by='SHAP', ascending=False).head(10).to_html(index=False)}

    <h2>PTM Annotations</h2>
    {df[df['PTM'] != ''].to_html(index=False)}

    <h2>Visualizations</h2>
    <img src="shap_barplot.png" alt="SHAP Barplot">
    <img src="shap_heatmap.png" alt="SHAP Heatmap">
    """

    if shap_3d_html:
        html_body += f"""
        <h2>3D SHAP Visualization</h2>
        <iframe src="{shap_3d_html}"></iframe>
        """

    html_footer = """
    </body>
    </html>
    """

    full_html = html_header + html_body + html_footer

    with open(output_file, 'w') as f:
        f.write(full_html)

    print(f"Full report with 3D viewer saved to {output_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to annotated CSV")
    parser.add_argument("--output", required=True, help="Path to save HTML report")
    parser.add_argument("--shap3d", default=None, help="Path to SHAP 3D HTML viewer (optional)")
    args = parser.parse_args()

    generate_html_report(args.input, args.output, shap_3d_html=args.shap3d)
