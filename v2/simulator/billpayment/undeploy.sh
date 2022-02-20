docker network disconnect simplebank-net sim_billpayment
docker container stop sim_billpayment
docker container rm sim_billpayment
docker image rm sim_billpayment:1.0