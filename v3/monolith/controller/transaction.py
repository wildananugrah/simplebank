from dataclasses import dataclass
from model.transaction import Transaction as TransactionModel
from model.transaction import TransferIntrabank as TransferIntrabankModel
from model.transaction import TransferInterbank as TransferInterbankModel
from model.transaction import EletricalBillPayment as EletricalBillPaymentModel
from exception.business_logic_exception import BusinessLogicException
from abc import ABC, abstractmethod
from datetime import datetime
from view.presenter import detail
from flask import jsonify

class Transaction:

    @staticmethod
    def deposit(json_request):
        try:
            start = datetime.now()
            
            model = TransactionModel()
            journal_number = model.deposit(json_request['account_number'], json_request['amount'])
            
            return detail( {'journal_number' : journal_number} , start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

    @staticmethod
    def detail(transaction_type, account_number, journal_number):
        try:
            start = datetime.now()
            
            model = TransactionModel()
            detail_transaction = model.detail_transaction(transaction_type, account_number, journal_number)
            
            return detail( detail_transaction , start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

    @staticmethod
    def list(cif_number):
        try:
            start = datetime.now()
            
            model = TransactionModel()
            transaction_list = model.list(cif_number)
            
            return detail( transaction_list , start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

    

class TransferIntrabank:

    @staticmethod
    def transfer(json_request):
        try:
            start = datetime.now()
            
            model = TransferIntrabankModel()
            model.from_account_number = json_request['from_account_number']
            model.to_account_number = json_request['to_account_number']
            model.cif_number = json_request['cif_number']
            model.amount = int(json_request['amount'])
            model.description = json_request['description']
            journal_number = model.transfer()
            
            return detail({ 'journal_number' : journal_number }, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

class TransferInterbank:

    @staticmethod
    def inquiry(to_account_number, to_bank_code):
        try:
            start = datetime.now()
            
            model = TransferInterbankModel()
            transaction = model.inquiry(to_account_number, to_bank_code)
            
            return detail(transaction, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

    @staticmethod
    def transfer(json_request):
        try:
            start = datetime.now()
            
            model = TransferInterbankModel()
            model.from_account_number = json_request['from_account_number']
            model.to_account_number = json_request['to_account_number']
            model.to_bank_code = json_request['to_bank_code']
            model.cif_number = json_request['cif_number']
            model.amount = int(json_request['amount'])
            model.description = json_request['description']
            journal_number = model.transfer()
            
            return detail({ 'journal_number' : journal_number }, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

class EletricalBillPayment:
    
    @staticmethod
    def inquiry(bill_id):
        try:
            start = datetime.now()
            
            model = EletricalBillPaymentModel()
            payment = model.inquiry(bill_id)

            return detail(payment, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

    @staticmethod
    def pay(json_request):
        try:
            start = datetime.now()
            
            model = EletricalBillPaymentModel()
            model.bill_id = json_request['bill_id']
            model.amount = json_request['amount']
            model.description = json_request['description']
            model.from_account_number = json_request['from_account_number']
            model.cif_number = json_request['cif_number']

            journal_number = model.pay()
            return detail({ 'journal_number' : journal_number }, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500