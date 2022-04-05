from dataclasses import dataclass
from model.transaction import Transaction as TransactionModel
from model.transaction import TransferIntrabank as TransferIntrabankModel
from model.transaction import DebitTransaction as DebitTransactionModel
from exception.business_logic_exception import BusinessLogicException
from service.journal_ack import JournalAck
from abc import ABC, abstractmethod
from datetime import datetime
from view.presenter import detail
from flask import jsonify

class Transaction:

    @staticmethod
    def deposit(json_request):
        try:
            print(f"incoming request: {json_request}")
            start = datetime.now()
            
            model = TransactionModel()
            journal_number = model.deposit(json_request['account_number'], json_request['amount'])
            print(f"outgoing request: {journal_number}")
            return detail( {'journal_number' : journal_number} , start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500
    
    @staticmethod
    def reversal(json_request):
        try:
            print(f"incoming request: {json_request}")
            start = datetime.now()
            
            model = TransactionModel()
            journal_number = model.reversal(json_request['account_number'], json_request['amount'], json_request['journal_number'])
            print(f"outgoing request: {journal_number}")
            return detail( {'journal_number' : journal_number} , start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

    @staticmethod
    def detail(transaction_type, account_number, journal_number):
        try:
            print(f"incoming request: {json_request}")
            start = datetime.now()
            
            model = TransactionModel()
            detail_transaction = model.detail_transaction(transaction_type, account_number, journal_number)
            print(f"outgoing request: {detail_transaction}")
            return detail( detail_transaction , start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

    @staticmethod
    def list(cif_number, skip, limit):
        try:
            print(f"incoming request: {cif_number}")
            start = datetime.now()
            
            model = TransactionModel()
            transaction_list = model.list(cif_number, skip, limit)
            print(f"outgoing request: {transaction_list}")
            return detail( transaction_list , start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

    

class TransferIntrabank:

    @staticmethod
    def transfer(json_request):
        try:
            print(f"incoming request: {json_request}")
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

class DebitTransaction:

    @staticmethod
    def debit(json_request):
        try:
            print(f"incoming request: {json_request}")
            start = datetime.now()
            
            model = DebitTransactionModel()
            model.transaction_id = json_request['transaction_id']
            model.transaction_type = json_request['transaction_type']
            model.from_account_number = json_request['from_account_number']
            model.cif_number = json_request['cif_number']
            model.amount = int(json_request['amount'])
            model.description = json_request['description']
            journal_number = model.debit()
            print(f"outgoing request: {journal_number}")
            return detail({ 'journal_number' : journal_number }, start, 200)
        except BusinessLogicException as error:
            request_message = {
                "transaction_id": json_request['transaction_id'],
                "status" : "FAILED",
                "message" : str(error),
                "journal_number": "000000"
            }
            JournalAck().notify_journal(json_request['transaction_type'], request_message, 'ack_debit')
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            request_message = {
                "transaction_id": json_request['transaction_id'],
                "status" : "FAILED",
                "message" : str(error),
                "journal_number": "000000"
            }
            JournalAck().notify_journal(json_request['transaction_type'], request_message, 'ack_debit')
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500