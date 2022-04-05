run-dev:
	@python main.py

run-model-test:
	@pytest tests/test_model.py -v -s --durations=0

run-api-test:
	@pytest -n 10 --count=2 tests/test_api.py -v -s --durations=0

run-api-test-10:
	@pytest --count=10 tests/test_api.py -v -s --durations=0

run-coverage-test:
	@coverage run -m pytest tests/test_model.py; coverage html; coverage report -m

compose-up:
	@docker-compose up -d --build --remove-orphans

compose-down:
	@docker-compose down

run-all:
	@python drop_db_2.py; make compose-down; make compose-up; make run-api-test; python data_integrity_test_saga.py