run-app-dev:
	@uvicorn main:app --reload --host 0.0.0.0 --port 8090

run-app-docker:
	@docker build -t simulator -f simulator.Dockerfile .
	@docker run --name simulator -p 8090:8090 -d simulator

remove-app-docker:
	@docker container stop simulator
	@docker container rm simulator
	@docker image rm simulator