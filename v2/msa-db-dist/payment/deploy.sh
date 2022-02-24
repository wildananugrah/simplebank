docker build -t payment:1.0 . 
docker run -d --name payment -p 3103:3103 payment:1.0
docker network connect simplebank-net payment