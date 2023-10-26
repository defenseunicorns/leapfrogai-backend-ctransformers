# LeapfrogAI CTransformers Backend

## Description

A LeapfrogAI API-compatible CTransformers wrapper for quantized model inferencing.

## Instructions

### Clone model locally

```bash
mkdir .model/
wget https://huggingface.co/TheBloke/mpt-7b-chat-GGML/resolve/main/mpt-7b-chat.ggmlv0.q4_0.bin
mv mpt-7b-chat.ggmlv0.q4_0.bin .model/mpt-7b-chat.ggmlv0.q4_0.bin
```

### Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
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
