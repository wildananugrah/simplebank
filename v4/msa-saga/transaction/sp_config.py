import os

# MONGODB_HOST="mongodb://45.113.234.254:3000"
# SIM_INTERBANK_HOST="http://45.113.232.164:3000"
# SIM_BILLPAYMENT_HOST="http://45.113.232.164:3010"

DATABASE_CONN_STR=os.getenv('DATABASE_CONN_STR')
ACCOUNT_HOST=os.getenv('ACCOUNT_HOST')
HISTORICAL_TRANSACTION_HOST=os.getenv('HISTORICAL_TRANSACTION_HOST')
RABBIT_MQ_HOST=os.getenv("RABBIT_MQ_HOST")
RABBIT_MQ_PORT=os.getenv("RABBIT_MQ_PORT")