from dataclasses import dataclass
from abc import ABC, abstractmethod
from exception.business_logic_exception import BusinessLogicException
from uuid import uuid4
from datetime import datetime
from service.account import Account
from service.interbank import Interbank
from service.transaction import Transaction as ServiceTransaction
from table.interbank_transfer import TblInterbankTransfer
from database import session

import random, string

@dataclass
class Transaction:

    """ represent transaction master entity """

    account: Account = Account()

    # def save(self, data):
    #     try:
    #         self.db.interbank_transfers.insert_one(data)
    #         return True
    #     except Exception as error:
    #         Exception(f"Internal server error: {str(error)}")

@dataclass
class TransferInterbank(Transaction):

    """ represent transaction in other bank system entity """
    
    from_account_number: str = None
    to_account_number: str = None
    to_bank_code: str = None
    amount: int = 0
    description: str = None
    cif_number: str = None
    transaction: ServiceTransaction = ServiceTransaction()
    session = session

    def generate_transaction_id(self, size=10):
        try:
            transaction_id = ''.join(random.choice(string.digits) for _ in range(size))
            db_transaction_id = self.session.query(TblInterbankTransfer).filter(TblInterbankTransfer.transaction_id == transaction_id).first()
            if db_transaction_id is not None:
                self.generate_transaction_id()
            return transaction_id
        except BusinessLogicException as error:
            return transaction_id

    def inquiry(self, to_account_number, to_bank_code):
        return Interbank().inquiry(to_account_number, to_bank_code)

    def detail(self, transaction_id):
        try:
            payment = self.session.query(TblInterbankTransfer).filter(TblInterbankTransfer.transaction_id == transaction_id).first()
            if payment:
                payment = payment.__dict__
                del payment['_sa_instance_state']
                return payment
            else:
                raise BusinessLogicException(f'Can not find transaction_id: {transaction_id}')
        except Exception as error:
            raise Exception(f"Internal server error. detail {error}")

    def update(self, transaction_id, update_value):
        try:
            transaction = self.session.query(TblInterbankTransfer).filter(TblInterbankTransfer.transaction_id == transaction_id).first()
            if transaction:
                transaction.status = update_value['status']
                transaction.journal_number = update_value['journal_number']
                transaction.message = update_value['message']
                self.session.commit()
                return True
            else:
                raise BusinessLogicException(f'Can not find transaction_id: {transaction_id}')
        except Exception as error:
            raise Exception(f"Internal server error. detail {error}")
            
    def notify(self, transaction_id, update_value):
        try:
            interbank_transfer = self.detail(transaction_id)

            self.update(transaction_id, update_value)

            # request notify to interbank 
            interbank = Interbank(acccount_number=self.from_account_number, 
                        amount=self.amount, 
                        bank_code=self.to_bank_code, 
                        description=self.description, 
                        journal_number=self.transaction.transaction_id,
                        transaction_datetime=datetime.now().strftime("%d-%m-%Y %H:%I%S"))
        
            response = interbank.notify()

        except ServiceException as error:
            raise ServiceException(f"Can not invoke interbank transfer service. detail: {error}")

        except Exception as error:
            raise Exception(f"Internal server error. detail {error}")

    def transfer(self):
        db_from_account_number = self.account.detail(self.from_account_number)

        self.transaction.transaction_id = self.generate_transaction_id()
        self.transaction.to_account_number = self.to_account_number
        self.transaction.bank_code = self.to_bank_code
        self.transaction.from_account_number = self.from_account_number
        self.transaction.transaction_type = "INTERBANK"
        self.transaction.cif_number = self.cif_number
        self.transaction.amount = self.amount
        self.transaction.description = self.description
        self.transaction.debit()

        interbank_transfer = TblInterbankTransfer(
            transaction_id=self.transaction.transaction_id,
            from_account_number=self.from_account_number,
            from_bank_code="009",
            to_account_number=self.to_account_number,
            to_bank_code=self.to_bank_code,
            amount=self.amount,
            cif_number=self.cif_number,
            description=self.description
        )

        self.session.add(interbank_transfer)
        self.session.commit()

        return self.transaction.transaction_id