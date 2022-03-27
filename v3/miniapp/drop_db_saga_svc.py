from pymongo import MongoClient

client_customer = MongoClient("mongodb://45.113.234.254:5000/")
client_account = MongoClient("mongodb://45.113.234.254:5010/")
client_transaction   = MongoClient("mongodb://45.113.234.254:5020/")
client_hist = MongoClient("mongodb://45.113.234.254:5030/")
client_interbank_transfer = MongoClient("mongodb://45.113.234.254:5040/")
client_payment = MongoClient("mongodb://45.113.234.254:5050/")

# db = client.simplebank_db
client_account.simplebank_db.accounts.delete_many({})
client_hist.simplebank_db.historical_transactions.delete_many({})
client_transaction.simplebank_db.transactions.delete_many({})
client_payment.simplebank_db.payments.delete_many({})
client_payment.simplebank_db.interbank_transfers.delete_many({})
print("DONE.")