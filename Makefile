VERSION := $(shell git describe --abbrev=0 --tags)

create-venv:
	python -m venv .venv

activate-venv:
	source .venv/bin/activate

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
	git clone https://huggingface.co/Sidharthkr/MPT-7b-chat-GGML model & \
	docker build -t ghcr.io/defenseunicorns/leapfrogai-backend-ctransformers:${VERSION} .

make docker-push:
	docker push ghcr.io/defenseunicorns/leapfrogai-backend-ctransformers:${VERSION}