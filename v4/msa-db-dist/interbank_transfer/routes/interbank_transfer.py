from controller.interbank_transfer import interbank_transfer_pay, interbank_transfer_inquiry
from flask import request, Blueprint
from pymongo import MongoClient

interbank_transfer = Blueprint("interbank_transfer", __name__)

@interbank_transfer.route("/transfer/interbank/", methods=["GET"])
def inquiry_interbank():
    return interbank_transfer_inquiry(request.args.get('to_account_number'), request.args.get('to_bank_code'))

@interbank_transfer.route("/transfer/interbank/", methods=["POST"])
def transfer_interbank():
    return interbank_transfer_pay(request.get_json())