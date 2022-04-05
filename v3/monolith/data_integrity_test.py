from pymongo import MongoClient
from datetime import datetime
import json, random, string

start = datetime.now()

# client = MongoClient("mongodb://45.113.234.254:3000/") # monolith
client = MongoClient("mongodb://45.113.234.254:6000/?readPreference=primary&directConnection=true") # monolith
db = client.simplebank_db

db_accounts = list(db.accounts.find())
db_transactions = list(db.transactions.find())
db_historical_transactions = list(db.historical_transactions.find())

print(f"started at: {start}")

print("accounts")
accounts = []
for account in db_accounts:
    accounts.append({ account['account_number'] : int(account['balance']) })

print(f"db_accounts: {len(db_accounts)}")

end = datetime.now()
print(f"elapse time: {end - start}")

print("historical_transactions")
hist_trx_summ = []
for account in db_accounts:
    hist_trx = list(db.historical_transactions.find({ 'account_number' : account['account_number'] }))
    # print(f"account_number: {account['account_number']} : {len(hist_trx)}")
    hist_trx_summ.append({ account['account_number'] : len(hist_trx) })

end = datetime.now()
print(f"elapse time: {end - start}")

print("\n\ntransactions")
trx_summ = []
for account in db_accounts:
    hist_trx = list(db.transactions.find({"$or" : [{ 'from_account_number' : account['account_number'] }, { 'to_account_number' : account['account_number'] }]}))
    # print(f"account_number: {account['account_number']} : {len(hist_trx)}")
    trx_summ.append({ account['account_number'] : len(hist_trx) })

matched = [i for i, j in zip(hist_trx_summ, trx_summ) if i == j]
not_matched = [i for i, j in zip(hist_trx_summ, trx_summ) if i != j]

print(f"matched: {len(matched)}")
print(f"not matched: {len(not_matched)}")

end = datetime.now()
print(f"elapse time: {end - start}")

print("\n\naccount balances")

account_balances = []
for account in db_accounts:
    hist_trxs = list(db.historical_transactions.find({ 'account_number' : account['account_number'] }))
    balance = 0
    for hist_trx in hist_trxs:
        if hist_trx['transaction_type'] == "CREDIT":
            balance += int(hist_trx['amount'])
        elif hist_trx['transaction_type'] == "DEBIT":
            balance -= int(hist_trx['amount'])
    account_balances.append({ account['account_number'] : balance })

matched = [i for i, j in zip(account_balances, accounts) if i == j]
not_matched = [i for i, j in zip(account_balances, accounts) if i != j]

if len(not_matched) > 0:
    for account in accounts:
        if '5336277127' in account:
            print(account)
    print("NOT MATCHED!")
    print(not_matched)

print(f"matched: {len(matched)}")
print(f"not matched: {len(not_matched)}")

end = datetime.now()
print(f"elapse time: {end - start}")

print("\n\nSUMMARY")

print(f"accounts: {len(db_accounts)}")
print(f"transactions: {len(db_transactions)}")
print(f"historical-trx: {len(db_historical_transactions)}")




