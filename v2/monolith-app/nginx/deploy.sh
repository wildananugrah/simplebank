docker build -t monolith-nginx:1.0 .
docker run -d --name monolith-nginx --net simplebank-net -p 3000:80 monolith-nginx:1.0