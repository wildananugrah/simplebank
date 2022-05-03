from controller.transaction import transaction_detail, transaction_deposit, transaction_list, transaction_intrabank_transfer, transaction_transfer_interbank_inquiry, transaction_transfer_interbank_transfer, transaction_electrical_billpayment_inquiry, transaction_electrical_billpayment_pay
from flask import request, Blueprint
transaction = Blueprint("transaction", __name__)

@transaction.route("/deposit/", methods=["POST"])
def deposit():
    return transaction_deposit(request.get_json())

@transaction.route("/", methods=["GET"])
def detail():
    return transaction_detail(request.args.get('transaction_type'), request.args.get('account_number'), request.args.get('journal_number'))

@transaction.route("/list/", methods=["GET"])
def list():
    return transaction_list(request.args.get('cif_number'), request.args.get('skip'), request.args.get('limit'))

@transaction.route("/transfer/intrabank/", methods=["POST"])
def transfer_intrabank():
    return transaction_intrabank_transfer(request.get_json())

@transaction.route("/transfer/interbank/", methods=["GET"])
def transfer_interbank_inquiry():
    return transaction_transfer_interbank_inquiry(request.args.get('to_account_number'), request.args.get('to_bank_code'))

@transaction.route("/transfer/interbank/", methods=["POST"])
def transfer_interbank_transfer():
    return transaction_transfer_interbank_transfer(request.get_json())

@transaction.route("/payment/eletrical/", methods=["GET"])
def electrical_billpayment_inquiry():
    return transaction_electrical_billpayment_inquiry(request.args.get('bill_id'))

@transaction.route("/payment/eletrical/", methods=["POST"])
def electrical_billpayment_pay():
    return transaction_electrical_billpayment_pay(request.get_json())