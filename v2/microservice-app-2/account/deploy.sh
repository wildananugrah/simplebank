docker build -t account:1.0 . 
docker run -d --name account -p 3101:3101 account:1.0
docker network connect simplebank-net account