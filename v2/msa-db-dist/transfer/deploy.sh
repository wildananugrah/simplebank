docker build -t transfer:1.0 . 
docker run -d --name transfer -p 3100:3100 transfer:1.0
docker network connect simplebank-net transfer