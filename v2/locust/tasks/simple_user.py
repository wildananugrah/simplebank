from locust import SequentialTaskSet, task

class SimpleUser(SequentialTaskSet):

    def on_start(self):
        print("UserLogin: Tasks execution started..")
        self.cif_number = None
        self.account_number = None
        self.deposit_amount = 10000
        self.bill_id = "830090890024"
        self.transaction_id = None
        self.interbank_account_number = None
        self.interbank_bank_code = None
        self.interbank_account_name = None
        self.to_account_number = "0949140897"
        
    def on_stop(self):
        print("UserLogin: Tasks execution completed..")

    @task
    def login(self):
        data = {
            "username": self.user.username,
            "password": self.user.password
        }

        with self.client.post("/customer/login", json=data, catch_response=True, name="login") as response:
            if response.status_code not in (200, 201):
                response.failure("Failed to login, status_code: " + str(response.status_code))
            else:
                self.cif_number = response.json()['customer_data']['cif_number']
                response.success()
    
    @task
    def create_account(self):
        data = {
            "cif_number" : self.cif_number,
            'currency' : 'IDR'
        }

        with self.client.post("/account", json=data, catch_response=True, name="account_create") as response:
            if response.status_code not in (200, 201):
                response.failure("Failed to create account, status_code: " + str(response.status_code))
            else:
                self.account_number = response.json()['account_number']
                response.success()

    @task
    def detail_account(self):
        with self.client.get(f"/account?account_number={self.account_number}", catch_response=True, name="account_detail") as response:
            if response.status_code not in (200, 201):
                response.failure("Failed to get account detail, status_code: " + str(response.status_code))
            else:
                response.success()

    @task
    def list_account(self):
        with self.client.get(f"/account/list?cif_number={self.cif_number}", catch_response=True, name="Account list") as response:
            if response.status_code not in (200, 201):
                response.failure("Failed to get account list, status_code:" + str(response.status_code))
            else:
                response.success()
    
    @task
    def deposit(self):
        data = {
            "account_number": self.account_number,
            "amount": self.deposit_amount,
            "description": f"test {self.account_number} deposit"
        }
        with self.client.post("/account/deposit/", json=data, catch_response=True, name="deposit account") as response:
            if response.status_code not in (200, 201):
                response.failure("Failed to deposit account, status_code: " + str(response.status_code))
            else:
                response.success()

    @task
    def inquiry_interbank_account(self):
        with self.client.get("/transfer/interbank/account_number?account_number=3540447401&bank_code=014", catch_response=True, name="inquiry interbank account") as response:
            if response.status_code not in (200, 201):
                response.failure("Failed to inquiry interbank account, status_code: " + str(response.status_code))
            else:
                self.interbank_account_number = response.json()['account_number']
                self.interbank_bank_code = response.json()['bank_code']
                self.interbank_account_name = response.json()['account_name']
                response.success()

    @task
    def save_account(self):
        data = {
            "cif_number" : self.cif_number,
            "account_number" : self.interbank_account_number,
            "bank_code" : self.interbank_bank_code,
            "account_name" : self.interbank_account_name
        }

        with self.client.post("/transfer/save/account_number", json=data, catch_response=True, name="save transfer account") as response:
            if response.status_code not in (200, 201):
                response.failure("Failed to save interbank account, status_code: " + str(response.status_code))
            else:
                response.success()
    
    @task
    def list_save_account(self):
        with self.client.get(f"/transfer/list/account_number?cif_number={self.cif_number}", catch_response=True, name="list save account") as response:
            if response.status_code not in (200, 201):
                response.failure("Failed to list save account, status_code: " + str(response.status_code))
            else:
                response.success()
                # if len(response.json()) == 1:
                #     response.success()
                # else:
                #     response.failure("Failed to len save account " + str(len(response.json())) + " ")

    @task
    def transfer_account(self):
        data = {
            "from_account_number": self.account_number,
            "to_account_number": self.to_account_number, 
            "amount" : 1,
            "description" : "TEST FROM ACCOUNT",
            "cif_number" : self.cif_number
        }

        with self.client.post(f"/transfer/", json=data, catch_response=True, name="transfer") as response:
            if response.status_code not in (200, 201):
                print(data)
                response.failure("Failed to transfer account, status_code: " + str(response.status_code))
            else:
                response.success()

    @task
    def transfer_interbank(self):
        data = {
            "from_account_number": self.account_number,
            "to_account_number": "3540447401",
            "bank_code":"014",
            "amount" : 1,
            "description" : "TEST INTERBANK",
            "cif_number" : self.cif_number
        }

        with self.client.post("/transfer/interbank/", json=data, catch_response=True, name="transfer interbank") as response:
            if response.status_code not in (200, 201):
                response.failure("Failed to transfer interbank account, status_code: " + str(response.status_code))
            else:
                response.success()
    
    @task
    def bill_inquiry(self):
        with self.client.get(f"/payment/bill/inquiry/?bill_id={self.bill_id}", catch_response=True, name="bill inquiry") as response:
            if response.status_code not in (200, 201):
                response.failure("Failed to bill inquiry, status_code: " + str(response.status_code))
            else:
                response.success()
    
    @task
    def bill_payment(self):
        data = {
            "bill_id" : self.bill_id,
            "account_number" : self.account_number,
            "biller_name" : "telkomsel",
            "amount" : 10,
            "cif_number" : self.cif_number,
            "description":  "TEST PAYMENT !",
            "biller_request_message" : {
                "bill_id" : self.bill_id,
                "amount" : 10,
                "detail" : "0813-1600-6010",
                "description" : "TEST PAYMENT"
            }
        }

        with self.client.post(f"/payment/bill/payment", json=data, catch_response=True, name="bill payment") as response:
            if response.status_code not in (200, 201):
                response.failure("Failed to bill payment, status_code: " + str(response.status_code))
            else:
                response.success()

    @task
    def payment_list(self):
        with self.client.get(f"/payment/list?cif_number={self.cif_number}", catch_response=True, name="bill payment list") as response:
            if response.status_code not in (200, 201):
                self.transaction_id = response.json()[0]['transaction_id']
                response.failure("Failed to bill payment list, status_code: " + str(response.status_code))
            else:
                response.success()
    
    @task
    def payment_detail(self):
        with self.client.get(f"/payment/detail?transaction_id={self.transaction_id}", catch_response=True, name="bill payment list") as response:
            if response.status_code not in (200, 201):
                response.failure("Failed to bill payment list, status_code: " + str(response.status_code))
            else:
                response.success()

    @task
    def delete_account(self):
        with self.client.delete(f"/account?account_number={self.account_number}", catch_response=True, name="account_delete") as response:
            if response.status_code not in (200, 201):
                response.failure("Failed to delete account, status_code: " + str(response.status_code))
            else:
                response.success()

    @task 
    def exit_task_execution(self):
        self.interrupt()