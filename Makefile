start-dev:
	docker-compose up

rebuild:
	docker-compose up --build

start-prod:
	docker-compose up --build --detach 
