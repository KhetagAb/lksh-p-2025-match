mode := dev

up:
	docker-compose -f core/docker-compose.$(mode).yml up --build --force-recreate --remove-orphans -d
	docker-compose -f bff/docker-compose.yml up --build --force-recreate --remove-orphans -d