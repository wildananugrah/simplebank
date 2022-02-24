from controller.customer import *
from flask import request, Blueprint
from pymongo import MongoClient

customer = Blueprint("customer", __name__)

@customer.route("/", methods=["GET"])
def detail():
    id_type = request.args.get('id_type')
    value = request.args.get('value')
    return CustomerController().detail(id_type, value)

@customer.route("/login", methods=["POST"])
def login():
    return CustomerController().login(request.get_json())

@customer.route("/logout", methods=["POST"])
def logout():
    return CustomerController().logout(request.get_json())