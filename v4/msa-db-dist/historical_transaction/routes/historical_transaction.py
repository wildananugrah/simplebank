from controller.historical_transaction import historical_transaction_list, historical_transaction_save
from flask import request, Blueprint

historical_transaction = Blueprint("historical_transaction", __name__)

@historical_transaction.route("/", methods=["GET"])
def find():
    return historical_transaction_list(request.args.get('account_number'), request.args.get('skip'), request.args.get('limit'))

@historical_transaction.route("/", methods=["POST"])
def save():
    return historical_transaction_save(request.get_json())