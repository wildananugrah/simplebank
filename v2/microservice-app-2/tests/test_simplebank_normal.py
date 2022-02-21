from dotenv import load_dotenv
from pymongo import MongoClient
import pytest, os, requests, random, string, time, json

# docker stats account customer transfer payment

client = MongoClient("mongodb://localhost:6000/?readPreference=secondary&directConnection=true")
db = client.simplebank_db

client2 = MongoClient("mongodb://localhost:6001/?readPreference=primary&directConnection=true")
db2 = client2.simplebank_db

load_dotenv()

host = "http://localhost:4002"

id_number_fail = '3175023005910001'
session_login_list = []
account_numbers = []
DEPOSIT_AMOUNT = 1000
TRANSFER_AMOUNT = 1
DEBIT_AMOUNT = 1
pytest.TO_ACCOUNT_NUMBER = None
pytest.ACCOUNT_NUMBERS_AND_CIF_NUMBERS = []

@pytest.mark.run(order=1)
def test_inquiry_customer_by_id_number_success():
    customers = db.customers.find({},{'_id' : False})
    for customer in customers:
        response = requests.get(f"{host}/customer/?id_type=id_number&value={customer['id_number']}")
        assert response.status_code in (200, 201)

@pytest.mark.run(order=2)
def test_inquiry_customer_by_id_number_fail():
    response = requests.get(f"{host}/customer/?id_type=id_number&value={id_number_fail}")
    assert 400 == response.status_code

@pytest.mark.run(order=3)
def test_login():
    customers = db.customers.find({},{'_id' : False})
    for customer in customers:
        data = {
            "username": customer['username'],
            "password": customer['password']
        }

        response = requests.post(f"{host}/customer/login", json=data)
        response_json = response.json()
        session_login_list.append({ 'cif_number' : customer['cif_number'] , 'is_login' : response_json['customer_data']['is_login'], 'session_id' : response_json['session_id']})
        assert response.status_code in (200, 201)

@pytest.mark.run(order=4)
def test_session_validation():
    for session_login in session_login_list:
        customer = db.customers.find_one({ 'cif_number' : session_login['cif_number'] })
        assert type(customer) == dict
        assert customer != None
        assert customer['is_login'] == True and customer['session_id'] != ''

@pytest.mark.run(order=5)
def test_logout():
    for session_login in session_login_list:
        data = { 'session_id' : session_login['session_id'] }
        response = requests.post(f"{host}/customer/logout?", json=data)
        assert response.status_code in (200, 201)

@pytest.mark.run(order=6)
def test_session_validation_logout():
    for session_login in session_login_list:
        customer = db.customers.find_one({ 'cif_number' : session_login['cif_number'] })
        assert type(customer) == dict
        assert customer != None
        assert customer['is_login'] == False and customer['session_id'] == ''

@pytest.mark.run(order=7)
def test_create_account():
    for customer in session_login_list:
        data = {
            "cif_number" : customer['cif_number'],
            'currency' : 'IDR'
        }

        response = requests.post(f"{host}/account", json=data)

        assert response.status_code in (200, 201)
        assert type(json.loads(response.text)) == dict
        pytest.ACCOUNT_NUMBERS_AND_CIF_NUMBERS.append({ 'account_number' : response.json()['account_number'], 'cif_number' : customer['cif_number'] })
        

@pytest.mark.run(order=8)
def test_get_account():
    for account_number_and_cif_number in pytest.ACCOUNT_NUMBERS_AND_CIF_NUMBERS:
        response = requests.get(f"{host}/account?account_number={account_number_and_cif_number['account_number']}")

        assert response.status_code in (200, 201)
        assert type(response.json()) == dict

        cif_number = response.json()['cif_number']

        response = requests.get(f"{host}/customer/?id_type=cif_number&value={cif_number}")
        assert response.status_code in (200, 201)

@pytest.mark.run(order=9)
def test_account_list_cif_number():
    for customer in session_login_list:
        response = requests.get(f"{host}/account/list?cif_number={customer['cif_number']}")
        assert response.status_code in (200, 201)
        assert type(response.json()) == list
        
        for x in response.json():
            assert type(x) == dict

        assert len(response.json()) == 1

@pytest.mark.run(order=10)
def test_deposit():

    for account_number_and_cif_number in pytest.ACCOUNT_NUMBERS_AND_CIF_NUMBERS:
        data = {
            "account_number": account_number_and_cif_number['account_number'],
            "amount": DEPOSIT_AMOUNT,
            "description": f"test {account_number_and_cif_number['account_number']} deposit"
        }

        response = requests.post(f"{host}/account/deposit/", json=data)

        assert response.status_code in (200, 201)
        assert response.json()['data']['amount'] == DEPOSIT_AMOUNT
        assert response.json()['data']['journal_number'] not in (None, '')
        assert response.json()['data']['account_number'] == account_number_and_cif_number['account_number']

@pytest.mark.run(order=11)
def test_transfer_from_account():
    customer_number = len(session_login_list)

    count = 0

    current_balance = 0
    for account_number_and_cif_number in pytest.ACCOUNT_NUMBERS_AND_CIF_NUMBERS:
        if count == 0:
            pytest.TO_ACCOUNT_NUMBER = account_number_and_cif_number['account_number']
            response = requests.get(f"{host}/account?account_number={account_number_and_cif_number['account_number']}")
            current_balance = response.json()['balance']
        else:
            transaction_id = ''.join(random.choice(string.digits) for _ in range(10))
            data = {
                "from_account_number": account_number_and_cif_number['account_number'],
                "to_account_number": pytest.TO_ACCOUNT_NUMBER,
                "amount": TRANSFER_AMOUNT,
                "transaction_id": transaction_id,
                "description": f"TRF {account_number_and_cif_number['account_number']} to {pytest.TO_ACCOUNT_NUMBER}"
            }
            response = requests.post(f"{host}/account/transfer/", json=data)

            assert response.status_code in (200, 201)
            assert type(response.json()) == dict
            assert transaction_id == response.json()['data']['transaction_id']
        count += 1
    
    for account_number_and_cif_number in pytest.ACCOUNT_NUMBERS_AND_CIF_NUMBERS:
        if account_number_and_cif_number['account_number'] == pytest.TO_ACCOUNT_NUMBER:
            response = requests.get(f"{host}/account?account_number={account_number_and_cif_number['account_number']}")

            assert response.status_code in (200, 201)
            assert response.json()['balance'] == (current_balance + count - 1)

        else:
            response = requests.get(f"{host}/account?account_number={account_number_and_cif_number['account_number']}")

            assert response.status_code in (200, 201)
            assert response.json()['balance'] == (DEPOSIT_AMOUNT - TRANSFER_AMOUNT)
    
    count = 0
    for account_number_and_cif_number in pytest.ACCOUNT_NUMBERS_AND_CIF_NUMBERS:
        if account_number_and_cif_number['account_number'] != pytest.TO_ACCOUNT_NUMBER:
            transaction_id = ''.join(random.choice(string.digits) for _ in range(10))
            data = {
                "from_account_number": pytest.TO_ACCOUNT_NUMBER,
                "to_account_number": account_number_and_cif_number['account_number'],
                "amount": TRANSFER_AMOUNT,
                "transaction_id": transaction_id,
                "description": f"TRF {account_number_and_cif_number['account_number']} to {pytest.TO_ACCOUNT_NUMBER}"
            }
            response = requests.post(f"{host}/account/transfer/", json=data)

            assert response.status_code in (200, 201)
            assert type(response.json()) == dict
            assert transaction_id == response.json()['data']['transaction_id']
            count += 1
    
    assert count == (len(pytest.ACCOUNT_NUMBERS_AND_CIF_NUMBERS) - 1)

@pytest.mark.run(order=12)
def test_debit():
    for account_number in account_numbers:
        transaction_id = ''.join(random.choice(string.digits) for _ in range(10))

        response = requests.get(f"{host}/account?account_number={account_number}")

        assert response.status_code in (200, 201)
        current_balance = response.json()['balance']

        data = {
            "account_number": account_number,
            "amount": DEBIT_AMOUNT,
            "transaction_id": transaction_id,
            "description": f"pembayaran test {account_number}"
        }
        response = requests.post(f"{host}/account/debit/", json=data)
        assert response.status_code in (200, 201)
        assert type(response.json()) == dict

        response = requests.get(f"{host}/account?account_number={account_number}")

        assert response.status_code in (200, 201)
        assert response.json()['balance'] == (current_balance - DEBIT_AMOUNT)

@pytest.mark.run(order=13)
def test_interbank():
    for account_number in account_numbers:
        transaction_id = ''.join(random.choice(string.digits) for _ in range(10))

        response = requests.get(f"{host}/account?account_number={account_number}")

        assert response.status_code in (200, 201)
        current_balance = response.json()['balance']

        data = {
            "account_number": account_number,
            "amount": DEBIT_AMOUNT,
            "transaction_id": transaction_id,
            "description": f"pembayaran test {account_number}",
            "transaction_type":"INTERBANK_TRANSFER"
        }

        response = requests.post(f"{host}/account/transfer/interbank/", json=data)
        assert response.status_code in (200, 201)
        assert type(response.json()) == dict

        response = requests.get(f"{host}/account?account_number={account_number}")

        assert response.status_code in (200, 201)
        assert response.json()['balance'] == (current_balance - DEBIT_AMOUNT)

@pytest.mark.run(order=14)
def test_historical_transactions():
    for account_number in account_numbers:
        response = requests.get(f"{host}/account/historical_transaction?account_number={account_number}")
        assert response.status_code in (200, 201)
        assert type(response.json()) == list
        if account_number == pytest.TO_ACCOUNT_NUMBER:
            assert len(response.json()) == 201
        else:
            # print(response.json())
            assert len(response.json()) == 3
        
        if len(response.json()) > 0:
            assert type(response.json()[0]) == dict

# @pytest.mark.run(order=15) # removed.
# def test_transfer_inquiry_own_account_number():
#     customers = db.customers.find({},{'_id' : False})
#     for customer in customers:
#         response = requests.get(f"{host}/transfer/inquiry/own_account_number/?cif_number={customer['cif_number']}")
#         assert response.status_code in (200, 201)
#         assert type(response.json()) == list
#         assert len(response.json()) == 1
#         assert type(response.json()[0]) == dict

@pytest.mark.run(order=16)
def test_transfer_inquiry_account_number():
    for account_number in account_numbers:
        response = requests.get(f"{host}/transfer/inquiry/account_number?account_number={account_number}")
        assert response.status_code in (200, 201)
        assert type(response.json()) == dict

@pytest.mark.run(order=17)
def test_transfer_inquiry_interbank_account_number():
    response = requests.get(f"{host}/transfer/interbank/account_number?account_number=3540447401&bank_code=014")
    assert response.status_code in (200, 201)
    assert type(response.json()) == dict

@pytest.mark.run(order=18)
def test_transfer_save_account_number():
    customers = db.customers.find({},{'_id' : False})
    for customer in customers:
        response = requests.get(f"{host}/transfer/interbank/account_number?account_number=3540447401&bank_code=014")
        assert response.status_code in (200, 201)
        assert type(response.json()) == dict

        interbank_response = response.json()
        data = {
            "cif_number" : customer['cif_number'],
            "account_number" : interbank_response['account_number'],
            "bank_code" : interbank_response['bank_code'],
            "account_name" : interbank_response['account_name']
        }
        requests.post(f"{host}/transfer/save/account_number", json=data)
        assert response.status_code in (200, 201)
        assert type(response.json()) == dict

@pytest.mark.run(order=19)
def test_transfer_list_account_number():
    customers = db.customers.find({},{'_id' : False})
    for customer in customers:

        response = requests.get(f"{host}/transfer/list/account_number?cif_number={customer['cif_number']}")

        assert response.status_code in (200, 201)
        assert type(response.json()) == list
        assert len(response.json()) == 1
        assert type(response.json()[0]) == dict

@pytest.mark.run(order=20)
def test_transfer_from_transfer():
    pytest.TO_ACCOUNT_NUMBER = None
    count = 0
    for account_numbers_and_cif_number in pytest.ACCOUNT_NUMBERS_AND_CIF_NUMBERS:
        if count == 0:
            pytest.TO_ACCOUNT_NUMBER = account_numbers_and_cif_number['account_number']
        else:
            data = {
                "from_account_number": account_numbers_and_cif_number['account_number'],
                "to_account_number": pytest.TO_ACCOUNT_NUMBER,
                "amount" : 1,
                "description" : "TEST FROM ACCOUNT",
                "cif_number" : account_numbers_and_cif_number['cif_number']
            }
            response = requests.post(f"{host}/transfer/", json=data)
            assert response.status_code in (200, 201)
            assert type(response.json()) == dict
        count += 1

@pytest.mark.run(order=21)
def test_transfer_interbank():
    count = 0
    for account_numbers_and_cif_number in pytest.ACCOUNT_NUMBERS_AND_CIF_NUMBERS:
        data = {
            "from_account_number": account_numbers_and_cif_number['account_number'],
            "to_account_number": "3540447401",
            "bank_code":"014",
            "amount" : 1,
            "description" : "TEST INTERBANK",
            "cif_number" : account_numbers_and_cif_number['cif_number']
        }
        response = requests.post(f"{host}/transfer/interbank/", json=data)
        assert response.status_code in (200, 201)
        assert type(response.json()) == dict

@pytest.mark.run(order=22)
def test_delete_transfer_account_number():
    customers = db.customers.find({},{'_id' : False})
    for customer in customers:

        response = requests.delete(f"{host}/transfer/account_number/?cif_number={customer['cif_number']}&account_number=3540447401&bank_code=014")
        
        assert response.status_code in (200, 201)
        assert type(response.json()) == dict

@pytest.mark.run(order=23)
def test_transfer_list():
    for account_numbers_and_cif_number in pytest.ACCOUNT_NUMBERS_AND_CIF_NUMBERS:

        response = requests.get(f"{host}/transfer?cif_number={account_numbers_and_cif_number['cif_number']}")

        assert response.status_code in (200, 201)
        assert type(response.json()) == list

        if account_numbers_and_cif_number['account_number'] == pytest.TO_ACCOUNT_NUMBER:
            assert len(response.json()) == 1
        else:
            assert len(response.json()) == 2
        assert type(response.json()[0]) == dict
        
        for transfer in response.json():
            response = requests.get(f"{host}/transfer/detail?transaction_id={transfer['transaction_id']}")
            assert response.status_code in (200, 201)
            assert type(response.json()) == dict

@pytest.mark.run(order=24)
def test_delete_account():
    for account_numbers_and_cif_number in pytest.ACCOUNT_NUMBERS_AND_CIF_NUMBERS:
        response = requests.delete(f"{host}/account?account_number={account_numbers_and_cif_number['account_number']}")
        assert response.status_code in (200, 201)
        assert type(response.json()) == dict

    db_accounts = db.accounts.find()
    accounts = []
    for account in db_accounts:
        accounts.append(account)
    
    assert len(accounts) == 0

@pytest.mark.run(order=25)
def test_delete_transfer():
    db2.transfers.delete_many({})

@pytest.mark.run(order=26)
def test_delete_historical_transactions():
    db2.historical_transactions.delete_many({})

@pytest.mark.run(order=27)
def test_delete_db_accounts():
    db2.accounts.delete_many({})

@pytest.mark.run(order=28)
def test_delete_db_payment():
    db2.payments.delete_many({})

@pytest.mark.run(order=29)
def test_delete_db_transfer_accounts():
    db2.transfer_accounts.delete_many({})