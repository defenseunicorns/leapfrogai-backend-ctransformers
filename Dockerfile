ARG ARCH=arm64

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev-${ARCH} as builder

WORKDIR /leapfrogai

COPY requirements.txt .

RUN pip install ctransformers --no-binary ctransformers
RUN pip install -r requirements.txt --user
RUN pip install wget --user

USER root
RUN mkdir -p .model/ && \
    wget https://huggingface.co/TheBloke/SynthIA-7B-v2.0-GGUF/resolve/main/synthia-7b-v2.0.Q4_K_M.gguf && \
    mv synthia-7b-v2.0.Q4_K_M.gguf .model/synthia-7b-v2.0.Q4_K_M.gguf

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-${ARCH}

WORKDIR /leapfrogai

COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages
COPY --from=builder /leapfrogai/.model/ /leapfrogai/.model/

COPY main.py .

EXPOSE 50051:50051

ENTRYPOINT ["python3", "main.py"]
