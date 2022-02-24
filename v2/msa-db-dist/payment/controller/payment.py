from model.payment import *
from view.payment import *
import random, string

class PaymentController():
    def __init__(self):
        self.model = PaymentModel()
        self.view = PaymentView()

    def list(self, cif_number):
        payment_list = self.model.list(cif_number)
        _payment_list = []

        for payment in payment_list:
            _payment_list.append(payment)

        return self.view.list(_payment_list)

    def detail(self, transaction_id):
        payment = self.model.detail(transaction_id)
        return self.view.detail(payment)

    def inquiry_billing(self, bill_id):
        response = self.model.inquiry_billers(bill_id)
        return self.view.detail(response.json(), response.status_code)

    def pay_billing(self, json_request):
        account_number = json_request['account_number']
        biller_request = json_request['biller_request_message']
        bill_id = json_request['bill_id']
        biller_name = json_request['biller_name']
        amount = json_request['amount']
        cif_number = json_request['cif_number']
        description = json_request['description']
        
        db_account_number = self.model.detail_account_number(account_number)

        if db_account_number == None:
            return self.view.detail({ 'message' : 'account number is not found' }, 400)

        if db_account_number['balance'] < amount:
            return self.view.unsufficient_account()

        notify_billers = self.model.notify_billers(biller_request)
        transaction_id = self.generate_transaction_id(account_number)
        
        if notify_billers.status_code in (200, 201):
            journal_number = self.generate_journal_number(account_number)

            self.model.update_account_number_balance(account_number, db_account_number['balance'] - amount)
            self.model.add_historical_transaction(account_number, amount, "DEBIT", journal_number, transaction_id, "TRANSFER", description)

            self.model.save_payment(account_number, bill_id, biller_name, amount, transaction_id, cif_number, biller_request, "DONE")
            return self.view.detail({ "message" : "payment has been executed successfully" }, 201)
        else:
            self.model.save_payment(cif_number, account_number, to_account_number, bank_code, amount, transaction_id, description, "NOTIFY_FAILED")
            return self.view.detail({ "message" : "payment transaction is failed" }, 500)

    def generate_transaction_id(self, cif_number, size=10):
        transaction_id = ''.join(random.choice(string.digits) for _ in range(size))
        db_transaction_id = self.model.find_transaction_id(cif_number, transaction_id)
        if db_transaction_id:
            self.generate_transaction_id(cif_number)
        return transaction_id

    def generate_journal_number(self, account_number, size=6):
        journal_number = ''.join(random.choice(string.digits) for _ in range(size))
        db_journal_number = self.model.find_journal_number(journal_number, account_number)
        if db_journal_number:
            self.generate_journal_number(account_number)
        return journal_number