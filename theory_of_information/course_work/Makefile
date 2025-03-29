APP_DIR = app
DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
STORAGES_FILE = docker/storages.yml
CODE_DIRS = ${APP_DIR} tests

.PHONY: storages
storages:
	$(DC) -f $(STORAGES_FILE) $(ENV) up --build -d

.PHONY: storages-down
storages-down:
	$(DC) -f $(STORAGES_FILE) ${ENV} down

.PHONY: lint
lint:
	isort ${CODE_DIRS}
	ruff check ${CODE_DIRS} --unsafe-fixes
	poetry check