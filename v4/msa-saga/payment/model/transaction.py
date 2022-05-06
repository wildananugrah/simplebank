from dataclasses import dataclass
from abc import ABC, abstractmethod
from exception.business_logic_exception import BusinessLogicException
from exception.service_exception import ServiceException
from uuid import uuid4
from datetime import datetime
from service.transaction import Transaction
from service.billpayment import EletricalBillPayment as EBPService
from database import session
from table.payment import TblPayment

import string, random


@dataclass
class EletricalBillPayment:

    """ represent eletrical bill payment entity """

    bill_id: str = None
    amount: int = 0
    description: str = None
    from_account_number: str = None
    cif_number: str = None
    payment: EBPService = EBPService()
    transaction: Transaction = Transaction()
    transaction_type: str = "ELECTRICAL_BILLPAYMENT"
    journal_number: str = None
    session = session

    def generate_transaction_id(self, size=10):
        try:
            transaction_id = ''.join(random.choice(string.digits) for _ in range(size))
            db_transaction_id = self.session.query(TblPayment).filter(TblPayment.transaction_id == transaction_id).first()
            if db_transaction_id is not None:
                self.generate_transaction_id()
            return transaction_id
        except BusinessLogicException as error:
            return transaction_id

    def inquiry(self, bill_id):
        return self.payment.inquiry(bill_id)

    def detail(self, transaction_id):
        try:
            payment = self.session.query(TblPayment).filter(TblPayment.transaction_id == transaction_id).first()
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
            transaction = self.session.query(TblPayment).filter(TblPayment.transaction_id == transaction_id).first()
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
            payment = self.detail(transaction_id)

            self.update(transaction_id, update_value)

            # invoke eletrical payment service
            self.payment.bill_id = payment['bill_id']
            self.payment.journal_number = update_value['journal_number']
            self.payment.description = payment['description']
            response = self.payment.pay()

        except ServiceException as error:
            raise ServiceException(f"Can not invoke eletrical payment service. detail: {error}")

        except Exception as error:
            raise Exception(f"Internal server error. detail {error}")

    def pay(self):
        try:
            transaction_datetime = datetime.now().strftime("%d-%m-%Y %H:%I%S")
                
            # invoke transaction to retrieve journal number.
            self.transaction.from_account_number = self.from_account_number
            self.transaction.transaction_type = self.transaction_type
            self.transaction.cif_number = self.cif_number
            self.transaction.amount = self.amount
            self.transaction.description = self.description
            self.transaction.transaction_id = self.generate_transaction_id()
            self.transaction.debit()

            payment = TblPayment(
                transaction_id=self.transaction.transaction_id,
                bill_id=self.bill_id,
                cif_number=self.cif_number,
                from_account_number=self.from_account_number,
                amount=self.amount,
                transaction_type=self.transaction_type,
                description=self.description
            )

            self.session.add(payment)
            self.session.commit()

            return self.transaction.transaction_id

        except ServiceException as error:
            self.transaction.from_account_number = self.from_account_number
            self.transaction.amount = self.amount
            self.transaction.journal_number = self.journal_number
            self.transaction.reversal()
            raise ServiceException(f"Can not invoke eletrical payment service. detail: {error}")

        except Exception as error:
            raise Exception(f"Internal server error. detail: {error}")