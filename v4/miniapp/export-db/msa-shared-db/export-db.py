from pymongo import MongoClient
from datetime import datetime
import json, random, string

start = datetime.now()

client = MongoClient("mongodb://45.113.234.254:3000/")
db = client.simplebank_db

db_accounts = list(db.accounts.find({}, {'_id' : False}))
db_transactions = list(db.transactions.find({}, {'_id' : False}))
db_historical_transactions = list(db.historical_transactions.find({}, {'_id' : False}))
db_payments = list(db.payments.find({}, {'_id' : False}))
db_interbank_transfer = list(db.interbank_transfers.find({}, {'_id' : False}))

print("db_accounts")
with open("db_accounts.json", "w") as f:
    f.write(json.dumps(db_accounts, indent=4, sort_keys=True, default=str))

end = datetime.now()
print(f"elapse time: {end - start}")

print("db_transactions")
with open("db_transactions.json", "w") as f:
    f.write(json.dumps(db_transactions, indent=4, sort_keys=True, default=str))

end = datetime.now()
print(f"elapse time: {end - start}")

print("db_historical_transactions")
with open("db_historical_transactions.json", "w") as f:
    f.write(json.dumps(db_historical_transactions, indent=4, sort_keys=True, default=str))

end = datetime.now()
print(f"elapse time: {end - start}")

print("db_payments")
with open("db_payments.json", "w") as f:
    f.write(json.dumps(db_payments, indent=4, sort_keys=True, default=str))

end = datetime.now()
print(f"elapse time: {end - start}")

print("db_interbank_transfer")
with open("db_interbank_transfer.json", "w") as f:
    f.write(json.dumps(db_interbank_transfer, indent=4, sort_keys=True, default=str))

end = datetime.now()
print(f"elapse time: {end - start}")




