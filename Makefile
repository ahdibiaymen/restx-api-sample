
.PHONY: help build-services start-services stop-services

build:
	docker-compose --env-file erp/.env build
start:
	docker-compose --env-file erp/.env up -d
stop:
	docker-compose --env-file erp/.env down
