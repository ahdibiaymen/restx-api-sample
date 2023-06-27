
.PHONY: help build-services start-services stop-services

load-env:
	container_id=$(docker ps | grep jenkins | awk '{print $1}')
	docker cp .env $container_id:/var/jenkins_home/workspace/restx-api-erp_develop/erp/.env

populate-db:
	container_id=$(docker ps | grep erp-app | awk '{print $1}')
	docker exec $container_id
create-network:
	docker network create --attachable paytonkawa-network
remove-network:
	docker network rm paytonkawa-network
build:
	docker-compose build
start:
	docker-compose  up -d --force-recreate
stop:
	docker-compose  down

