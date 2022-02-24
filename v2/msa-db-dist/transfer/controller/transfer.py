from model.transfer import *
from view.transfer import *
import random, string

class TransferController():
    def __init__(self):
        self.model = TransferModel()
        self.view = TransferView()

    def inquiry_interbank_account_number(self, account_number, bank_code):
        result = self.model.inquiry_interbank_account_number(account_number, bank_code)
        return self.view.detail(result.json(), result.status_code)
    
    def save_account_number(self, json_request):
        cif_number = json_request['cif_number']
        account_number = json_request['account_number']
        bank_code = json_request['bank_code']
        self.model.save_account_number(cif_number, account_number, bank_code)

        return self.view.detail({ 'cif_number' : cif_number, 'account_number' : account_number, 'bank_code' : bank_code})

    def delete_account_number(self, cif_number, account_number, bank_code):
        if self.model.detail_interbank_account_number(cif_number, account_number, bank_code):
            self.model.delete_account_number(cif_number, account_number, bank_code)
            return self.view.delete_success()
        else:
            return self.view.not_found_account_number()

    def list_account_number(self, cif_number):
        saved_accounts = self.model.list_account_number(cif_number)
        accounts = []
        for account in saved_accounts:
            accounts.append(account)

        return self.view.list(accounts)
    
    def detail(self, transaction_id):
        return self.view.detail(self.model.detail(transaction_id))

    def transfer_account_number(self, json_request):
        # check balance
        # current balance = from account balance + to account balance
        # from account balance = from acount balance - amount
        # to account balanace = to account balance + amount
        # current balance == from account balance + to account balance
        # update balance
        # get detail balance 
        # current balance == db from account balance + db to account balance

        from_account_number = json_request['from_account_number'] 
        to_account_number = json_request['to_account_number'] 
        amount = json_request['amount'] 
        description = json_request['description']
        cif_number = json_request['cif_number']
        
        data = json_request
        message = None

        db_from_account_number = self.model.detail_account_number(from_account_number)

        if db_from_account_number == None:
            return self.view.detail({ 'message' : 'from account number is not found' }, 400)

        if db_from_account_number['balance'] < amount:
            return self.view.unsufficient_account()
        
        db_to_account_number = self.model.detail_account_number(to_account_number)

        if db_to_account_number == None:
            return self.view.detail({ 'message' : 'to account number is not found' }, 400)

        current_balance = db_from_account_number['balance'] + db_to_account_number['balance']

        from_account_number_balance = db_from_account_number['balance'] - amount
        to_account_number_balance = db_to_account_number['balance'] + amount

        if current_balance == (from_account_number_balance + to_account_number_balance):
            transaction_id = self.generate_transaction_id(from_account_number)
            journal_number = self.generate_journal_number(from_account_number)

            self.model.update_account_number_balance(from_account_number, from_account_number_balance)
            self.model.update_account_number_balance(to_account_number, to_account_number_balance)

            self.model.add_historical_transaction(from_account_number, amount, "DEBIT", journal_number, transaction_id, "TRANSFER", description)
            self.model.add_historical_transaction(to_account_number, amount, "CREDIT", journal_number, transaction_id, "TRANSFER", description)

            self.model.save_transfer(cif_number, from_account_number, to_account_number, "009", amount, transaction_id, description, "DONE")

            return self.view.detail({ "message" : "amount has been transfered successfully" }, 201)

        else:
            self.model.save_transfer(cif_number, from_account_number, to_account_number, "009", amount, transaction_id, description, "SETTLEMENT_FAILED")
            return self.view.detail({ "message" :  "update balance error!" }, 500)

        return self.view.detail({ 'message' : message, 'data' : data }, status_code)

    def transfer_interbank_account_number(self, json_request):
        from_account_number = json_request['from_account_number'] 
        to_account_number = json_request['to_account_number'] 
        amount = json_request['amount'] 
        description = json_request['description']
        bank_code = json_request['bank_code']
        cif_number = json_request['cif_number']

        data = json_request
        message = None

        db_from_account_number = self.model.detail_account_number(from_account_number)

        if db_from_account_number == None:
            return self.view.detail({ 'message' : 'from account number is not found' }, 400)

        if db_from_account_number['balance'] < amount:
            return self.view.unsufficient_account()

        notify_result = self.model.notify_interbank(from_account_number, "009", to_account_number, bank_code, amount, description)
        transaction_id = self.generate_transaction_id(from_account_number)
        if notify_result.status_code in (200, 201):
            journal_number = self.generate_journal_number(from_account_number)
            self.model.update_account_number_balance(from_account_number, db_from_account_number['balance'] - amount)
            self.model.add_historical_transaction(from_account_number, amount, "DEBIT", journal_number, transaction_id, "TRANSFER", description)

            self.model.save_transfer(cif_number, from_account_number, to_account_number, bank_code, amount, transaction_id, description, "DONE")
            return self.view.detail({ "message" : "interbank transfer has been executed successfully" }, 201)
        else:
            self.model.save_transfer(cif_number, from_account_number, to_account_number, bank_code, amount, transaction_id, description, "NOTIFY_FAILED")
            return self.view.detail({ "message" : "interbank transfer is failed" }, 500)

    def list(self, cif_number):
        transfer_list = self.model.list(cif_number)
        _transfer_list = []

        for transfer in transfer_list:
            _transfer_list.append(transfer)

        return self.view.list(_transfer_list)

    def generate_transaction_id(self, account_number, size=10):
        transaction_id = ''.join(random.choice(string.digits) for _ in range(size))
        db_transaction_id = self.model.find_transaction_id(transaction_id, account_number)
        if db_transaction_id:
            self.generate_transaction_id(account_number)
        return transaction_id

    def generate_journal_number(self, account_number, size=6):
        journal_number = ''.join(random.choice(string.digits) for _ in range(size))
        db_journal_number = self.model.find_journal_number(journal_number, account_number)
        if db_journal_number:
            self.generate_journal_number(account_number)
        return journal_number
