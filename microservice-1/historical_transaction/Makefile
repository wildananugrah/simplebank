run-test:
	@pytest -v

run-app-dev:
	@uvicorn main:app --reload --host 0.0.0.0 --port 7030

run-db-dev:
	@docker run --name simplebank-pg -p 6000:5432 -v data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=simplebank! -e POSTGRES_USER=simplebank -e POSTGRES_DB=simplebank-db -d postgres

run-pg-admin:
	@docker run --name pgadmin -p 9090:80 -e 'PGADMIN_DEFAULT_EMAIL=user@gmail.com' -e 'PGADMIN_DEFAULT_PASSWORD=password1!' -d dpage/pgadmin4

compose-up:
	@docker-compose up -d --build --remove-orphans

compose-down:
	@docker-compose down