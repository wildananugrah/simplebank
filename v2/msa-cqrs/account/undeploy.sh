docker network disconnect simplebank-net account
docker container stop account
docker container rm account
docker image rm account:1.0