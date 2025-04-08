#!/bin/bash

# Create and activate conda environment
conda create -n openfold python=3.8 -y
source $(conda info --base)/etc/profile.d/conda.sh
conda activate openfold

# Install PyTorch with CUDA (adjust CUDA version as needed)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Clone OpenFold
git clone https://github.com/aqlaboratory/openfold.git
cd openfold

# Install dependencies
pip install -r requirements.txt
pip install biopython scipy dgl "fair-esm[esmfold]"
pip install git+https://github.com/facebookresearch/esm.git

# Download pretrained weights (assumes wget is available)
mkdir -p openfold/resources
wget https://opendata.ccbb.pitt.edu/openfold/finetuned_model_params/finetuned_model_weights.pt -O openfold/resources/model_weights.pt

echo "✅ OpenFold setup complete."
