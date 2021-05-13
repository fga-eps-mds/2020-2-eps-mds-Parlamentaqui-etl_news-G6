start-dev:
	docker-compose up

rebuild:
	docker-compose up --build

start-prod:
	docker-compose up --build --detach 

test:
	sudo docker-compose run prlmntq_etl_news python  src/test.py
