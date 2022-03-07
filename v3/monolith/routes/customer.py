from controller.customer import CustomerMobile
from flask import request, Blueprint
from pymongo import MongoClient

customer = Blueprint("customer", __name__)

@customer.route("/", methods=["GET"])
def detail():
    id_type = request.args.get('key_type')
    value = request.args.get('value')
    return CustomerMobile.detail(id_type, value)

@customer.route("/mobile/login/", methods=["POST"])
def login():
    return CustomerMobile.login(request.get_json())

@customer.route("/mobile/logout/", methods=["POST"])
def logout():
    return CustomerMobile.logout(request.get_json())