from dataclasses import dataclass
from abc import ABC, abstractmethod
from exception.business_logic_exception import BusinessLogicException
from uuid import uuid4
from datetime import datetime
from service.customer import Customer
from table.account import TblAccount
from database import session
import random, string

@dataclass
class Account:

    """ represent account master entity """

    account_number: str = None
    currency: str = None
    balance: int = 0
    customer: Customer = Customer()
    session = session

    def generate_account_number(self, size=10):
        account_number = ''.join(random.choice(string.digits) for _ in range(size))

        try:
            db_account_number = self.session.query(TblAccount).filter(TblAccount.account_number == account_number).first()
            if db_account_number:
                self.generate_account_number()
            return account_number
        except BusinessLogicException as error:
            return account_number

    def detail(self, account_number):
        account = self.session.query(TblAccount).filter(TblAccount.account_number == account_number).first()
        if account:
            return {
                "account_number" : account.account_number,
                "currency" : account.currency,
                "balance" : account.balance,
                "cif_number" : account.cif_number
            }
        else:
            raise BusinessLogicException(f'Can not find account_number: {account_number}')
    
    def create(self, cif_number, currency = 'IDR', balance = 0):
        self.customer.detail(key_type="cif_number", value=cif_number)
        
        account_number = self.generate_account_number()
        account = TblAccount(account_number=account_number, currency=currency, balance=balance, cif_number=cif_number)
        self.session.add(account)
        self.session.commit()
        return self.detail(account_number)

    def update(self, account_number, current_balance):
        self.detail(account_number)

        account = self.session.query(TblAccount).filter(TblAccount.account_number == account_number).first()
        account.balance = current_balance
        self.session.commit()
        
        return self.detail(account_number)

    def delete(self, account_number):
        account = self.session.query(TblAccount).filter(TblAccount.account_number == account_number).first()

        if account is None:
            raise BusinessLogicException(f'Can not find account_number: {account_number}')

        self.session.delete(account)
        self.session.commit()
        return True

    def list(self, cif_number, skip, limit):
        accounts = self.session.query(TblAccount).filter(TblAccount.cif_number == cif_number).offset(skip).limit(limit)
        
        data = []
        for account in accounts:
            data.append({
                'account_number' : account.account_number,
                'balance' : account.balance,
                'cif_number' : account.cif_number,
                'currency' : account.currency
            })
        return data