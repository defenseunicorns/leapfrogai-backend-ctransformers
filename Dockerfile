FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev-amd64 as builder

WORKDIR /leapfrogai

COPY requirements.txt .

RUN pip install -r requirements.txt --user
RUN pip install wget --user

USER root
RUN mkdir -p .model/ && \
    wget https://huggingface.co/TheBloke/SynthIA-7B-v2.0-GGUF/resolve/main/synthia-7b-v2.0.Q4_K_M.gguf && \
    mv synthia-7b-v2.0.Q4_K_M.gguf .model/model.gguf

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-amd64

WORKDIR /leapfrogai

COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-package
COPY --from=builder /home/nonroot/.local/bin/leapfrogai /home/nonroot/.local/bin/leapfrogais
COPY --from=builder /leapfrogai/.model/ /leapfrogai/.model/

COPY main.py .

EXPOSE 50051:50051

ENTRYPOINT ["/home/nonroot/.local/bin/leapfrogai", "--app-dir=.", "main:Model"]

