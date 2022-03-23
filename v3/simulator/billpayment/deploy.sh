docker build -t sim_billpayment:1.0 . 
# docker run -d --name sim_billpayment --net simplebank-net -p 9010:9010 sim_billpayment:1.0
docker run -d --name sim_billpayment -e MONGODB_HOST=mongodb://mongo:27017 -p 3010:9010 --net simulator_net sim_billpayment:1.0