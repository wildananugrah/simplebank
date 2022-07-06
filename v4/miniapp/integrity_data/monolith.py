from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import json

start = datetime.now()

engine = create_engine("postgresql+psycopg2://simplebankdb_user:simplebankdb_password@45.113.234.254:3000/simplebankdb") # monolith
Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()

class TblCustomer(Base):
   __tablename__ = 'customers'
   id = Column(Integer, primary_key=True)
   username = Column(String)
   password = Column(String)
   email = Column(String)
   cif_number = Column(String, unique=True, index=True)
   id_number = Column(String)
   name = Column(String)
   is_login = Column(Boolean)
   session_id = Column(String, default="")

   accounts = relationship("TblAccount", back_populates="customer")

class TblAccount(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    cif_number = Column(String, ForeignKey('customers.cif_number'))
    account_number = Column(String)
    currency = Column(String)
    balance = Column(Integer)

    customer = relationship("TblCustomer", back_populates="accounts")

class TblTransaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    transaction_type = Column(String)
    journal_number = Column(String)
    from_account_number = Column(String)
    to_account_number = Column(String)
    bank_code = Column(String)
    amount = Column(Integer)
    transaction_datetime = Column(DateTime, default=datetime.utcnow)
    cif_number = Column(String)
    status = Column(String)
    description = Column(String, default="")

class TblHistoricalTransaction(Base):
    __tablename__ = "historical_transactions"

    id = Column(Integer, primary_key=True)
    transaction_type = Column(String)
    account_number = Column(String)
    amount = Column(Integer)
    journal_number = Column(String)
    current_balance = Column(Integer)
    description = Column(String)
    transaction_datetime = Column(DateTime, default=datetime.utcnow)

db_accounts = session.query(TblAccount).all()
db_transactions = session.query(TblTransaction).all()
db_historical_transactions = session.query(TblHistoricalTransaction).all()

accounts = [{ x.account_number : x.balance } for x in db_accounts]
hist_trxs = [{ x.account_number : session.query(TblHistoricalTransaction).filter(TblHistoricalTransaction.account_number == x.account_number).count() } for x in db_accounts]
trxs = [{ x.account_number : session.query(TblTransaction).filter((TblTransaction.from_account_number == x.account_number) | (TblTransaction.to_account_number == x.account_number)).count() } for x in db_accounts]

print(f"count accounts: {len(accounts)}")
print(f"count hist_trx: {len(hist_trxs)}")
print(f"count trxs: {len(trxs)}")

matched = [i for i, j in zip(hist_trxs, trxs) if i == j]
not_matched = [i for i, j in zip(hist_trxs, trxs) if i != j]

print(f"matched: {len(matched)}")
print(f"not matched: {len(not_matched)}")

end = datetime.now()
print(f"elapse time: {end - start}")

def cal_account_balance(account_number):
    account_trxs = [{ 'amount': x.amount, 'transaction_type': x.transaction_type } for x in session.query(TblHistoricalTransaction).filter(TblHistoricalTransaction.account_number == account_number)]
    balance = 0
    for account_trx in account_trxs:
        if account_trx['transaction_type'] == 'CREDIT':
            balance += account_trx['amount']
        else:
            balance -= account_trx['amount']
    return balance

hist_account_balances = [{ x.account_number : cal_account_balance(x.account_number) } for x in db_accounts]

matched = [i for i, j in zip(accounts, hist_account_balances) if i == j]
not_matched = [i for i, j in zip(accounts, hist_account_balances) if i != j]

print(f"accounts: {accounts}")
print(f"historical_trx : {hist_account_balances}")

print(f"matched: {len(matched)}")
print(f"not matched: {len(not_matched)}")

end = datetime.now()
print(f"elapse time: {end - start}")