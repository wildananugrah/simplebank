import os

# MONGODB_HOST="mongodb://45.113.234.254:3000"
# SIM_INTERBANK_HOST="http://45.113.232.164:3000"

MONGODB_HOST=os.getenv("MONGODB_HOST")
SIM_INTERBANK_HOST=os.getenv("SIM_INTERBANK_HOST")