from locust import HttpUser, task

class SimpleBankTest(HttpUser):
    
    id_number = "31730059100009"
    name = "User Name"
    email = "user@gmail.com"
    cif_number = None

    username = "username"
    password = "password"

    account_1 = None
    account_2 = None
    account_3 = None

    def create_customer(self):
        self.client.post(f"/customer", json={
            "name": name,
            "id_number": id_number,
            "email": email
        })

    def all_customer(self):
        self.client.get(f"/customers")

    def select_by_cif(self):
        self.client.get(f"/customer/cif?cif_number={cif_number}")
    
    def select_by_id_number(self):
        self.client.get(f"/customer/id_number?id_number={id_number}")

    def delete_by_cif(self):
        self.client.delete(f"/customer/cif?cif_number={cif_number}")

    def delete_by_id_number(self):
        self.client.delete(f"/customer/id_number?id_number={id_number}")

    def update_customer(self):
        self.client.put(f"/customer", json={
            "name": name,
            "id_number": id_number,
            "email": email
        })
    
    def update_customer_login(self):
        self.client.put(f"/customer_user", json={ "username" : username, "password" : password, "cif_number" : cif_number })

    def customer_login(self):
        self.client.post(f"/customer/login", json={ "username" : username, "password" : password })

    def create_account(self):
        self.client.post(f"/account", json={
            "cif_number": cif_number,
            "currency": "IDR",
            "balance": 0
        })

    def select_all_accounts(self):
        self.client.get(f"/accounts")

    def select_account_by_cif(self):
        self.client.get(f"/accounts/cif_number?cif_number={cif_number}")

    def delete_account(self, account):
        self.client.delete(f"/account?account={account}")

    def deposit_account(self, account, amount):
        self.client.post(f"/deposit", json={"account_number" : account, "amount" : amount})
    
    def transfer_account(self, from_account, to_account, amount):
        self.client.post(f"/transfer", json={ "to_account_number" : to_account, "from_account_number" : from_account, "amount" : amount })
    
    def bill_inquiry(self):
        self.client.post(f"/bill/inquiry/tax", json={
            "bill_id" : "001"
        })

    def bill_payment(self, account):
        self.client.post(f"/bill/payment/tax", json={
            "bill_id" : "001",
            "account_number": account,
            "amount": 10
        })

    def historical(self, account):
        self.client.get(f"/historical_transaction?account_number={account}")

    @task
    def run_task(self):

        # 1. create customer
        self.create_customer()
        
        # 2. all customers
        self.all_customer()
        
        # 3. customer by cif
        self.select_by_cif()
        
        # 4. customer by id_number
        self.select_by_id_number()
        
        # 5. delete by cif
        self.delete_by_cif()
        
        # 6. create customer
        self.create_customer()
        
        # 7. delete by id_number
        self.delete_by_id_number()
        
        # 8. create customer
        self.create_customer()
        
        # 9. update customer
        self.update_customer()
        
        # 10. update username password
        self.update_customer_login()
        
        # 11. customer login
        self.customer_login()
        
        # 12. create account 1
        self.create_account()

        # 13. create account 2
        self.create_account()
        
        # 14. create account 3
        self.create_account()
        
        # 15. get all accounts
        self.select_all_accounts()

        # 16. get account by cif
        self.select_account_by_cif()

        # 17. deposit account 1 10000
        self.deposit_account(account_1, 10000)

        # 18. transfer account 1 to account 2 100
        self.transfer_account(account_1, account_2, 100)

        # 19. historical transaction account 1 2x
        self.historical(account_1)
        
        # 20. historical transaction acctoun 2 1x
        self.historical(account_2)
        
        # 21. payment inquiry
        self.bill_inquiry()

        # 22. payment pay account 1
        self.bill_payment(account_1)

        # 23. historical transaction count 1 3x
        self.historical(account_1)
        # 24. delete accounts
        self.delete_account(account_1)
        self.delete_account(account_2)
        self.delete_account(account_3)

        # 25. delete customer
        self.delete_by_id_number()