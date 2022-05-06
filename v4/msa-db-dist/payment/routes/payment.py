from controller.transaction import electrical_billpayment_inquiry, electrical_billpayment_pay
from flask import request, Blueprint
from pymongo import MongoClient

payment = Blueprint("payment", __name__)

@payment.route("/payment/eletrical/", methods=["GET"])
def inquiry_eletrical_payment():
    return electrical_billpayment_inquiry(request.args.get('bill_id'))

@payment.route("/payment/eletrical/", methods=["POST"])
def pay_eletrical_payment():
    return electrical_billpayment_pay(request.get_json())