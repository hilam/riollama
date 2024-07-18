.PHONY: run-app-dev run-app-prd

RUN=poetry run

run-app-dev:
	${RUN} rio run

run-app-prd:
	${RUN} rio run --release
