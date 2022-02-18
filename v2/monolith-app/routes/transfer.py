from transfer.controller.transfer import *
from flask import request, Blueprint

transfer = Blueprint("transfer", __name__)

@transfer.route("/own_account_list", methods=["GET"])
@transfer.route("/own_account_list/", methods=["GET"])
def own_account_list():
    return TransferController().own_account_list(request.args.get("cif_number"))

@transfer.route("/account_inquiry", methods=["GET"])
@transfer.route("/account_inquiry/", methods=["GET"])
def account_inquiry():
    return TransferController().account_inquiry(request.args.get("account_number"))

@transfer.route("/account_interbank_inquiry", methods=["GET"])
@transfer.route("/account_interbank_inquiry/", methods=["GET"])
def account_interbank_inquiry():
    return TransferController().account_interbank_inquiry(request.args.get("account_number"), request.args.get("bank_code"))

@transfer.route("/save_account/", methods=["POST"])
def save_account():
    return TransferController().save_account(request.get_json())

@transfer.route("/account_number_list", methods=["GET"])
@transfer.route("/account_number_list/", methods=["GET"])
def account_number_list():
    return TransferController().list_account(request.args.get('cif_number'))

@transfer.route("/accounts/", methods=["DELETE"])
def accounts():
    return TransferController().delete_account(request.args.get('cif_number'), request.args.get('account_number'), request.args.get('bank_code'))

@transfer.route("/", methods=["POST"])
def account_transfer():
    return TransferController().account_transfer(request.get_json())

@transfer.route("/", methods=["GET"])
@transfer.route("", methods=["GET"])
def list():
    return TransferController().list(request.args.get('cif_number'))

@transfer.route("/interbank/", methods=["POST"])
def account_interbank_transfer():
    return TransferController().account_interbank_transfer(request.get_json())

@transfer.route("/detail", methods=["GET"])
@transfer.route("/detail/", methods=["GET"])
def transfer_detail():
    return TransferController().transfer_detail(request.args.get('transaction_id'))
