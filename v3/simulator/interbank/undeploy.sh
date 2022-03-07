# docker network disconnect simplebank-net sim_interbank
docker container stop sim_interbank
docker container rm sim_interbank
docker image rm sim_interbank:1.0