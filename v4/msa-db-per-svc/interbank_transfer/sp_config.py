import os

# MONGODB_HOST="mongodb://45.113.234.254:3000"
# SIM_INTERBANK_HOST="http://45.113.232.164:3000"
# SIM_BILLPAYMENT_HOST="http://45.113.232.164:3010"

TRANSACTION_HOST=os.getenv('TRANSACTION_HOST')
HISTORICAL_TRANSACTION_HOST=os.getenv('HISTORICAL_TRANSACTION_HOST')
ACCOUNT_HOST=os.getenv('ACCOUNT_HOST')
SIM_INTERBANK_HOST=os.getenv("SIM_INTERBANK_HOST")