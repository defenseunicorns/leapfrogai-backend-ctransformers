# LeapfrogAI CTransformers Backend

## Description

A LeapfrogAI API-compatible CTransformers wrapper for quantized model inferencing.

## Instructions

### Run Locally

```bash
# Clone Model
mkdir .model/
wget https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q2_K.gguf
mv mistral-7b-v0.1.Q2_K.gguf .model/mistral-7b-v0.1.Q2_K.gguf

# Setup Python Virtual Environment
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt

# Start Model Backend
python main.py
```

### Docker Run Locally

```bash
docker build -t ghcr.io/defenseunicorns/leapfrogai/ctransformers:latest .
docker run -p 50051:50051 ghcr.io/defenseunicorns/leapfrogai/ctransformers:latest
```

### Docker Build and Push

```bash
make docker-build
make docker-push
```
