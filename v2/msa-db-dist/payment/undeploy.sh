docker network disconnect simplebank-net payment
docker container stop payment
docker container rm payment
docker image rm payment:1.0