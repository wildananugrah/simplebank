from schemas.transaction import TransferOKSchema
from schemas.deposit import DepositOKSchema

class TransactionView():
    def transfer_response(self, from_account_number, to_account_number, journal_number, amount, timestamp):
        return TransferOKSchema(
            journal_number=journal_number,
            timestamp=timestamp,
            amount=amount,
            from_account_number=from_account_number,
            to_account_number=to_account_number
        ).dict()
    
    def deposit_response(self, account_number, journal_number, balance, timestamp):
        return DepositOKSchema(
            journal_number=journal_number,
            timestamp=timestamp,
            balance=balance,
            account_number=account_number
        ).dict()