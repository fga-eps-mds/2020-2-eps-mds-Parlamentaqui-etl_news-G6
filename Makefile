start-dev:
	docker-compose up

rebuild:
	docker-compose up --build

start-prod:
	docker-compose up --build --detach 

test:
	sudo docker run prlmntq_etl_news sh -c 'python3 src/test.py'
