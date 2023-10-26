# LeapfrogAI CTransformers Backend

## Description

A LeapfrogAI API-compatible CTransformers wrapper for quantized model inferencing.

## Instructions

### Run Locally

#### Clone Model Locally

```bash
mkdir .model/
wget https://huggingface.co/TheBloke/mpt-7b-chat-GGML/resolve/main/mpt-7b-chat.ggmlv0.q4_0.bin
mv mpt-7b-chat.ggmlv0.q4_0.bin .model/mpt-7b-chat.ggmlv0.q4_0.bin
```

#### Run Python Backend Locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python main.py
```

### Docker Run

#### Local Image Build and Run

```bash
docker build -t ghcr.io/defenseunicorns/leapfrogai/ctransformers:latest .
docker run -p 50051:50051 ghcr.io/defenseunicorns/leapfrogai/ctransformers:latest
```

#### Remote Image Build and Run

Where `<IMAGE_TAG>` is the released packages found [here](https://github.com/orgs/defenseunicorns/packages/container/package/leapfrogai%2Fctransformers).

```bash
docker build -t ghcr.io/defenseunicorns/leapfrogai/ctransformers:<IMAGE_TAG> .
docker run -p 50051:50051 ghcr.io/defenseunicorns/leapfrogai/ctransformers:<IMAGE_TAG>
```

### Docker Build and Push

```bash
make docker-build
make docker-push
```
