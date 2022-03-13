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

@interbank_transfer.route("/transfer/interbank/detail/", methods=["GET"])
def transfer_interbank_detail():
    return InterbankTransfer.detail(request.args.get("transaction_id"))

@interbank_transfer.route("/transfer/interbank/list/", methods=["GET"])
def transfer_interbank_list():
    return InterbankTransfer.list(request.args.get("cif_number"))

@interbank_transfer.route("/transfer/interbank/update/", methods=["POST"])
def transfer_interbank_update():
    return InterbankTransfer.update(request.get_json())