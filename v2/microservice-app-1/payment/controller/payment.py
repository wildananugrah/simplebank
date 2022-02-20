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
        transaction_id = self.generate_transaction_id(cif_number)

        message = "PROCESSED"
        status_code = 200
        data = json_request
        data['transaction_id'] = transaction_id

        self.model.save_payment(account_number, bill_id, biller_name, amount, transaction_id, cif_number, biller_request)

        result_debit = self.model.debit(account_number, amount, description, transaction_id)


        return self.view.detail({ 'message' : message, 'data' : data }, status_code)

    def update(self, json_request):
        if json_request['status_code'] in (200, 210):
            message = "SETTLEMENT_DONE"
            self.model.update_payment(json_request['data']['transaction_id'], message)

            biller_request = self.model.detail(json_request['data']['transaction_id'])['outgoing_request']
            
            result_notify_biller = self.model.notify_billers(biller_request)
            if result_notify_biller.status_code in (200, 201):
                status_code = result_notify_biller.status_code
                message = "DONE"
                self.model.update_payment(json_request['data']['transaction_id'], message, result_notify_biller.json())
            else:
                status_code = result_notify_biller.status_code
                message = "NOTIFY_FAILED"
                self.model.reversal_payment(json_request['data']['account_number'], json_request['data']['amount'], json_request['data']['description'], json_request['data']['transaction_id'], json_request['data']['journal_number'])
                self.model.update_payment(json_request['data']['transaction_id'], message)
        else:
            status_code = json_request['status_code']
            message = "SETTLEMENT_FAILED"  
            self.model.update_payment(json_request['data']['transaction_id'], message)
        
        return self.view.detail({ 'message' : message }, status_code)

    def update_reversal(self, json_request):
        status_code = json_request['status_code']
        message = None
        data = json_request

        if status_code in (200, 210):
            message = "REVERSED"
            self.model.update_payment(json_request['data']['transaction_id'], message, incoming_response=json_request)
        else:
            status_code = 500
            message = 'REVESAL_FAILED'
            self.model.update_payment(json_request['data']['transaction_id'], message, incoming_response=json_request)
        
        return self.view.detail({ 'message' : message }, status_code)

    def generate_transaction_id(self, cif_number, size=10):
        transaction_id = ''.join(random.choice(string.digits) for _ in range(size))
        db_transaction_id = self.model.find_transaction_id(cif_number, transaction_id)
        if db_transaction_id:
            self.generate_transaction_id(cif_number)
        return transaction_id