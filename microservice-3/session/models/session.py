import requests, os

class SessionModel():

    def login(self, username, password):
        customer_url = os.environ.get("CUSTOMER_HOST")
        response = requests.post(f"{customer_url}/customer/login", json={ "username"  : username, "password" : password})
        if response.status_code == 200:
            return response.json()
        else:
            return False