from locust import SequentialTaskSet, task
import time

class NormalUser(SequentialTaskSet):

    def on_start(self):
        print("UserLogin: Tasks execution started..")
        self.cif_number = None
        self.id_number = "8705095121996512"
        self.from_account_number = None
        self.to_account_number = None
        self.deposit_amount = 10000
        self.bill_id = "670706837027"
        self.to_interbank_account_number = "3540447401"
        self.session_id = None
        
    def on_stop(self):
        print("UserLogin: Tasks execution completed..")
    
    @task
    def hit_transaction(self):
        
        data = {
            "username": self.user.username,
            "password": self.user.password
        }

        with self.client.post(f"/customer/mobile/login/", json=data, catch_response=True, name="a_test_customer_mobile_login") as response:
            if response.status_code not in (200, 201):
                response.failure("test_customer_mobile_login failed, status_code: " + str(response.status_code) + " " + str(response.text))
            else:
                self.cif_number = response.json()['data']['cif_number']
                self.session_id = response.json()['data']['session_id']
                response.success()

        data = {
            "cif_number" : self.cif_number
        }

        with self.client.post(f"/account/", json=data, catch_response=True, name="b_test_account_create") as response:
            if response.status_code not in (200, 201):
                response.failure("test_account_create failed, status_code: " + str(response.status_code) + " " + str(response.text))
            else:
                self.from_account_number = response.json()['data']['account_number']
                response.success()

        data = {
            "cif_number" : self.cif_number
        }

        with self.client.post(f"/account/", json=data, catch_response=True, name="c_test_account_create_2") as response:
            if response.status_code not in (200, 201):
                response.failure("test_account_create_2 failed, status_code: " + str(response.status_code))
            else:
                self.to_account_number = response.json()['data']['account_number']
                response.success()
        
        with self.client.get(f"/account/?account_number={self.from_account_number}", catch_response=True, name="d_test_account_detail") as response:
            if response.status_code not in (200, 201):
                response.failure("test_account_detail failed, status_code: " + str(response.status_code) + " " + str(response.text))
            else:
                response.success()     

        with self.client.get(f"/account/list/?cif_number={self.cif_number}&skip=0&limit=10", catch_response=True, name="e_test_account_list") as response:
            if response.status_code not in (200, 201):
                response.failure("test_account_list failed, status_code: " + str(response.status_code) + " " + str(response.text))
            else:
                response.success()     
        
        data = {
            "account_number": self.from_account_number,
            "amount": self.deposit_amount
        }

        with self.client.post(f"/transaction/deposit/", json=data, catch_response=True, name="f_test_transaction_deposit") as response:
            if response.status_code not in (200, 201):
                response.failure("test_transaction_deposit failed, status_code: " + str(response.status_code) + " " + str(response.text))
            else:
                response.success()

                data = {
                    "from_account_number": self.from_account_number,
                    "to_account_number": self.to_account_number,
                    "cif_number" : self.cif_number,
                    "amount": 1,
                    "description" : "stress test intrabank"
                }

                with self.client.post(f"/transaction/transfer/intrabank/", json=data, catch_response=True, name="g_test_transaction_intrabank") as response:
                    if response.status_code not in (200, 201):
                        response.failure("test_transaction_intrabank failed, status_code: " + str(response.status_code) + " " + str(response.text))
                    else:
                        response.success()  
            
                with self.client.get(f"/transaction/transfer/interbank/?to_account_number=3540447401&to_bank_code=014", catch_response=True, name="h_test_transaction_interbank_inquiry") as response:
                    if response.status_code not in (200, 201):
                        response.failure("test_transaction_interbank_inquiry failed, status_code: " + str(response.status_code) + " " + str(response.text))
                    else:
                        response.success()

                data = {
                    "from_account_number": self.from_account_number,
                    "to_account_number": self.to_interbank_account_number,
                    "to_bank_code": "014",
                    "cif_number": self.cif_number,
                    "amount": 1,
                    "description": "TEST INTERBANK"
                }

                with self.client.post(f"/transaction/transfer/interbank/", json=data, catch_response=True, name="i_test_transaction_interbank_transfer") as response:
                    if response.status_code not in (200, 201):
                        response.failure("test_transaction_interbank_transfer failed, status_code: " + str(response.status_code) + " " + str(response.text))
                    else:
                        response.success()

                with self.client.get(f"/transaction/payment/eletrical/?bill_id={self.bill_id}", catch_response=True, name="j_test_transaction_eletric_payment_inquiry") as response:
                    if response.status_code not in (200, 201):
                        response.failure("test_transaction_eletric_payment_inquiry failed, status_code: " + str(response.status_code) + " " + str(response.text))
                    else:
                        response.success()
                
                data = {
                    "bill_id":self.bill_id,
                    "amount": 1,
                    "description": "TEST PAYMENT ELETRICAL PAYMENT",
                    "from_account_number": self.from_account_number,
                    "cif_number": self.cif_number
                }

                with self.client.post(f"/transaction/payment/eletrical/", json=data, catch_response=True, name="k_test_transaction_eletric_payment_pay") as response:
                    if response.status_code not in (200, 201):
                        response.failure("test_transaction_eletric_payment_pay failed, status_code: " + str(response.status_code) + " " + str(response.text))
                    else:
                        response.success()      

        with self.client.get(f"/transaction/list/?cif_number={self.cif_number}&skip=0&limit=10", catch_response=True, name="l_test_transaction_list") as response:
            if response.status_code not in (200, 201):
                response.failure("test_transaction_list failed, status_code: " + str(response.status_code) + " " + str(response.text))
            else:
                response.success()
        
        with self.client.get(f"/historical_transaction/?account_number={self.from_account_number}&skip=0&limit=10", catch_response=True, name="m_test_hist_trx") as response:
            if response.status_code not in (200, 201):
                response.failure("test_hist_trx failed, status_code: " + str(response.status_code) + " " + str(response.text))
            else:
                response.success()

        # data = {
        #     "session_id" : self.session_id
        # }
        # with self.client.post(f"/customer/mobile/logout/", json=data, catch_response=True, name="n_test_customer_mobile_logout") as response:
        #     if response.status_code not in (200, 201, 400): # 400 stil okay i guess. pfft
        #         response.failure("test_customer_mobile_logout failed, status_code: " + str(response.status_code) + " session_id: " + str(self.session_id) + ", username: " + str(self.user.username))
        #     else:
        #         response.success()
        
        self.interrupt()