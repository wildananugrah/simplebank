from flask import jsonify

class AccountView():
    def detail(self, message):
        return jsonify(message)

    def delete_success(self):
        return jsonify({ "message" : "account has been deleted successfully" })
    
    def list(self, message):
        return jsonify(message)

    def settlement_success(self):
        return jsonify({"message" : "settlement success!"})

    def not_found_account_number(self, message = None):
        if message == None:
            return jsonify({ "message" : "account number is not found" }), 400
        else:
            return jsonify({"message" : message}), 400

    def settlement_failed(self):
        return jsonify({"message" : "settlement failed!"}), 500