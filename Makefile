build:
	docker-compose build

local:
	uvicorn src.main:app --reload
