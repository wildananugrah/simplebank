docker build -t sim_interbank:1.0 . 
# docker run -d --name sim_interbank --net simplebank-net -p 9000:9000 sim_interbank:1.0
docker run -d --name sim_interbank -p 9000:9000 sim_interbank:1.0