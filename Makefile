DEV_COMPOSE=dockerfiles/docker-compose-dev.yml

DEFAULT_DB=driverbackend

# Development commands

up-postgres-dev:
	docker-compose -f $(DEV_COMPOSE) up -d db_postgres

build-api-dev:
	docker-compose -f $(DEV_COMPOSE) up --build api

build-dev:
	docker-compose -f $(DEV_COMPOSE) up -d db_postgres &&\
	docker-compose -f $(DEV_COMPOSE) up --build api

run-dev:
	docker-compose -f $(DEV_COMPOSE) up -d db_postgres &&\
	docker-compose -f $(DEV_COMPOSE) run --service-ports api

ALL_CONTAINERS = $$(sudo docker ps -a -q)

ALL_IMAGES = $$(sudo docker images -q)

# Stop Containers
stop-all:
	sudo docker stop $(ALL_CONTAINERS)

# Remove Containers
rm-all:
	sudo docker rm $(ALL_CONTAINERS)

# Remove Images
rm-images:
	sudo docker rmi $(ALL_IMAGES)

# Container access

ssh-api:
	docker exec -it api bash

ssh-postgres:
	docker exec -it db_postgres bash

# Scripts
collectstatic:
	docker exec -it api python manage.py collectstatic

createsuperuser:
	docker exec -it api python manage.py createsuperuser

makemigrations:
	docker exec -it api python manage.py makemigrations

migrate:
	docker exec -it api python manage.py migrate

test:
	docker exec -it api python manage.py test

test_module:
	@read -p "Enter Module Name: " test_module; \
	docker exec -it api python manage.py test $$test_module

create_default_db:
	./scripts/database/create_db.sh $(DEFAULT_DB) $(DEFAULT_DB) $(DEFAULT_DB)
