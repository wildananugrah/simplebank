from models.transaction import TransactionModel
from models.account import AccountModel
from models.historical_transaction import HistoricalTransactionModel
from views.transaction import TransactionView
from schemas.transaction import TransferSchema
from schemas.deposit import DepositSchema
from fastapi import HTTPException
from datetime import datetime

import random, string

class TransactionController():
    def __init__(self, db):
        self.model = TransactionModel(db)
        self.view = TransactionView()
        self.db = db

    def transfer(self, transfer: TransferSchema):

        account_model = AccountModel(self.db)
        historical_transaction_model = HistoricalTransactionModel()
        db_from_account = account_model.detail(transfer.from_account_number)
        db_to_account = account_model.detail(transfer.to_account_number)

        if not db_from_account:
            raise HTTPException(status_code=400, detail="Invalid from account")

        if not db_to_account:
            raise HTTPException(status_code=400, detail="Invalid to account")

        if db_from_account.balance < transfer.amount:
            raise HTTPException(status_code=400, detail="Unsufficient balance")

        journal_number = historical_transaction_model.generate_journal_number()
        timestamp = datetime.utcnow()

        if self.model.transfer(from_account_number=transfer.from_account_number, 
                            db_from_account_number=db_from_account, 
                            to_account_number=transfer.to_account_number, 
                            db_to_account_number=db_to_account, 
                            journal_number=journal_number, 
                            amount=transfer.amount, 
                            timestamp=timestamp):

            return self.view.transfer_response(
                from_account_number=transfer.from_account_number, 
                to_account_number=transfer.to_account_number, 
                journal_number=journal_number, 
                amount=transfer.amount, 
                timestamp=timestamp
            )
        else:
            raise HTTPException(status_code=500, detail="ERROR TRANSFER")

    def deposit(self, deposit: DepositSchema):
        account_model = AccountModel(self.db)
        historical_transaction_model = HistoricalTransactionModel()
        db_account = account_model.detail(deposit.account_number)

        if not db_account:
            raise HTTPException(status_code=400, detail="Invalid account")

        journal_number = historical_transaction_model.generate_journal_number()
        timestamp = datetime.utcnow()

        if self.model.deposit(account_number=deposit.account_number, 
                                db_account_number=db_account, 
                                journal_number=journal_number, 
                                amount=deposit.amount, 
                                timestamp=timestamp):
            return self.view.deposit_response(
                account_number=deposit.account_number,  
                journal_number=journal_number, 
                balance=db_account.balance, 
                timestamp=timestamp
            )
        else:
            raise HTTPException(status_code=500, detail="ERROR DEPOSIT")