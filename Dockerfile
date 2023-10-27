FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev-amd64 as builder

WORKDIR /leapfrogai

COPY requirements.txt .

RUN pip install -r requirements.txt --user
RUN pip install wget --user

USER root
RUN mkdir -p .model/ && \
    wget https://huggingface.co/TheBloke/dolphin-2.1-mistral-7B-GGUF/resolve/main/dolphin-2.1-mistral-7b.Q4_K_M.gguf && \
    mv dolphin-2.1-mistral-7b.Q4_K_M.gguf .model/dolphin-2.1-mistral-7b.Q4_K_M.gguf

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-amd64

WORKDIR /leapfrogai

COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages
COPY --from=builder /leapfrogai/.model/ /leapfrogai/.model/

COPY main.py .

EXPOSE 50051:50051

ENTRYPOINT ["python3", "main.py"]
