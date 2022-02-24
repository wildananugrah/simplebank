from flask import jsonify

class TransferView():
    
    def list(self, message, status_code = 200):
        return jsonify(message), status_code

    def detail(self, message, status_code = 201):
        return jsonify(message), status_code

    def delete_success(self):
        return jsonify({ 'message' : 'account has been deleted successfully' }), 201
    
    def not_found_account_number(self):
        return jsonify({'message' : 'account number not found!'}), 400

    def unsufficient_balance(self, message = "unsufficient balance!"):
        return jsonify({ "message" : message }), 400