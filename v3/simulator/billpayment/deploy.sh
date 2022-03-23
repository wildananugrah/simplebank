docker build -t sim_billpayment:1.0 . 
# docker run -d --name sim_billpayment --net simplebank-net -p 9010:9010 sim_billpayment:1.0
docker run -d --name sim_billpayment -e mongodb://45.113.234.254:7000 -p 3010:9010 sim_billpayment:1.0