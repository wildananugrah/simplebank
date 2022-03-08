run-dev:
	@python main.py

run-model-test:
	@pytest tests/test_model.py -v -s --durations=0

run-api-test:
	@pytest tests/test_api.py -v -s --durations=0

run-coverage-test:
	@coverage run -m pytest tests/test_model.py; coverage html

compose-up:
	@docker-compose up -d --build --remove-orphans

compose-down:
	@docker-compose down