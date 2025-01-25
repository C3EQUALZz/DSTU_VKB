DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker/app.yml
STORAGES_FILE = docker/storages.yml
CACHE_FILE = docker/cache.yml
METRICS_FILE = docker/metrics.yml
APP_CONTAINER = pacman-app-backend

.PHONY: app
app:
	$(DC) -f $(APP_FILE) $(ENV) up --build -d

.PHONY: storages
storages:
	$(DC) -f $(STORAGES_FILE) $(ENV) up --build -d

.PHONY: cache
cache:
	$(DC) -f $(CACHE_FILE) $(ENV) up --build -d

.PHONY: metrics
metrics:
	$(DC) -f $(METRICS_FILE) $(ENV) up --build -d

.PHONY: all
all:
	$(DC) -f $(STORAGES_FILE) -f $(APP_FILE) -f $(CACHE_FILE) -f $(METRICS_FILE) $(ENV) up --build -d

.PHONY: all-down
all-down:
	$(DC) -f $(STORAGES_FILE) -f $(APP_FILE) -f $(CACHE_FILE) -f $(METRICS_FILE) $(ENV) down

.PHONY: app-down
app-down:
	$(DC) -f $(APP_FILE) ${ENV} down

.PHONY: storages-down
storages-down:
	$(DC) -f $(STORAGES_FILE) ${ENV} down

.PHONY: storages-down
cache-down:
	$(DC) -f $(CACHE_FILE) ${ENV} down

.PHONY: metrics-down
metrics-down:
	$(DC) -f $(METRICS_FILE) $(ENV) down

.PHONY: app-shell
app-shell:
	$(EXEC) $(APP_CONTAINER) bash

.PHONY: app-logs
app-logs:
	$(LOGS) $(APP_CONTAINER) -f