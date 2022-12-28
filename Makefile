migrate:
	docker-compose exec backend alembic upgrade head

m?=
migrations:
	docker-compose exec backend alembic revision --autogenerate -m "$(m)"

downgrade:
	docker-compose exec backend alembic downgrade -1

test:
	docker-compose exec backend pytest --asyncio-mode=auto