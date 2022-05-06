from dataclasses import dataclass
from model.customer import Customer, CustomerMobile, CustomerInternetBanking
from exception.business_logic_exception import BusinessLogicException
from abc import ABC, abstractmethod
from datetime import datetime
from view.presenter import view_detail
from flask import jsonify

def customer_detail(key_type, value):
    try:
        start = datetime.now()
        model = Customer()
        customer = model.detail(key_type, value)
        return view_detail(customer, start)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def customer_mobile_login(json_request):
    try:
        start = datetime.now()
        model = CustomerMobile()
        model.username = json_request['username']
        model.password = json_request['password']
        customer = model.login()

        return view_detail(customer, start, 200)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def customer_internet_banking_login(json_request):
    try:
        start = datetime.now()
        model = CustomerInternetBanking()
        model.email = json_request['email']
        model.password = json_request['password']
        customer = model.login()

        return view_detail(customer, start, 200)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def customer_logout(json_request):
    try:
        start = datetime.now()
        model = Customer()
        customer = model.logout(json_request['session_id'])
        return view_detail(customer, start, 200)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500