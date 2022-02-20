docker run -d --hostname my-rabbit --name sb-rabbit -p 5672:5672 rabbitmq:3
docker network connect simplebank-net sb-rabbit