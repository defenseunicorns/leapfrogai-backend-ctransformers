FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev-amd64 as builder

WORKDIR /leapfrogai

COPY requirements.txt .

RUN pip install -r requirements.txt --user
RUN pip install wget --user
RUN mkdir -p .model/TheBloke/mpt-7b-chat-GGML && \
    wget https://huggingface.co/TheBloke/mpt-7b-chat-GGML/resolve/main/mpt-7b-chat.ggmlv0.q4_0.bin && \
    mv mpt-7b-chat.ggmlv0.q4_0.bin .model/TheBloke/mpt-7b-chat-GGML/mpt-7b-chat.ggmlv0.q4_0.bin

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-amd64

WORKDIR /leapfrogai

COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages
COPY --from=builder /leapfrogai/.model/TheBloke/mpt-7b-chat-GGML/ /leapfrogai/.model/TheBloke/mpt-7b-chat-GGML

COPY main.py .

EXPOSE 50051:50051

ENTRYPOINT ["python3", "main.py"]
