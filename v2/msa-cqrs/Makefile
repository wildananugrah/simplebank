compose-up:
	@docker-compose up -d --build --remove-orphans

compose-down:
	@docker-compose down

run-mq:
	@docker run -d --hostname my-rabbit --name sb-rabbit -p 5672:5672 rabbitmq:3

run-test:
	@pytest -v -s --durations=0