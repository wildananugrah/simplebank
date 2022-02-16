import time
from locust import HttpUser, task, between, SequentialTaskSet

class SimpleBankTest(SequentialTaskSet):

    id_number = "31730059100009"
    name = "User Name"
    email = "user@gmail.com"
    cif_number = None

    username = "username"
    password = "password"

    account_1 = None
    account_2 = None
    account_3 = None

    def create_customer(self, name, id_number, email):
        return self.client.post(f"/customer", json={
            "name": self.name,
            "id_number": self.id_number,
            "email": self.email
        })

    def all_customer(self):
        return self.client.get(f"/customers")

    def select_by_cif(self, cif_number):
        return self.client.get(f"/customer/cif?cif_number={cif_number}", name="/select_by_cif")
    
    def select_by_id_number(self, id_number):
        return self.client.get(f"/customer/id_number?id_number={id_number}", name="/select_by_id_number")

    def delete_by_cif(self, cif_number):
        return self.client.delete(f"/customer/cif?cif_number={cif_number}", name="/delete_by_cif")

    def delete_by_id_number(self, id_number):
        return self.client.delete(f"/customer/id_number?id_number={id_number}", name="/delete_by_id_number")

    def update_customer(self, name, id_number, email, cif_number):
        return self.client.put(f"/customer?cif_number={cif_number}", json={
            "name": name,
            "id_number": id_number,
            "email": email
        }, name="/update_customer")
    
    def update_customer_login(self, username, password, cif_number):
        return self.client.put(f"/customer_user", json={ "username" : username, "password" : password, "cif_number" : cif_number })

    def customer_login(self, username, password):
        return self.client.post(f"/customer/login", json={ "username" : username, "password" : password })

    def create_account(self, cif_number):
        return self.client.post(f"/account", json={
            "cif_number": cif_number,
            "currency": "IDR",
            "balance": 0
        })

    def select_all_accounts(self):
        return self.client.get(f"/accounts")

    def select_account_by_cif(self, cif_number):
        return self.client.get(f"/accounts/cif_number?cif_number={cif_number}", name="/select_account_by_cif")

    def delete_account(self, account):
        return self.client.delete(f"/account?account={account}", name="/delete_account")

    def deposit_account(self, account, amount):
        return self.client.post(f"/deposit", json={"account_number" : account, "amount" : amount})
    
    def transfer_account(self, from_account, to_account, amount):
        return self.client.post(f"/transfer", json={ "to_account_number" : to_account, "from_account_number" : from_account, "amount" : amount })
    
    def bill_inquiry(self):
        return self.client.post(f"/bill/inquiry/tax", json={
            "bill_id" : "001"
        })

    def bill_payment(self, account):
        return self.client.post(f"/bill/payment/tax", json={
            "bill_id" : "001",
            "account_number": account,
            "amount": 10
        })

    def historical(self, account):
        return self.client.get(f"/historical_transaction?account_number={account}", name="/historical")

    @task
    def task_1(self):
        response = self.create_customer(self.name, self.id_number, self.email)
        if response.status_code == 200:
            self.cif_number = response.json()['cif_number']

    @task
    def task_2(self):
        self.all_customer()

    @task
    def task_3(self):
        self.select_by_cif(cif_number=self.cif_number)

    @task
    def task_4(self):
        self.select_by_id_number(id_number=self.id_number)

    @task
    def task_5(self):
        self.delete_by_cif(cif_number=self.cif_number)

    @task
    def task_6(self):
        self.create_customer(self.name, self.id_number, self.email)

    @task
    def task_7(self):
        self.delete_by_id_number(self.id_number)

    @task
    def task_8(self):
        response = self.create_customer(self.name, self.id_number, self.email)
        if response.status_code == 200:
            self.cif_number = response.json()['cif_number']

    @task
    def task_9(self):
        self.update_customer(self.name, self.id_number, self.email, self.cif_number)

    @task
    def task_10(self):
        self.update_customer_login(self.username, self.password, self.cif_number)
    
    @task
    def task_11(self):
        self.customer_login(self.username, self.password)

    @task
    def task_12(self):
        response = self.create_account(self.cif_number)
        if response.status_code == 200:
            self.account_1 = response.json()['account']
    
    @task
    def task_13(self):
        response = self.create_account(self.cif_number)
        if response.status_code == 200:
            self.account_2 = response.json()['account']

    @task
    def task_14(self):
        response = self.create_account(self.cif_number)
        if response.status_code == 200:
            self.account_3 = response.json()['account']

    @task
    def task_15(self):
        self.select_all_accounts()

    @task
    def task_16(self):
        self.select_account_by_cif(self.cif_number)

    @task
    def task_17(self):
        self.deposit_account(self.account_1, 10000)
    
    @task
    def task_18(self):
        self.transfer_account(self.account_1, self.account_2, 100)

    @task
    def task_19(self):
        self.historical(self.account_1)

    @task
    def task_20(self):
        self.historical(self.account_2)

    @task
    def task_21(self):
        self.bill_inquiry()

    @task
    def task_22(self):
        self.bill_payment(self.account_1)

    @task 
    def task_23(self):
        self.historical(self.account_1)

    @task
    def task_24(self):
        self.delete_account(self.account_1)
        self.delete_account(self.account_2)
        self.delete_account(self.account_3)
    
    @task
    def task_25(self):
        self.delete_by_id_number(self.id_number)

class MyLoadTest(HttpUser):
    min_wait = 5000
    max_wait = 15000

    tasks = [SimpleBankTest]