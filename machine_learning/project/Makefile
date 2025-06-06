DC = docker compose
NETWORK_NAME = microservices-network
GRAFANA_NETWORK_NAME = grafana-network

# 👉 Создание сети (не падать, если она уже есть)
network:
	-@docker network rm $(NETWORK_NAME)
	@docker network create $(NETWORK_NAME)
	-@docker network rm $(GRAFANA_NETWORK_NAME)
	@docker network create $(GRAFANA_NETWORK_NAME)

grafana:
	cd monitoring && $(DC) -f docker-compose-override.yaml up --build -d

down-grafana:
	cd monitoring && $(DC) -f docker-compose-override.yaml down

# 👉 Поднять kafka (брокер)
broker:
	cd kafka && $(DC) -f docker-compose-override.yaml up --build -d

down-broker:
	cd kafka && $(DC) -f docker-compose-override.yaml down

# 👉 Поднять user сервис
user:
	cd user-service && $(DC) --env-file .env -f docker-compose-override.yaml up --build -d

down-user:
	cd user-service && $(DC) --env-file .env -f docker-compose-override.yaml down

# 👉 Поднять text сервис
text:
	cd text-service && $(DC) --env-file .env -f docker-compose-override.yaml up --build -d

down-text:
	cd text-service && $(DC) --env-file .env -f docker-compose-override.yaml down

# 👉 Поднять image сервис
image:
	cd image-service && $(DC) --env-file .env -f docker-compose-override.yaml up --build -d

down-image:
	cd image-service && $(DC) --env-file .env -f docker-compose-override.yaml down

# 👉 Поднять telegram сервис
telegram:
	cd telegram-service && $(DC) --env-file .env -f docker-compose-override.yaml up --build -d

down-telegram:
	cd telegram-service && $(DC) --env-file .env -f docker-compose-override.yaml down

# 👉 Поднять всё (по порядку)
production: network grafana broker image user telegram

all: network broker image user telegram

down-all: down-user down-broker down-image down-telegram
	@docker network rm $(NETWORK_NAME) || true

# 👉 Остановить все сервисы
down-production: down-image down-grafana down-user down-broker down-text down-telegram
	@docker network rm $(NETWORK_NAME) || true
	@docker network rm $(GRAFANA_NETWORK_NAME) || true