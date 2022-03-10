from controller.interbank_transfer import *
from flask import request, Blueprint
from pymongo import MongoClient

interbank_transfer = Blueprint("interbank_transfer", __name__)

@interbank_transfer.route("/transfer/interbank/", methods=["GET"])
def inquiry_interbank():
    return InterbankTransfer.inquiry(request.args.get('to_account_number'), request.args.get('to_bank_code'))

@interbank_transfer.route("/transfer/interbank/", methods=["POST"])
def transfer_interbank():
    return InterbankTransfer.transfer(request.get_json())