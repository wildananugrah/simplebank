from dataclasses import dataclass
from abc import ABC, abstractmethod
from db import dbinstance
from exception.business_logic_exception import BusinessLogicException
from exception.service_exception import ServiceException
from uuid import uuid4
from datetime import datetime
from service.customer import Customer as CustomerService
import random, string

@dataclass
class Account:

    """ represent account master entity """

    account_number: str = None
    currency: str = None
    balance: int = 0
    customer: CustomerService = CustomerService()

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
        try:
            self.customer.detail(key_type="cif_number", value=cif_number)
        except ServiceException as error:
            raise BusinessLogicException(f"Can not find cif number: {cif_number} detail: {str(error)}")

        self.db.accounts.insert_one(data)
        return self.detail(account_number)

    def update(self, account_number, current_balance):
        self.detail(account_number)

        query = { 'account_number' : account_number }
        new_value = { 'balance' : current_balance }

        self.db.accounts.update_one(query, { '$set' : new_value })

        return self.detail(account_number)

    def settlement(self, from_account_number, to_account_number, amount):
        from_account_number = self.detail(from_account_number)
        to_account_number = self.detail(to_account_number)

        query = { 'account_number' : from_account_number }
        new_value = { 'balance' : from_account_number['balance'] - amount }

        self.db.accounts.update_one(query, { '$set' : new_value })

        query = { 'account_number' : to_account_number }
        new_value = { 'balance' : to_account_number['balance'] + amount }

        self.db.accounts.update_one(query, { '$set' : new_value })

        return True

    def update_many(self, documents):

        try:
            for document in documents:
                self.update(document['account_number'], document['current_balance'])
            
            return True
        except Exception as error:
            print(f"ERROR: {error}")

    def delete(self, account_number):
        self.detail(account_number)
        self.db.accounts.delete_one({ 'account_number' : account_number })
        return True

    def list(self, cif_number, skip, limit):
        return list(self.db.accounts.find({ 'cif_number' : cif_number}, { '_id' : False }).skip(int(skip)).limit(int(limit)))
