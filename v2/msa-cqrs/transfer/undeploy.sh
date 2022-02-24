docker network disconnect simplebank-net transfer
docker container stop transfer
docker container rm transfer
docker image rm transfer:1.0