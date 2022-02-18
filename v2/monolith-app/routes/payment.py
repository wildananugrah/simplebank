from payment.controller.payment import *
from flask import request, Blueprint
from pymongo import MongoClient

payment = Blueprint("payment", __name__)

@payment.route("/", methods=["GET"])
def inquiry_billpayment():
    return PaymentController().inquiry_billing(request.args.get('bill_id'))

@payment.route("/", methods=["POST"])
def payment_billpayment():
    return PaymentController().payment_billing(request.get_json())

@payment.route("/list", methods=["GET"])
def payment_list():
    return PaymentController().list(request.args.get("cif_number"))

@payment.route("/detail", methods=["GET"])
def payment_detail():
    return PaymentController().detail(request.args.get("transaction_id"))