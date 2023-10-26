# LeapfrogAI ctransformers Backend

## Description

## Instructions

### Clone model locally

```
mkdir .model/
wget https://huggingface.co/TheBloke/mpt-7b-chat-GGML/resolve/main/mpt-7b-chat.ggmlv0.q4_0.bin
mv mpt-7b-chat.ggmlv0.q4_0.bin .model/mpt-7b-chat.ggmlv0.q4_0.bin
```

### Run Locally

```
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python main.py
```

### Docker

```
docker build -t leapfrog-backend-ctransformers:latest .
docker run -p 50051:50051 leapfrog-backend-ctransformers:latest
```