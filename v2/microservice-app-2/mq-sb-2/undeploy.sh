docker network disconnect simplebank-net mq-sb-1
docker container stop mq-sb-1
docker container rm mq-sb-1
docker image rm mq-sb-1:1.0