docker build -t mq-sb-1:1.0 . 
docker run -d --name mq-sb-1 mq-sb-1:1.0
docker network connect simplebank-net mq-sb-1