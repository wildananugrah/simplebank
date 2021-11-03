from models.payment import Payment
import requests

class TaxPayment(Payment):

    def inquiry(self, bill_id):
        # build message
        response = requests.post(self.url, json={ 'bill_id' : bill_id }, headers={ 'Action' : "INQUIRY" })
        self.insert_to_h2hlookup(bill_id=bill_id, bill_type="TAX", transaction_type="INQUIRY", account_number='', cif_number='', action='', status="SUCCESS")
        return response

    def payment(self, bill_id, account_number, cif_number, amount):
        # build message
        response = requests.post(self.url, json={ 'bill_id' : bill_id , 'account_number' : account_number}, headers={ 'Action' : "PAYMENT" })
        self.debit(account_number=account_number, amount=amount)
        self.insert_to_h2hlookup(bill_id=bill_id, bill_type="TAX", transaction_type="PAYMENT", account_number=account_number, cif_number=cif_number, action='', status="SUCCESS")
        return response