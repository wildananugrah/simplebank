import requests

class TestApp():

    def __init__(self):

        self.is_debug = True
        self.host = "http://localhost:8000"

        self.id_number = "31730059100009"
        self.name = "User Name"
        self.email = "user@gmail.com"
        self.cif_number = None

        self.username = "username"
        self.password = "password"

        self.account_1 = None
        self.account_2 = None
        self.account_3 = None
    
    def create_customer(self):
        print("== create customer ==")
        response = requests.post(f"{self.host}/customer", json={
            "name": self.name,
            "id_number": self.id_number,
            "email": self.email
        })

        if response.status_code == 200:
            self.cif_number = response.json()['cif_number']

        self.debug(response)

    def all_customer(self):
        print("== select all customers ==")
        response = requests.get(f"{self.host}/customers")
        self.debug(response)

    def select_by_cif(self):
        print("== select by cif number == ")
        response = requests.get(f"{self.host}/customer/cif?cif_number={self.cif_number}")
        self.debug(response)
    
    def select_by_id_number(self):
        print("== select by id number == ")
        response = requests.get(f"{self.host}/customer/id_number?id_number={self.id_number}")
        self.debug(response)

    def delete_by_cif(self):
        print("== delete by cif == ")
        response = requests.delete(f"{self.host}/customer/cif?cif_number={self.cif_number}")
        self.debug(response)

    def delete_by_id_number(self):
        print("== delete by id number ==")
        response = requests.delete(f"{self.host}/customer/id_number?id_number={self.id_number}")
        self.debug(response)

    def update_customer(self):
        print("== update customer ==")
        response = requests.put(f"{self.host}/customer?cif_number={self.cif_number}", json={
            "name": self.name,
            "id_number": self.id_number,
            "email": self.email
        })
        self.debug(response)
    
    def update_customer_login(self):
        print("== update customer login ==")
        response = requests.put(f"{self.host}/customer_user", json={ "username" : self.username, "password" : self.password, "cif_number" : self.cif_number })
        self.debug(response)

    def customer_login(self):
        print("== customer login ==")
        response = requests.post(f"{self.host}/customer/login", json={ "username" : self.username, "password" : self.password })
        self.debug(response)

    def create_account(self):
        print("== create account ==")
        response = requests.post(f"{self.host}/account", json={
            "cif_number": self.cif_number,
            "currency": "IDR",
            "balance": 0
        })
        self.debug(response)

        if response.status_code == 200:
            return response.json()['account']
        else:
            return None

    def select_all_accounts(self):
        print("== select all accounts ==")
        response = requests.get(f"{self.host}/accounts")
        self.debug(response)

    def select_account_by_cif(self):
        print("== select account by cif ==")
        response = requests.get(f"{self.host}/accounts/cif_number?cif_number={self.cif_number}")
        self.debug(response)

    def delete_account(self, account):
        print(f"== delete account: {account} ==")
        response = requests.delete(f"{self.host}/account?account={account}")
        self.debug(response)

    def deposit_account(self, account, amount):
        print(f"== deposit account: {account} ==")
        response = requests.post(f"{self.host}/deposit", json={"account_number" : account, "amount" : amount})
        self.debug(response)
    
    def transfer_account(self, from_account, to_account, amount):
        print(f"== transfer {from_account} to {to_account} amount: {amount} ==")
        response = requests.post(f"{self.host}/transfer", json={ "to_account_number" : to_account, "from_account_number" : from_account, "amount" : amount })
        self.debug(response)

    def bill_inquiry(self):
        response = requests.post(f"{self.host}/bill/inquiry/tax", json={
            "bill_id" : "001"
        })
        self.debug(response)

    def bill_payment(self, account):
        response = requests.post(f"{self.host}/bill/payment/tax", json={
            "bill_id" : "001",
            "account_number": account,
            "amount": 10
        })
        self.debug(response)

    def historical(self, account):
        print(f"== historical {account} ==")
        response = requests.get(f"{self.host}/historical_transaction?account_number={account}")

        self.debug(response)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def debug(self, response):
        if self.is_debug == True:
            if response.status_code == 200:
                print(f"{response.status_code} {response.text}")
            else:
                print(response.text)

    def run(self):
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
        self.account_1 = self.create_account()

        # 13. create account 2
        self.account_2 = self.create_account()
        
        # 14. create account 3
        self.account_3 = self.create_account()
        
        # 15. get all accounts
        self.select_all_accounts()

        # 16. get account by cif
        self.select_account_by_cif()

        # 17. deposit account 1 10000
        self.deposit_account(self.account_1, 10000)

        # 18. transfer account 1 to account 2 100
        self.transfer_account(self.account_1, self.account_2, 100)

        # 19. historical transaction account 1 2x
        history_trx = self.historical(self.account_1)
        print(f"account 1 len: {len(history_trx)}")
        if len(history_trx) == 2:
            print(f" TRUE ")

        # 20. historical transaction acctoun 2 1x
        history_trx = self.historical(self.account_2)
        print(f"account 2 len: {len(history_trx)}")
        if len(history_trx) == 1:
            print(f" TRUE ")

        # 21. payment inquiry
        self.bill_inquiry()

        # 22. payment pay account 1
        self.bill_payment(self.account_1)

        # 23. historical transaction count 1 3x
        history_trx = self.historical(self.account_1)
        print(f"account 1 len: {len(history_trx)}")
        if len(history_trx) == 3:
            print(f" TRUE ")

        # 24. delete accounts
        self.delete_account(self.account_1)
        self.delete_account(self.account_2)
        self.delete_account(self.account_3)

        # 25. delete customer
        self.delete_by_id_number()

TestApp().run()