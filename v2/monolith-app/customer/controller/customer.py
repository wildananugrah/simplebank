from customer.view.customer import *
from customer.model.customer import *

class CustomerController():

    def __init__(self):
        self.model = model = CustomerModel()

    def detail(self,id_type, value):

        message = None
        
        if id_type == 'cif_number':
            message = self.model.detail_by_cif(value)
        elif id_type == 'id_number':
            message = self.model.detail_by_id_number(value)

        if message:
            return CustomerView().detail(message)
        else:
            return CustomerView().detail({ 'message' : 'customer not found.' }, 400)

    def login(self,json_request):
        username = json_request['username']
        password = json_request['password']

        customer = self.model.login(username, password)

        if customer:
            cif_number = customer['cif_number']
            session_id = self.create_session_id(cif_number)
            self.model.update_session(cif_number, session_id, True)
            return CustomerView().login_success(customer, session_id)
        else:
            return CustomerView().invalid_username_or_password()

    def logout(self, json_request):
        session_id = json_request['session_id']

        if self.model.validate_session(session_id):
            message = self.model.logout(session_id)
        else:
            message = { "message"  : "session id invalid" }

        return CustomerView().detail(message)

    def create_session_id(self, cif_number):
        data = json.dumps({
            "cif_number" : cif_number,
            "datetime": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "uuid": str(uuid4())
        })
        data_bytes = data.encode('ascii')
        base64_bytes = base64.b64encode(data_bytes)
        base64_string = base64_bytes.decode("ascii")

        return base64_string