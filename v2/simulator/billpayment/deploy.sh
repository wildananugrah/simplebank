docker build -t sim_billpayment:1.0 . 
docker run -d --name sim_billpayment -p 9010:9010 sim_billpayment:1.0
docker network connect simplebank-net sim_billpayment