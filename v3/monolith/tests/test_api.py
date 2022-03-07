import pytest
import requests

host = "http://localhost:3000"
id_number = "1605058497852873"
cif_number = "1681274973"
username_1 = "user1"
password_1 = "password"
bill_id = "458625142578"

pytest.ACCOUNT_NUMBER = None

# HELPERS [STARTED]

def find_customer(usename, password):
    customer_mobile = CustomerMobile()
    customer_mobile.username = usename
    customer_mobile.password = password

    customer_mobile = customer_mobile.login()

    return customer_mobile

def find_accounts(cif_number):
    account = Account()
    account = account.list(cif_number)
    return account

def create_account(cif_number):
    account = Account()
    account = account.create(cif_number)
    return account

def delete_account(account_number):
    account = Account()
    account = account.delete(account_number)
    return account

# HELPERS [ENDED]

# CUSTOMER TEST [STARTED]

@pytest.mark.run(order=1)
def test_customer_find_by_id_number():
    response = requests.get(f"{host}/customer/?key_type=id_number&value={id_number}")
    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

@pytest.mark.run(order=2)
def test_customer_find_by_cif_number():
    response = requests.get(f"{host}/customer/?key_type=cif_number&value={cif_number}")
    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

@pytest.mark.run(order=3)
def test_customer_mobile_login():
    data = {
        "username": username_1,
        "password" : password_1
    }
    response = requests.post(f"{host}/customer/mobile/login/", json=data)

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

    return response.json()['data']

@pytest.mark.run(order=4)
def test_customer_mobile_logout():

    data = {
        "session_id": test_customer_mobile_login()['session_id']
    }

    response = requests.post(f"{host}/customer/mobile/logout/", json=data)

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

# CUSTOMER TEST [ENDED]

# ACCOUNT TEST [STARTED]

@pytest.mark.run(order=5)
def test_account_create():

    data = {
        "cif_number": cif_number
    }

    response = requests.post(f"{host}/account/", json=data)

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

    return response.json()

@pytest.mark.run(order=5)
def test_account_list():
    response = requests.get(f"{host}/account/list/?cif_number={cif_number}")

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict
    assert type(response.json()['data']) is list

    return response.json()['data']

@pytest.mark.run(order=6)
def test_account_detail():
    account = test_account_list()[0]
    response = requests.get(f"{host}/account/?account_number={account['account_number']}")

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

@pytest.mark.run(order=7)
def test_account_delete():
    account = test_account_list()[0]
    response = requests.delete(f"{host}/account/?account_number={account['account_number']}")

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

# ACCOUNT TEST [ENDED]

# TRANSFER TEST [STARTED]

@pytest.mark.run(order=8)
def test_transaction_deposit():
    pytest.ACCOUNT_NUMBER = test_account_create()['data']
    data = {
        "account_number": pytest.ACCOUNT_NUMBER['account_number'],
        "amount": 1000
    }
    response = requests.post(f"{host}/transaction/deposit/", json=data)

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

@pytest.mark.run(order=9)
def test_transaction_intrabank():
    to_account_number = test_account_create()
    data = {
        "from_account_number": pytest.ACCOUNT_NUMBER['account_number'],
        "to_account_number": to_account_number['data']['account_number'],
        "cif_number": pytest.ACCOUNT_NUMBER['cif_number'],
        "amount": 1,
        "description": "TEST INTRABANK"
    }
    response = requests.post(f"{host}/transaction/transfer/intrabank/", json=data)

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

@pytest.mark.run(order=10)
def test_transaction_interbank_inquiry():
    response = requests.get(f"{host}/transaction/transfer/interbank/?to_account_number=3540447401&to_bank_code=014")
    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

@pytest.mark.run(order=11)
def test_transaction_interbank_transfer():
    data = {
        "from_account_number": pytest.ACCOUNT_NUMBER['account_number'],
        "to_account_number": "3540447401",
        "to_bank_code": "014",
        "cif_number": pytest.ACCOUNT_NUMBER['cif_number'],
        "amount": 1,
        "description": "TEST INTERBANK"
    }

    response = requests.post(f"{host}/transaction/transfer/interbank/", json=data)
    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

@pytest.mark.run(order=12)
def test_transaction_eletric_payment_inquiry():
    response = requests.get(f"{host}/transaction/payment/eletrical/?bill_id={bill_id}")
    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

@pytest.mark.run(order=13)
def test_transaction_eletric_payment_pay():
    data = {
        "bill_id":bill_id,
        "amount": 1,
        "description": "TEST PAYMENT ELETRICAL PAYMENT",
        "from_account_number": pytest.ACCOUNT_NUMBER['account_number'],
        "cif_number": pytest.ACCOUNT_NUMBER['cif_number']
    }
    response = requests.post(f"{host}/transaction/payment/eletrical/", json=data)
    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

@pytest.mark.run(order=14)
def test_transaction_list():
    response = requests.get(f"{host}/transaction/list/?cif_number={pytest.ACCOUNT_NUMBER['cif_number']}")

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict
    assert type(response.json()['data']) is list

    for transaction in response.json()['data']:
        response_detail = requests.get(f"{host}/transaction/?transaction_type={transaction['transaction_type']}&account_number={transaction['from_account_number']}&journal_number={transaction['journal_number']}")
        assert response is not None
        assert response.status_code in (200, 201)
        assert type(response.json()) is dict

# TRANSFER TEST [ENDED]

# PAYMENT TEST [STARTED]

# PAYMENT TEST [ENDED]