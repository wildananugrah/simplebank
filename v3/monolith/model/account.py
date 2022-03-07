from dataclasses import dataclass
from abc import ABC, abstractmethod
from db import dbinstance
from exception.business_logic_exception import BusinessLogicException
from uuid import uuid4
from datetime import datetime
import random, string

class AccountAbstract(ABC):

    """ represent base account """

    @abstractmethod
    def detail(self, account_number):
        raise NotImplementedError("detail is not implemented.")

    @abstractmethod
    def create(self, cif_number, currency = 'IDR', balance = 0):
        raise NotImplementedError("create is not implemented.")

    @abstractmethod
    def delete(self, account_number):
        raise NotImplementedError("delete is not implemented.")

    @abstractmethod
    def list(self, cif_number):
        raise NotImplementedError("list is not implemented.")

    @abstractmethod
    def generate_account_number(self, size=0):
        raise NotImplementedError("generate_account_number is not implemented.")

@dataclass
class Account:

    """ represent account master entity """

    account_number: str = None
    currency: str = None
    balance: int = 0

    db = dbinstance.get_db().simplebank_db

    def generate_account_number(self, size=10):
        account_number = ''.join(random.choice(string.digits) for _ in range(size))

        try:
            db_account_number = self.detail(account_number)
            if db_account_number or account_number[0] == '0':
                self.generate_account_number()
            return account_number
        except BusinessLogicException as error:
            return account_number

    def detail(self, account_number):
        account = self.db.accounts.find_one({ 'account_number' : account_number }, { '_id' : False })
        if account:
            return account
        else:
            raise BusinessLogicException(f'Can not find account_number: {account_number}')
    
    def create(self, cif_number, currency = 'IDR', balance = 0):
        account_number = self.generate_account_number()
        data = {
            'account_number' : account_number,
            'currency' : currency,
            'balance' : balance,
            'cif_number': cif_number
        }
        self.db.accounts.insert_one(data)
        return self.detail(account_number)

    def update(self, account_number, current_balance):
        self.detail(account_number)

        query = { 'account_number' : account_number }
        new_value = { 'balance' : current_balance }

        self.db.accounts.update_one(query, { '$set' : new_value })

        return self.detail(account_number)

    def delete(self, account_number):
        self.detail(account_number)
        self.db.accounts.delete_one({ 'account_number' : account_number })
        return True

    def list(self, cif_number):
        return list(self.db.accounts.find({ 'cif_number' : cif_number}, { '_id' : False }))