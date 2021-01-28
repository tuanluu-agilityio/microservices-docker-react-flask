.PHONY: build

up: killcompose
	@docker-compose -f docker-compose-dev.yml up --build -d

test:
	@docker-compose -f docker-compose-dev.yml run users python manage.py test

recreate_db:
	@docker-compose -f docker-compose-dev.yml run users python manage.py recreate_db

seed_db:
	@docker-compose -f docker-compose-dev.yml run users python manage.py seed_db

killcompose:
	@docker-compose -f docker-compose-dev.yml down

nginx:
	@docker-compose -f docker-compose-dev.yml up --build nginx

build:
	@docker-compose -f docker-compose-prod.yml up -d --build

cov:
	@docker-compose -f docker-compose-dev.yml run users python manage.py cov
