VERSION := $(shell git describe --abbrev=0 --tags)

create-venv:
	python -m venv .venv

activate-venv:
	source .venv/bin/activate

fetch-model:
	mkdir -p .model/
	wget https://huggingface.co/TheBloke/SynthIA-7B-v2.0-GGUF/resolve/main/synthia-7b-v2.0.Q4_K_M.gguf
	mv synthia-7b-v2.0.Q4_K_M.gguf .model/synthia-7b-v2.0.Q4_K_M.gguf

requirements-dev:
	python -m pip install -r requirements-dev.txt

requirements:
	pip-sync requirements.txt requirements-dev.txt

build-requirements:
	pip-compile -o requirements.txt pyproject.toml

build-requirements-dev:
	pip-compile --extra dev -o requirements-dev.txt pyproject.toml

test:
	pytest **/*.py

dev:
	python main.py

make docker-build:
	docker build -t ghcr.io/defenseunicorns/leapfrogai/ctransformers:${VERSION} .

make docker-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/ctransformers:${VERSION}