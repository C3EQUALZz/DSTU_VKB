DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker/app.yml
CACHE_FILE = docker/cache.yml
APP_CONTAINER = theory-of-information-app-backend

.PHONY: app
app:
	$(DC) -f $(APP_FILE) $(ENV) up --build -d

.PHONY: cache
cache:
	$(DC) -f $(CACHE_FILE) $(ENV) up --build -d

.PHONY: all
all:
	$(DC) -f $(APP_FILE) -f $(CACHE_FILE) $(ENV) up --build -d

.PHONY: all-down
all-down:
	$(DC) -f $(APP_FILE) -f $(CACHE_FILE) $(ENV) down

.PHONY: app-down
app-down:
	$(DC) -f $(APP_FILE) ${ENV} down

.PHONY: cache-down
cache-down:
	$(DC) -f $(CACHE_FILE) ${ENV} down

.PHONY: app-shell
app-shell:
	$(EXEC) $(APP_CONTAINER) bash

.PHONY: app-logs
app-logs:
	$(LOGS) $(APP_CONTAINER) -f