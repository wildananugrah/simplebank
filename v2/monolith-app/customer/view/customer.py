from flask import jsonify

class CustomerView():
    def detail(self, message, status_code = 201):
        return jsonify(message), status_code

    def login_success(self, customer, session_id):
        return jsonify({ 'session_id' :  session_id, 'customer_data' : customer})
    
    def invalid_username_or_password(self):
        return jsonify({"message" : "invalid username or password"}), 400