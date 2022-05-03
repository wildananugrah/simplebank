from dataclasses import dataclass
from model.transaction import Transaction as TransactionModel
from model.transaction import TransferInterbank as TransferInterbankModel
from exception.business_logic_exception import BusinessLogicException
from abc import ABC, abstractmethod
from datetime import datetime
from view.presenter import view_detail
from flask import jsonify

def transaction_transfer_interbank_inquiry(to_account_number, to_bank_code):
    try:
        start = datetime.now()
        
        model = TransferInterbankModel()
        transaction = model.inquiry(to_account_number, to_bank_code)
        
        return view_detail(transaction, start, 200)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def transaction_transfer_interbank_transfer(json_request):
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
        
        return view_detail({ 'journal_number' : journal_number }, start, 200)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500