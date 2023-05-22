
.PHONY: help build-services start-services stop-services

build:
	docker network create --attachable paytonkawa-network
	docker-compose  build
start:
	docker-compose  up -d
stop:
	docker-compose  down
	docker network rm paytonkawa-network
