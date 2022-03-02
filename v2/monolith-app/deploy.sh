docker build -t monolith-app:1.0 .
docker network create simplebank-net
docker run -d --name monolith-app --net simplebank-net monolith-app:1.0