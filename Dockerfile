FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

RUN apt-get update && apt-get install -y git wget python3-pip python3-dev

RUN pip3 install --upgrade pip
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt
RUN pip3 install biopython scipy dgl seaborn shap matplotlib pandas
RUN pip3 install git+https://github.com/facebookresearch/esm.git

CMD ["bash"]