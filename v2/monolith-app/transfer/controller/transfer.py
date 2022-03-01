from transfer.model.transfer import *
from transfer.view.transfer import *
import random, string

class TransferController():
    def __init__(self):
        self.model = TransferModel()
        self.view = TransferView()

    def inquiry_own_account_number(self, cif_number):
        result = self.model.inquiry_own_account_number(cif_number)
        return self.view.list(result[0].get_json(), result[1])

    def inquiry_account_number(self, account_number):
        result = self.model.inquiry_account_number(account_number)
        return self.view.detail(result[0].get_json(), result[1])

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

        data = {
            'from_account_number' : from_account_number,
            'to_account_number' : to_account_number,
            'amount' : amount,
            'description' : description,
            'cif_number' : cif_number,
            'transaction_id' : transaction_id
        }

        # save transfer
        save_transfer_result = self.model.save_transfer(cif_number, from_account_number, to_account_number, '009', amount, transaction_id)
        
        message =  None
        status_code = 200

        # settlement 
        if save_transfer_result:
            transfer_result = self.model.transfer_account_number(from_account_number, to_account_number, transaction_id, amount, description)

            # update transfer
            if transfer_result[1] in (200, 201):
                message = 'DONE'
                data['transfer_result'] = transfer_result[0].get_json()
                self.model.update(transaction_id, message)
            else:
                message = 'SETTLEMENT_FAILED'
                status_code = 500
                self.model.update(transaction_id, message)
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

        data = {
            'from_account_number' : from_account_number,
            'to_account_number' : to_account_number,
            'amount' : amount,
            'description' : description,
            'bank_code' : bank_code,
            'cif_number' : cif_number,
            'transaction_id' : transaction_id
        }

        # save 
        save_transfer_result = self.model.save_transfer(cif_number, from_account_number, to_account_number, bank_code, amount, transaction_id)

        # settlement
        message =  None
        status_code = 200

        if save_transfer_result:
            settlement_result = self.model.settlement_account_number(from_account_number, to_account_number, bank_code, transaction_id, amount)
            
            if settlement_result[1] in (200, 201):
                # update transfer
                message = 'SETTLEMENT_DONE'
                self.model.update(transaction_id, message)

                data['settlement_response'] = settlement_result[0].get_json()

                # notify
                notify_result = self.model.notify_interbank(from_account_number, '009', to_account_number, bank_code, amount, description)
                
                # update transfer
                if notify_result.status_code in (200, 201):
                    
                    message = 'DONE'
                    self.model.update(transaction_id, message)
                    data['interbank_response'] = notify_result.json()

                else:
                    message = 'NOTIFY_FAILED'
                    status_code = 500
                    self.model.update(transaction_id, message)
                    self.model.reversal_interbank(from_account_number, to_account_number, bank_code, transaction_id, amount, journal_number)
            else:
                message = 'SETTLEMENT_FAILED'
                status_code = 500
                self.model.update(transaction_id, message)
        else:
            message = 'SAVE_TRANSFER_FAILED'
            status_code = 500
            self.model.update(transaction_id, message)
        
        return self.view.detail({ 'message' : message, 'data' : data }, status_code)
    
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