
build-services:
	docker-compose --env-file crm/.env build
start-services:
	docker-compose --env-file crm/.env up -d
stop-services:
	docker-compose --env-file crm/.env down
