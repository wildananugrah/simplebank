docker network disconnect simplebank-net monolith-nginx
docker container stop monolith-nginx
docker container rm monolith-nginx
docker image rm monolith-nginx:1.0