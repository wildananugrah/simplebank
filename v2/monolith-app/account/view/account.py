from flask import jsonify

class AccountView():
    def detail(self, message, status_code=201):
        return jsonify(message), status_code

    def delete_success(self):
        return jsonify({ "message" : "account has been deleted successfully" }), 201
    
    def list(self, message):
        return jsonify(message), 201

    def settlement_success(self):
        return jsonify({"message" : "settlement success!"}), 201

    def not_found_account_number(self, message = None):
        if message == None:
            return jsonify({ "message" : "account number is not found" }), 400
        else:
            return jsonify({"message" : message}), 400

    def settlement_failed(self):
        return jsonify({"message" : "settlement failed!"}), 500