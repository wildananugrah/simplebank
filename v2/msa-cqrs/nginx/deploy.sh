docker build -t monolith-nginx:1.0 .
docker run -d --name monolith-nginx -p 4000:80 monolith-nginx:1.0
docker network connect simplebank-net monolith-nginx