import os

MONGODB_READ_HOST="mongodb://45.113.234.254:6060/?readPreference=secondary&directConnection=true"
MONGODB_WRITE_HOST="mongodb://45.113.234.254:6000/?readPreference=primary&directConnection=true"
SIM_BILLPAYMENT_HOST="http://45.113.232.164:3010"

# MONGODB_READ_HOST=os.getenv("MONGODB_READ_HOST")
# MONGODB_WRITE_HOST=os.getenv("MONGODB_WRITE_HOST")
# SIM_BILLPAYMENT_HOST=os.getenv("SIM_BILLPAYMENT_HOST")