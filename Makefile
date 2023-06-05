PROJECT_NAME := k8s-pods-ttl
DOCKER_REGISTRY := rcdfs

build:
	@echo 'Running docker build'
	docker build \
		-t $(DOCKER_REGISTRY)/$(PROJECT_NAME):latest \
		-f Dockerfile \
		.

push:
	@echo 'Pushing docker image'
	docker push $(DOCKER_REGISTRY)/$(PROJECT_NAME):latest

test:
	@echo 'Running tests for pipelines'
	poetry run python -m pytest --show-capture=no -vvvv --ignore=tests/ -m "not integration" -x tests
