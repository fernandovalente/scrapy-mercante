build:
	docker-compose build

local:
	docker-compose up

scraper-test:
	docker-compose run fast-api python3 /app/scraper/portspider.py