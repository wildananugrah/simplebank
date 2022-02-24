from flask import jsonify

class PaymentView():
    def __init__(self):
        pass

    def detail(self, message, status = 201):
        return jsonify(message), status

    def list(self, message, status = 201):
        return jsonify(message), status

    def not_found_account_number(self):
        return jsonify({ 'message' : 'invalid account number' }), 400