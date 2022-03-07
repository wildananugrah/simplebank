run-dev:
	@python main.py

run-test:
	@pytest -v -s --durations=0

run-test-coverage:
	@coverage run -m pytest; coverage html

compose-up:
	@docker-compose up -d --build --remove-orphans

compose-down:
	@docker-compose down