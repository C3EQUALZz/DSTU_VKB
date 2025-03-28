DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
STORAGES_FILE = docker/storages.yml

.PHONY: storages
storages:
	$(DC) -f $(STORAGES_FILE) $(ENV) up --build -d

.PHONY: storages-down
storages-down:
	$(DC) -f $(STORAGES_FILE) ${ENV} down

