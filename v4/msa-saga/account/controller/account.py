from dataclasses import dataclass
from model.account import Account
from exception.business_logic_exception import BusinessLogicException
from abc import ABC, abstractmethod
from datetime import datetime
from view.presenter import view_detail
from flask import jsonify

def account_detail(account_number):
    try:
        start = datetime.now()
        model = Account()
        account = model.detail(account_number)
        return view_detail(account, start, 200)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def account_delete(account_number):
    try:
        start = datetime.now()
        model = Account()
        account = model.delete(account_number)
        return view_detail(account, start, 200)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500
    
def account_list(cif_number, skip, limit):
    try:
        start = datetime.now()
        model = Account()
        account_list = model.list(cif_number, skip, limit)
        return view_detail(account_list, start, 200)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def account_create(json_request):
    try:
        start = datetime.now()
        model = Account()
        account = model.create(json_request['cif_number'])
        return view_detail(account, start, 200)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def account_update(json_request):
    try:
        start = datetime.now()
        model = Account()
        account = model.update(json_request['account_number'], json_request['current_balance'])
        return view_detail(account, start, 200)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500