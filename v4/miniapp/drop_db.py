from pymongo import MongoClient

client = MongoClient("mongodb://45.113.234.254:6000/?readPreference=primary&directConnection=true") # monolith
db = client.simplebank_db
db.accounts.delete_many({})
db.historical_transactions.delete_many({})
db.transactions.delete_many({})
db.payments.delete_many({})
db.interbank_transfers.delete_many({})
print("DONE.")