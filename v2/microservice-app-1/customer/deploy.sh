docker build -t customer:1.0 . 
docker run -d --name customer -p 3100:3100 customer:1.0
docker network connect simplebank-net customer