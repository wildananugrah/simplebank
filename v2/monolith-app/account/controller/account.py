from account.model.account import *
from account.view.account import *
from customer.model.customer import *
import random, string, json

class AccountController():
    def __init__(self):
        self.model = AccountModel()
        self.view = AccountView()

    def create(self, json_request):
        account_number = self.generate_account_number()
        cif_number = json_request['cif_number']
        currency = json_request['currency']
        balance = 0

        account = self.model.create(account_number, cif_number, currency, balance)
        
        return self.view.detail(account)

    def delete(self, account_number):
        
        if self.model.detail(account_number):
            self.model.delete(account_number)
            return self.view.delete_success()
        else:
            return self.view.not_found_account_number()

    def detail(self, account_number):
        account_number_detail = self.model.detail(account_number)
        
        if account_number_detail:
            return self.view.detail(account_number_detail)
        else:
            return self.view.not_found_account_number()

    def list(self, cif_number):
        db_account_numbers = self.model.list(cif_number)

        print(cif_number)
        
        account_numbers = []
        for account_number in db_account_numbers:
            account_numbers.append(account_number)

        return self.view.list(account_numbers)

    def historical_transaction(self, account_number):
        db_hist_trx = self.model.historical_transaction(account_number)
        
        hist_trx = []
        for hist in db_hist_trx:
            hist_trx.append(hist)

        return self.view.list(hist_trx)

    def deposit(self, json_request):
        # validate account number
        # current settlement balance = current balance + amount
        # update balance
        # current balance == db current balance - amount

        account_number = json_request['account_number']
        amount = int(json_request['amount'])
        description = json_request['description']
        
        db_account_number = self.model.detail(account_number)

        data = json_request

        if not db_account_number:
            return self.view.not_found_account_number()

        current_settlement_balance = db_account_number['balance'] + amount

        self.model.update_balance(account_number, current_settlement_balance)

        db_current_account_number = self.model.detail(account_number)

        transaction_status = None
        if db_account_number['balance'] == (db_current_account_number['balance'] - amount):
            transaction_status = True
        else:
            transaction_status = False

        if transaction_status:
            journal_number = self.generate_journal_number(account_number)
            data['journal_number'] =journal_number
            self.model.add_historical_transaction(account_number, amount, "CREDIT", journal_number, '', "DEPOSIT", description)
            return self.view.detail({ 'message' : 'success', 'data' : data })
        else:
            return self.view.settlement_failed()


    def transfer(self, json_request):
        # get detail from account number
        # get detail to account number
        # get from account number balance + to account number balance = current settlement balance
        # from account number balance - amount -> current from account number balance 
        # to account number balance - amount -> current to account number balance
        # current settlement balance == current from account number balance + current to account number balance
        # update from account balance
        # update to account balance
        # get detail from account number 2
        # get detail to account number 2
        # current settlement balance == from account number balance 2 +  to account number balance 2
        # done

        from_account_number = json_request['from_account_number']
        to_account_number = json_request['to_account_number']
        transaction_id = json_request['transaction_id']
        description = json_request['description']
        amount = int(json_request['amount'])

        data = json_request

        db_from_account_number = self.model.detail(from_account_number)
        db_to_account_number = self.model.detail(to_account_number)

        if not db_from_account_number:
            return self.view.not_found_account_number("From account number is not found!")

        if not db_to_account_number:
            return self.view.not_found_account_number("To account number is not found!")

        db_from_account_number_balance = db_from_account_number['balance']
        db_to_account_number_balance = db_to_account_number['balance']

        current_settlement_balance = db_from_account_number_balance + db_to_account_number_balance

        if amount >= db_from_account_number_balance:
            return self.view.unsufficient_balance()

        from_account_number_current_balance = db_from_account_number_balance - amount
        to_account_number_current_balance = db_to_account_number_balance + amount

        transaction_status = None

        if current_settlement_balance == from_account_number_current_balance + to_account_number_current_balance:
            self.model.update_balance(from_account_number, from_account_number_current_balance)
            self.model.update_balance(to_account_number, to_account_number_current_balance)

            db_from_account_number = self.model.detail(from_account_number)
            db_to_account_number = self.model.detail(to_account_number)

            if current_settlement_balance == db_from_account_number['balance'] + db_to_account_number['balance']:
                transaction_status = True
            else:
                transaction_status = False

        else:
            self.model.update_balance(db_from_account_number, db_from_account_number_balance)
            self.model.update_balance(db_to_account_number, db_to_account_number_balance)
            transaction_status = False

        if transaction_status:
            journal_number = self.generate_journal_number(from_account_number)
            data['journal_number'] = journal_number
            self.model.add_historical_transaction(from_account_number, amount, "DEBIT", journal_number, transaction_id, "TRANSFER", description)
            self.model.add_historical_transaction(to_account_number, amount, "CREDIT", journal_number, transaction_id, "TRANSFER", description)

            # notify transfer

            return self.view.detail({ 'message' : 'success', 'data' : data })
        else:
            return self.view.settlement_failed()

    def reversal(self, json_request):
        # detail account
        # get balance
        # current settlement balance = db balance + amount
        # get db balance
        # current settlement balance == db current settlement balance - amount

        account_number = json_request['account_number']
        amount = int(json_request['amount'])
        description = json_request['description']
        transaction_id = json_request['transaction_id']
        journal_number = json_request['journal_number']
        transaction_type = json_request['transaction_type']
        data = json_request

        db_account_number = self.model.detail(account_number)
        current_settlement_balance = db_account_number['balance'] + amount

        self.model.update_balance(account_number, current_settlement_balance)
        db_current_account_number = self.model.detail(account_number)

        db_current_settlement_balance = db_current_account_number['balance'] - amount

        if db_account_number['balance'] == db_current_settlement_balance:
            self.model.add_historical_transaction(account_number, amount, "CREDIT", journal_number, transaction_id, transaction_type, description)
            return self.view.detail({ 'message' : 'success', 'data' : data })
        else:
            return self.view.reversal_failed()

    def debit(self, json_request):
        # detail account
        # get balance
        # current settlement balance = db balance - amount
        # get db balance
        # current settlement balance == db current settlement balance + amount

        account_number = json_request['account_number']
        amount = int(json_request['amount'])
        description = json_request['description']
        transaction_id = json_request['transaction_id']
        transaction_type = json_request['transaction_type']
        data = json_request

        db_account_number = self.model.detail(account_number)

        if db_account_number == None:
            return self.view.not_found_account_number()

        if amount >= db_account_number['balance']:
            return self.view.unsufficient_balance()

        current_settlement_balance = db_account_number['balance'] - amount

        self.model.update_balance(account_number, current_settlement_balance)
        db_current_account_number = self.model.detail(account_number)

        db_current_settlement_balance = db_current_account_number['balance'] + amount

        if db_account_number['balance'] == db_current_settlement_balance:
            journal_number = self.generate_journal_number(account_number)
            data['journal_number'] = journal_number
            self.model.add_historical_transaction(account_number, amount, "DEBIT", journal_number, transaction_id, transaction_type, description)
            return self.view.detail({ "message" : "success", 'data' : data })
        else:
            return self.view.settlement_failed()

    def generate_journal_number(self, account_number, size=6):
        journal_number = ''.join(random.choice(string.digits) for _ in range(size))
        db_journal_number = self.model.find_journal_number(journal_number, account_number)
        if db_journal_number:
            self.generate_journal_number(account_number)
        return journal_number

    def generate_account_number(self, size=10):
        account_number = ''.join(random.choice(string.digits) for _ in range(size))
        db_account_number = self.model.detail(account_number)
        if db_account_number:
            self.generate_account_number()
        return account_number
