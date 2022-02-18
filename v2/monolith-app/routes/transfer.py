from transfer.controller.transfer import *
from flask import request, Blueprint

transfer = Blueprint("transfer", __name__)

@transfer.route("/inquiry/own_account_number", methods=["GET"])
@transfer.route("/inquiry/own_account_number/", methods=["GET"])
def own_account_list():
    return TransferController().inquiry_own_account_number(request.args.get("cif_number"))

@transfer.route("/inquiry/account_number", methods=["GET"])
@transfer.route("/inquiry/account_number/", methods=["GET"])
def account_inquiry():
    return TransferController().inquiry_account_number(request.args.get("account_number"))

@transfer.route("/interbank/account_number", methods=["GET"])
@transfer.route("/interbank/account_number/", methods=["GET"])
def account_interbank_inquiry():
    return TransferController().inquiry_interbank_account_number(request.args.get("account_number"), request.args.get("bank_code"))

@transfer.route("/save/account_number", methods=["POST"])
def save_account():
    return TransferController().save_account_number(request.get_json())

@transfer.route("/list/account_number", methods=["GET"])
@transfer.route("/list/account_number", methods=["GET"])
def account_number_list():
    return TransferController().list_account_number(request.args.get('cif_number'))

@transfer.route("/account_number/", methods=["DELETE"])
def accounts():
    return TransferController().delete_account_number(request.args.get('cif_number'), request.args.get('account_number'), request.args.get('bank_code'))

@transfer.route("/", methods=["POST"])
def account_transfer():
    return TransferController().transfer_account_number(request.get_json())

@transfer.route("/", methods=["GET"])
@transfer.route("", methods=["GET"])
def list():
    return TransferController().list(request.args.get('cif_number'))

@transfer.route("/interbank/", methods=["POST"])
def account_interbank_transfer():
    return TransferController().transfer_interbank_account_number(request.get_json())

@transfer.route("/detail", methods=["GET"])
@transfer.route("/detail/", methods=["GET"])
def detail():
    return TransferController().detail(request.args.get('transaction_id'))
