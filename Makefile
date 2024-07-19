.PHONY: run-app-dev run-app-prd run-ollama run-ui

RUN=poetry run
COMPOSE=docker compose

run-app-dev:
	${RUN} rio run

run-app-prd:
	${RUN} rio run --release

run-ollama:
	${COMPOSE} up ollama -d

run-ui:
	${COMPOSE} up open-webui -d
