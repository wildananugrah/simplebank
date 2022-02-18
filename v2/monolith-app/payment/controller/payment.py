from payment.model.payment import *
from payment.view.payment import *
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
        print(response.json())
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

        # validate account number
        result_account_number = self.model.find_account_number(account_number)

        message = None
        status_code = None
        data = json_request

        if result_account_number[1] in (200, 201):
            self.model.save_payment(account_number, bill_id, biller_name, amount, transaction_id, cif_number, biller_request)

            result_debit = self.model.debit(account_number, amount, description, transaction_id)

            if result_debit[1] in (200, 201):
                status_code = result_debit[1]
                message = "SETTLEMENT_DONE"

                data['settlement_response'] = result_debit[0].get_json()
                
                self.model.update_payment(transaction_id, message)
                
                result_notify_biller = self.model.notify_billers(biller_request)
                if result_notify_biller.status_code in (200, 201):
                    status_code = result_notify_biller.status_code
                    message = "DONE"
                    data['biller_response'] = result_notify_biller.json()
                    self.model.update_payment(transaction_id, message, result_notify_biller.json())
                else:
                    status_code = result_notify_biller.status_code
                    message = "NOTIFY_FAILED"
                    self.model.reversal_payment(account_number, amount, description, transaction_id, journal_number)
                    self.model.update_payment(transaction_id, message)
            else:
                status_code = result_debit.status_code
                message = "SETTLEMENT_FAILED"
                
                self.model.update_payment(transaction_id, message)
        else:
            return self.view.not_found_account_number()

        return self.view.detail({ 'message' : message, 'data' : data }, status_code)

    def generate_transaction_id(self, cif_number, size=10):
        transaction_id = ''.join(random.choice(string.digits) for _ in range(size))
        db_transaction_id = self.model.find_transaction_id(cif_number, transaction_id)
        if db_transaction_id:
            self.generate_transaction_id(cif_number)
        return transaction_id