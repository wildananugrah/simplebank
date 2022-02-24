docker network disconnect simplebank-net customer
docker container stop customer
docker container rm customer
docker image rm customer:1.0