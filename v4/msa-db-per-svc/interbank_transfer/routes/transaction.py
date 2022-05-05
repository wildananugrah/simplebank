from controller.transaction import transaction_transfer_interbank_inquiry, transaction_transfer_interbank_transfer
from flask import request, Blueprint
transaction = Blueprint("transaction", __name__)

@transaction.route("/transfer/interbank/", methods=["GET"])
def transfer_interbank_inquiry():
    return transaction_transfer_interbank_inquiry(request.args.get('to_account_number'), request.args.get('to_bank_code'))

@transaction.route("/transfer/interbank/", methods=["POST"])
def transfer_interbank_transfer():
    return transaction_transfer_interbank_transfer(request.get_json())