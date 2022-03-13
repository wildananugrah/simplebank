import os

# MONGODB_HOST="mongodb://45.113.235.79:5040"
# SIM_INTERBANK_HOST="http://45.113.232.164:3000"
# RABBIT_MQ_HOST="45.113.232.164"
# RABBIT_MQ_PORT="3020"

MONGODB_HOST=os.getenv("MONGODB_HOST")
SIM_INTERBANK_HOST=os.getenv("SIM_INTERBANK_HOST")
RABBIT_MQ_HOST=os.getenv("RABBIT_MQ_HOST")
RABBIT_MQ_PORT=os.getenv("RABBIT_MQ_PORT")