from dataclasses import dataclass
from model.transaction import Transaction as TransactionModel
from model.transaction import TransferIntrabank as TransferIntrabankModel
from model.transaction import DebitTransaction as DebitTransactionModel
from exception.business_logic_exception import BusinessLogicException
from abc import ABC, abstractmethod
from datetime import datetime
from view.presenter import view_detail
from flask import jsonify

def transaction_deposit(json_request):
    try:
        start = datetime.now()
        
        model = TransactionModel()
        journal_number = model.deposit(json_request['account_number'], json_request['amount'])
        
        return view_detail( {'journal_number' : journal_number} , start, 200)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def transaction_debit(json_request):
    try:
        start = datetime.now()
        
        model = DebitTransactionModel()
        model.from_account_number = json_request['from_account_number']
        model.amount = int(json_request['amount'])
        model.description = json_request['description']
        model.cif_number = json_request['cif_number']
        model.transaction_type = json_request['transaction_type']
        journal_number = model.debit()
        
        return view_detail( {'journal_number' : journal_number} , start, 200)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def transaction_reversal(json_request):
    try:
        start = datetime.now()
        
        model = TransactionModel()
        journal_number = model.reversal(json_request['account_number'], json_request['amount'], json_request['journal_number'])  
        return detail( {'journal_number' : journal_number} , start, 200)
        
    except BusinessLogicException as error:
        return detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def transaction_detail(transaction_type, account_number, journal_number):
    try:
        start = datetime.now()
        
        model = TransactionModel()
        detail_transaction = model.detail_transaction(transaction_type, account_number, journal_number)
        
        return view_detail( detail_transaction , start, 200)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def transaction_list(cif_number, skip, limit):
    try:
        start = datetime.now()
        
        model = TransactionModel()
        transaction_list = model.list(cif_number, skip, limit)
        
        return view_detail( transaction_list , start, 200)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def transaction_intrabank_transfer(json_request):
    try:
        start = datetime.now()
        
        model = TransferIntrabankModel()
        model.from_account_number = json_request['from_account_number']
        model.to_account_number = json_request['to_account_number']
        model.cif_number = json_request['cif_number']
        model.amount = int(json_request['amount'])
        model.description = json_request['description']
        journal_number = model.transfer()
        
        return view_detail({ 'journal_number' : journal_number }, start, 200)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500