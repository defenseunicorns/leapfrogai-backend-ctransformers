# LeapfrogAI ctransformers Backend

## Description

## Instructions

### Clone model locally

```
mkdir .model/TheBloke/mpt-7b-chat-GGML/
cd .model/TheBloke/mpt-7b-chat-GGML/
wget https://huggingface.co/TheBloke/mpt-7b-chat-GGML/resolve/main/mpt-7b-chat.ggmlv0.q4_0.bin
```

### Docker

```
docker build --build-arg IMAGE_TAG=0.3.2 -t leapfrog-backend-ctransformers:latest .
docker run -p 50051:50051 leapfrog-backend-ctransformers:latest
```