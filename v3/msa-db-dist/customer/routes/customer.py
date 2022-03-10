from controller.customer import CustomerMobile, CustomerInternetBanking, Customer
from flask import request, Blueprint
from pymongo import MongoClient

customer = Blueprint("customer", __name__)

@customer.route("/", methods=["GET"])
def detail():
    id_type = request.args.get('key_type')
    value = request.args.get('value')
    return Customer.detail(id_type, value)

@customer.route("/mobile/login/", methods=["POST"])
def mobile_login():
    return CustomerMobile.login(request.get_json())

@customer.route("/mobile/logout/", methods=["POST"])
def mobile_logout():
    return CustomerMobile.logout(request.get_json())

@customer.route("/internet_banking/login/", methods=["POST"])
def interbank_banking_login():
    return CustomerInternetBanking.login(request.get_json())

@customer.route("/internet_banking/logout/", methods=["POST"])
def internet_banking_logout():
    return CustomerInternetBanking.logout(request.get_json())