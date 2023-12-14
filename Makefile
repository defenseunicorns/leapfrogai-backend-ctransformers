VERSION := $(shell git describe --abbrev=0 --tags 2> /dev/null )
ifeq ($(VERSION),)
  VERSION := latest
endif

ARCH := $(shell uname -m | sed s/aarch64/arm64/ | sed s/x86_64/amd64/)

MODEL_URL ?= https://huggingface.co/TheBloke/SynthIA-7B-v2.0-GGUF/resolve/main/synthia-7b-v2.0.Q4_K_M.gguf

.PHONY: all

create-venv:
	python -m venv .venv

activate-venv:
	source .venv/bin/activate

fetch-model:
	mkdir -p .model/
	wget ${MODEL_URL}
	mv *.gguf .model/model.gguf	

requirements-dev:
	python -m pip install -r requirements-dev.txt

requirements-gpu:
	CMAKE_ARGS="-DLLAMA_CUBLAS=on" python -m pip install -r requirements-gpu.txt
	
requirements:
	pip-sync requirements.txt requirements-dev.txt

build-requirements:
	pip-compile -o requirements.txt pyproject.toml

build-requirements-dev:
	pip-compile --extra dev -o requirements-dev.txt pyproject.toml

build-requirements-gpu:
	pip-compile --extra gpu -o requirements-gpu.txt pyproject.toml

test:
	pytest **/*.py

dev:
	leapfrogai main.Model

docker-build:
	if ! [ -f config.yaml ]; then cp config.example.yaml config.yaml; fi
	docker build -t ghcr.io/defenseunicorns/leapfrogai/llama-cpp-py:${VERSION}-${ARCH} . --build-arg ARCH=${ARCH}

docker-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/llama-cpp-py:${VERSION}-${ARCH}