from dataclasses import dataclass
from abc import ABC, abstractmethod
from db import dbinstance
from exception.business_logic_exception import BusinessLogicException
from uuid import uuid4
from datetime import datetime
from service.account import Account
from service.historical_transaction import HistoricalTransaction

import random, string

@dataclass
class Transaction:

    """ represent transaction master entity """

    journal_number: str = None
    account: Account = Account()
    historical_transaction: HistoricalTransaction = HistoricalTransaction()
    db = dbinstance.get_db().simplebank_db

    def generate_journal_number(self, acccount_number, size=10):
        journal_number = ''.join(random.choice(string.digits) for _ in range(size))

        try:
            db_journal_number = self.detail(acccount_number, journal_number)
            if db_journal_number or journal_number[0] == '0':
                self.generate_journal_number(acccount_number)
            return journal_number
        except BusinessLogicException as error:
            return journal_number

    def detail(self, account_number, journal_number):
        return self.db.transactions.find_one({ 'account_number' : account_number, 'journal_number' : journal_number }, { '_id' : False })
    
    def list(self, cif_number, skip, limit):
        return list(self.db.transactions.find({'cif_number' : cif_number}, { '_id' : False }).skip(int(skip)).limit(int(limit)).sort('transaction_datetime', -1)) # descending

    def save(self, transaction_type, from_account_number, to_account_number, to_bank_code, amount, journal_number, cif_number, status, description=""):
        data = {
            'transaction_type': transaction_type,
            'journal_number' : journal_number,
            'from_account_number': from_account_number, 
            'to_account_number': to_account_number, 
            'bank_code' : to_bank_code,
            'amount': amount,
            'transaction_datetime' : datetime.today().replace(microsecond=0),
            'cif_number' : cif_number,
            'status' : status,
            'description': description
        }

        self.db.transactions.insert_one(data)

        return True
    
    def store_to_historical_transaction(self, transaction_type, account_number, amount, journal_number, current_balance, description = ""):
        self.historical_transaction.transaction_type = transaction_type
        self.historical_transaction.account_number = account_number
        self.historical_transaction.amount = amount
        self.historical_transaction.journal_number = journal_number
        self.historical_transaction.current_balance = current_balance
        self.historical_transaction.description = description
        self.historical_transaction.save()
        return True

    def deposit(self, account_number, amount):
        account = self.account.detail(account_number)
        account_update_balance = account['balance'] + amount
        to_account_number_update_balance = self.account.update(account_number, account_update_balance)['balance']
        journal_number = self.generate_journal_number(account_number)
        self.save(transaction_type="DEPOSIT", 
                from_account_number=account_number, 
                to_account_number=account_number, 
                to_bank_code="009", 
                amount=amount, 
                journal_number=journal_number, 
                cif_number=account['cif_number'], 
                status="DONE")
        self.store_to_historical_transaction(transaction_type="CREDIT", account_number=account_number, amount=amount, journal_number=journal_number, current_balance=to_account_number_update_balance)
            
        return journal_number
    
    def reversal(self, account_number, amount, journal_number):
        try:
            account = self.account.detail(account_number)
            account_update_balance = account['balance'] + amount
            to_account_number_update_balance = self.account.update(account_number, account_update_balance)['balance']
            self.save(transaction_type="REVERSAL", 
                    from_account_number=account_number, 
                    to_account_number=account_number, 
                    to_bank_code="009", 
                    amount=amount, 
                    journal_number=journal_number, 
                    cif_number=account['cif_number'], 
                    status="DONE")
                    
            self.store_to_historical_transaction(transaction_type="REVERSAL", account_number=account_number, amount=amount, journal_number=journal_number, current_balance=to_account_number_update_balance)
                
            return journal_number
        except Exception as error:
            raise BusinessLogicException(f"Can not reversal. detail: {error}")

    def detail_transaction(self, transaction_type, account_number, journal_number):

        if transaction_type not in ['DEPOSIT', 'INTERBANK', 'INTRABANK', 'ELECTRICAL_BILLPAYMENT']:
            raise BusinessLogicException("Invalid transaction type.")
        query = { 'transaction_type' : transaction_type, 'from_account_number' : account_number, 'journal_number' : journal_number }
        detail = self.db.transactions.find_one(query, { '_id' : False })
        if detail is None:
            raise BusinessLogicException(f"Can not find: trx_type: {transaction_type} account_number: {account_number} journal_number: {journal_number}")
        return detail

@dataclass
class TransferIntrabank(Transaction):

    from_account_number: str = None
    to_account_number: str = None
    cif_number: str = None
    description: str = None
    amount: int = 0

    """ represent transaction in own bank system entity """

    def transfer(self):
        db_to_account_number = self.account.detail(self.to_account_number)
        if db_to_account_number is None:
            raise BusinessLogicException(f"Invalid to_account_number: {self.to_account_number}")

        db_from_account_number = self.account.detail(self.from_account_number)
        if db_from_account_number is None:
            raise BusinessLogicException(f"Invalid from_account_number: {self.from_account_number}")

        if db_from_account_number['balance'] < self.amount:
            raise BusinessLogicException(f"Unsufficient fund from_account_number: {self.from_account_number}")

        to_account_number_current_balance =  db_to_account_number['balance'] + self.amount # credit
        from_account_number_current_balance =  db_from_account_number['balance'] - self.amount # debit

        total_current_balance = db_to_account_number['balance'] + db_from_account_number['balance']

        to_account_number_update_balance = self.account.update(self.to_account_number, to_account_number_current_balance)['balance']
        from_account_number_update_balance = self.account.update(self.from_account_number, from_account_number_current_balance)['balance']
        journal_number = self.generate_journal_number(self.from_account_number)

        if total_current_balance == (to_account_number_update_balance + from_account_number_update_balance):
            self.save(transaction_type="INTRABANK", 
                        from_account_number=self.from_account_number, 
                        to_account_number=self.to_account_number, 
                        to_bank_code="009", 
                        amount=self.amount, 
                        journal_number=journal_number, 
                        cif_number=self.cif_number, 
                        description=self.description,
                        status="DONE")

            self.store_to_historical_transaction(transaction_type="DEBIT", account_number=self.from_account_number, amount=self.amount, journal_number=journal_number, current_balance=from_account_number_update_balance, description=self.description)
            self.store_to_historical_transaction(transaction_type="CREDIT", account_number=self.to_account_number, amount=self.amount, journal_number=journal_number, current_balance=to_account_number_update_balance, description=self.description)
            
            return journal_number
        else:
            raise BusinessLogicException(f"Invalid settlement: {total_current_balance} is not {(to_account_number_update_balance + from_account_number_update_balance)}")
        

@dataclass
class DebitTransaction(Transaction):

    """ represent transaction in other bank system entity """
    
    from_account_number: str = None
    amount: int = 0
    description: str = None
    cif_number: str = None
    transaction_type: str = None

    def debit(self):
        try:
            db_from_account_number = self.account.detail(self.from_account_number)

            if db_from_account_number['balance'] < self.amount:
                raise BusinessLogicException(f"Unsufficient fund from_account_number: {self.from_account_number}")

            from_account_number_current_balance =  db_from_account_number['balance'] - self.amount # debit

            from_account_number_update_balance = self.account.update(self.from_account_number, from_account_number_current_balance)['balance']

            journal_number = self.generate_journal_number(self.from_account_number)


            self.save(transaction_type=self.transaction_type, 
                    from_account_number=self.from_account_number, 
                    to_account_number=None, 
                    to_bank_code=None,
                    amount=self.amount, 
                    journal_number=journal_number, 
                    cif_number=self.cif_number, 
                    description=self.description,
                    status="DONE")

            self.store_to_historical_transaction(transaction_type="DEBIT", account_number=self.from_account_number, amount=self.amount, journal_number=journal_number, current_balance=from_account_number_update_balance,description=self.description)

            return journal_number
        except Exception as error:
            raise BusinessLogicException(f"Can not debit account. detail {error}")
