docker run -d --name mongodb1 -p 6000:27017 --net mongo-net mongo mongod --replSet mongoSet
docker run -d --name mongodb2 -p 6002:27017 --net mongo-net mongo mongod --replSet mongoSet
docker run -d --name mongodb3 -p 6003:27017 --net mongo-net mongo mongod --replSet mongoSet
docker run -d --name mongodb4 -p 6004:27017 --net mongo-net mongo mongod --replSet mongoSet
docker run -d --name mongodb5 -p 6005:27017 --net mongo-net mongo mongod --replSet mongoSet

# config  = { "_id" : "mongoSet", members : [ { "_id" : 0, "host" : "192.168.1.139:6000" }, { "_id" : 1, "host" : "192.168.1.139:6001" }, { "_id" : 2, "host" : "192.168.1.139:6002" } ] }
# config  = { "_id" : "mongoSet", members : [ { "_id" : 0, "host" : "172.31.0.2:27017" }, { "_id" : 1, "host" : "172.31.0.3:27017" }, { "_id" : 2, "host" : "172.31.0.4:6002" } ] }

# docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mongodb1

# config = {
#    "_id":"mongoSet",
#    "members":[
#         {
#             "_id":0,
#             "host":"172.31.0.2:27017"
#         },
#         {
#             "_id":1,
#             "host":"172.31.0.3:27017"
#         },
#         {
#             "_id":2,
#             "host":"172.31.0.4:27017"
#         },
#         {
#             "_id":3,
#             "host":"172.31.0.5:27017"
#         },
#         {
#             "_id":4,
#             "host":"172.31.0.6:27017"
#         }
#     ]
# }