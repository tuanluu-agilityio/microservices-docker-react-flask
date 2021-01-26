.PHONY: build

runbuild: killcompose
	@docker-compose -f docker-compose-dev.yml up --build -d

runtest:
	@docker-compose -f docker-compose-dev.yml run users python manage.py test

recreate_db:
	@docker-compose -f docker-compose-dev.yml run users python manage.py recreate_db

seed_db:
	@docker-compose -f docker-compose-dev.yml run users python manage.py seed_db

killcompose:
	@docker-compose -f docker-compose-dev.yml down

runnginx:
	@docker-compose -f docker-compose-dev.yml up --build nginx

runbuild_prod:
	@docker-compose -f docker-compose-prod.yml up -d --build

runcov:
	@docker-compose -f docker-compose-dev.yml run users python manage.py cov
