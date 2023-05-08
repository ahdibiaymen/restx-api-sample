
build-services:
	docker-compose --env-file erp/.env build
start-services:
	docker-compose --env-file erp/.env up -d
stop-services:
	docker-compose --env-file erp/.env down
