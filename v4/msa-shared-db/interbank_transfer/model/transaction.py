from dataclasses import dataclass
from abc import ABC, abstractmethod
from exception.business_logic_exception import BusinessLogicException
from uuid import uuid4
from datetime import datetime
from model.account import Account
from model.historical_transaction import HistoricalTransaction
from service.interbank import Interbank
from database import session
from table.transaction import TblTransaction
from sqlalchemy import and_

import random, string

@dataclass
class Transaction:

    """ represent transaction master entity """

    journal_number: str = None
    account: Account = Account()
    historical_transaction: HistoricalTransaction = HistoricalTransaction()
    session = session

    def generate_journal_number(self, account_number, size=10):
        journal_number = ''.join(random.choice(string.digits) for _ in range(size))

        try:
            db_journal_number = self.session.query(TblTransaction).filter(and_(TblTransaction.from_account_number == account_number, TblTransaction.journal_number == journal_number)).first()
            if db_journal_number is not None:
                self.generate_journal_number(account_number)
            return journal_number
        except BusinessLogicException as error:
            return journal_number

    def detail(self, account_number, journal_number):
        transaction = self.session.query(TblTransaction).filter(and_(TblTransaction.from_account_number == account_number, TblTransaction.journal_number == journal_number)).first()
        return {
            'transaction_type': transaction.transaction_type,
            'journal_number' : transaction.journal_number,
            'from_account_number': transaction.from_account_number, 
            'to_account_number': transaction.to_account_number, 
            'bank_code' : transaction.bank_code,
            'amount': transaction.amount,
            'transaction_datetime' : transaction.transaction_datetime,
            'cif_number' : transaction.cif_number,
            'status' : transaction.status,
            'description': transaction.description
        }
    
    def list(self, cif_number, skip, limit):
        transactions = self.session.query(TblTransaction).filter(TblTransaction.cif_number == cif_number).offset(skip).limit(limit).order_by(TblTransaction.transaction_datetime.desc())
        data = []
        for transaction in transactions:
            data.append({
                'transaction_type': transaction.transaction_type,
                'journal_number' : transaction.journal_number,
                'from_account_number': transaction.from_account_number, 
                'to_account_number': transaction.to_account_number, 
                'bank_code' : transaction.bank_code,
                'amount': transaction.amount,
                'transaction_datetime' : transaction.transaction_datetime,
                'cif_number' : transaction.cif_number,
                'status' : transaction.status,
                'description': transaction.description
            })
        return data

    def save(self, transaction_type, from_account_number, to_account_number, to_bank_code, amount, journal_number, cif_number, status, description=""):
        
        transaction = TblTransaction(
            transaction_type=transaction_type,
            journal_number=journal_number,
            from_account_number=from_account_number,
            to_account_number=to_account_number,
            bank_code=to_bank_code,
            amount=amount,
            cif_number=cif_number,
            status=status,
            description=description
        )

        self.session.add(transaction)
        self.session.commit()

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
        journal_number = "123456"
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
    
    def detail_transaction(self, transaction_type, account_number, journal_number):

        if transaction_type not in ['DEPOSIT', 'INTERBANK', 'INTRABANK', 'ELETRICAL_BILLPAYMENT']:
            raise BusinessLogicException("Invalid transaction type.")
        query = { 'transaction_type' : transaction_type, 'from_account_number' : account_number, 'journal_number' : journal_number }
        detail = self.session.query(TblTransaction).filter(and_(TblTransaction.transaction_type == transaction_type, TblTransaction.from_account_number == account_number, TblTransaction.journal_number == journal_number)).first()
        if detail is None:
            raise BusinessLogicException(f"Can not find: trx_type: {transaction_type} account_number: {account_number} journal_number: {journal_number}")
        detail = detail.__dict__
        del detail['_sa_instance_state']
        return detail

@dataclass
class TransferInterbank(Transaction):

    """ represent transaction in other bank system entity """
    
    from_account_number: str = None
    to_account_number: str = None
    to_bank_code: str = None
    amount: int = 0
    description: str = None
    cif_number: str = None

    def inquiry(self, to_account_number, to_bank_code):
        return Interbank().inquiry(to_account_number, to_bank_code)

    def transfer(self):
        db_from_account_number = self.account.detail(self.from_account_number)
        if db_from_account_number is None:
            raise BusinessLogicException(f"Invalid from_account_number: {self.from_account_number}")

        if db_from_account_number['balance'] < self.amount:
            raise BusinessLogicException(f"Unsufficient fund from_account_number: {self.from_account_number}")

        from_account_number_current_balance =  db_from_account_number['balance'] - self.amount # debit

        from_account_number_update_balance = self.account.update(self.from_account_number, from_account_number_current_balance)['balance']

        journal_number = self.generate_journal_number(self.from_account_number)

        # request notify to interbank 
        interbank = Interbank(acccount_number=self.from_account_number, 
                        amount=self.amount, 
                        bank_code=self.to_bank_code, 
                        description=self.description, 
                        journal_number=journal_number,
                        transaction_datetime=datetime.now().strftime("%d-%m-%Y %H:%I%S"))
        
        response = interbank.notify()

        self.save(transaction_type="INTERBANK", 
                from_account_number=self.from_account_number, 
                to_account_number=self.to_account_number, 
                to_bank_code=self.to_bank_code, 
                amount=self.amount, 
                journal_number=journal_number, 
                cif_number=self.cif_number, 
                description=self.description,
                status="DONE")

        self.store_to_historical_transaction(transaction_type="DEBIT", account_number=self.from_account_number, amount=self.amount, journal_number=journal_number, current_balance=from_account_number_update_balance,description=self.description)

        return journal_number