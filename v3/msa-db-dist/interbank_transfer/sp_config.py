import os

# MONGODB_READ_HOST="mongodb://45.113.235.79:6050/?readPreference=secondary&directConnection=true"
# MONGODB_WRITE_HOST="mongodb://45.113.235.79:6000/?readPreference=primary&directConnection=true"
# SIM_INTERBANK_HOST="http://45.113.232.164:3000"

MONGODB_READ_HOST=os.getenv("MONGODB_READ_HOST")
MONGODB_WRITE_HOST=os.getenv("MONGODB_WRITE_HOST")
SIM_INTERBANK_HOST=os.getenv("SIM_INTERBANK_HOST")