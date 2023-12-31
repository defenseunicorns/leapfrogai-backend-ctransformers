# LeapfrogAI CTransformers Backend

## Description

A LeapfrogAI API-compatible CTransformers wrapper for quantized model inferencing.

## Instructions

### Run Locally

For cloning a model locally and running the development backend.

#### Run Python Backend Locally

```bash
# Clone Model
mkdir .model/
wget https://huggingface.co/TheBloke/Synthia-7B-v2.0-GGUF/resolve/main/synthia-7b-v2.0.Q4_K_M.gguf
mv synthia-7b-v2.0.Q4_K_M.gguf .model/synthia-7b-v2.0.Q4_K_M.gguf

# Setup Python Virtual Environment
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt

# Start Model Backend
python main.py
```

### Docker Run

#### Local Image Build and Run

For local image building and running.

```bash
docker build -t ghcr.io/defenseunicorns/leapfrogai/ctransformers:latest .
docker run -p 50051:50051 ghcr.io/defenseunicorns/leapfrogai/ctransformers:latest
```

#### Remote Image Build and Run

For pulling a tagged image from the main release repository.

Where `<IMAGE_TAG>` is the released packages found [here](https://github.com/orgs/defenseunicorns/packages/container/package/leapfrogai%2Fctransformers).

```bash
docker build -t ghcr.io/defenseunicorns/leapfrogai/ctransformers:<IMAGE_TAG> .
docker run -p 50051:50051 ghcr.io/defenseunicorns/leapfrogai/ctransformers:<IMAGE_TAG>
```

### Docker Build and Push

This is for pushing a new image tag to the repository. Beforehand, ensure you run a `git tag <IMAGE_TAG>`.

```bash
make docker-build
make docker-push
```
