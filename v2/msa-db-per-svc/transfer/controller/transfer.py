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

        return self.view.detail(self.model.save_account_number(cif_number, account_number, bank_code))

    def delete_account_number(self, cif_number, account_number, bank_code):
        if self.model.detail_account_number(cif_number, account_number, bank_code):
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
        from_account_number = json_request['from_account_number'] 
        to_account_number = json_request['to_account_number'] 
        amount = json_request['amount'] 
        description = json_request['description']
        cif_number = json_request['cif_number']
        transaction_id = self.generate_transaction_id(from_account_number)

        data = json_request
        data['transaction_id'] = transaction_id

        # save transfer
        save_transfer_result = self.model.save_transfer(cif_number, from_account_number, to_account_number, '009', amount, transaction_id, description)
        
        message =  None
        status_code = 200

        # settlement 
        if save_transfer_result:
            message = 'PROCESSED'
            transfer_result = self.model.transfer_account_number(from_account_number, to_account_number, transaction_id, amount, description)
            print(transfer_result.json())
            if transfer_result.status_code in (200, 201):
                message = 'DONE'
                data['transfer_result'] = json_request
                status_code = transfer_result.status_code
                self.model.update(transaction_id, message)
            else:
                message = 'SETTLEMENT_FAILED'
                data['transfer_result'] = json_request
                status_code = transfer_result.status_code
                self.model.update(transaction_id, message)
            
            return self.view.detail({ 'message' : message, 'detail' : transfer_result.json(), 'transaction_id' : transaction_id }, status_code)

        else:
            message = 'SAVE_TRANSFER_FAILED'
            status_code = 500
            self.model.update(transaction_id, message)

        return self.view.detail({ 'message' : message, 'data' : data }, status_code)

    def transfer_interbank_account_number(self, json_request):
        from_account_number = json_request['from_account_number'] 
        to_account_number = json_request['to_account_number'] 
        amount = json_request['amount'] 
        description = json_request['description']
        bank_code = json_request['bank_code']
        cif_number = json_request['cif_number']
        transaction_id = self.generate_transaction_id(from_account_number)

        data = json_request
        data['transaction_id'] = transaction_id

        # save 
        save_transfer_result = self.model.save_transfer(cif_number, from_account_number, to_account_number, bank_code, amount, transaction_id, description)

        # settlement
        message =  "PROCESSED"
        status_code = 200

        content = {}

        if save_transfer_result:
            settlement_result = self.model.settlement_account_number(from_account_number, to_account_number, bank_code, transaction_id, amount)

            if settlement_result.status_code in (200, 201):
                message = 'SETTLEMENT_DONE'
                self.model.update(transaction_id, message)

                content['settlement_response'] = settlement_result.json()
                transaction = self.model.detail(transaction_id)
                content['transaction'] = transaction

                # notify
                notify_result = self.model.notify_interbank(transaction['from_account_number'], '009', transaction['to_account_number'], transaction['bank_code'], transaction['amount'], transaction['description'])
                
                # update transfer
                if notify_result.status_code in (200, 201):
                    
                    message = 'DONE'
                    self.model.update(transaction_id, message)
                    content['interbank_response'] = notify_result.json()

                else:
                    message = 'NOTIFY_FAILED'
                    status_code = 500
                    self.model.update(transaction_id, message)
                    reversal_result = self.model.reversal_interbank(transaction['from_account_number'], transaction['to_account_number'], transaction['bank_code'], transaction_id, transaction['amount'], settlement_result.json()['data']['journal_number'])

                    if reversal_result.status_code in (200, 201):
                        message = 'REVERSED'
                        self.model.update(transaction_id, message)
                    else:
                        message = 'REVESAL_FAILED'
                        status_code = 500
                        self.model.update(transaction_id, message)

            else:
                message = 'SETTLEMENT_FAILED'
                status_code = 500
                self.model.update(transaction_id, message)

        else:
            message = 'SAVE_TRANSFER_FAILED'
            status_code = 500
            self.model.update(transaction_id, message)
        
        return self.view.detail({ 'message' : message, 'data' : content }, status_code)

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
