.PHONY: app-dev app-prd ollama ui stop clean

RUN=poetry run  # ou 'pasta_ambiente_virtual/bin/python' se não usar 'poetry'
COMPOSE=docker compose

app-dev:
	${RUN} rio run

app-prd:
	${RUN} rio run --release

ollama:
	${COMPOSE} up ollama -d

ui:
	${COMPOSE} up open-webui -d

stop:
	${COMPOSE} down

clean:
	${COMPOSE} down --volumes --remove-orphans
