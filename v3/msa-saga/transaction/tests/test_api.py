import pytest
import requests

host = "http://localhost:3020"
cif_number = "1681274973" # must exist in customer database

pytest.ACCOUNT_NUMBER = None

# HELPERS [STARTED]

def create_account():
    data = { 'cif_number' : cif_number }
    return requests.post("http://localhost:3010/account/", json=data).json()['data']

# HELPERS [ENDED]

# TRANSACTION TEST [STARTED]

@pytest.mark.run(order=11)
def test_transaction_deposit():
    pytest.ACCOUNT_NUMBER = create_account()
    data = {
        "account_number": pytest.ACCOUNT_NUMBER['account_number'],
        "amount": 1000
    }
    response = requests.post(f"{host}/transaction/deposit/", json=data)

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

@pytest.mark.run(order=12)
def test_transaction_intrabank():
    to_account_number = create_account()
    data = {
        "from_account_number": pytest.ACCOUNT_NUMBER['account_number'],
        "to_account_number": to_account_number['account_number'],
        "cif_number": pytest.ACCOUNT_NUMBER['cif_number'],
        "amount": 1,
        "description": "TEST INTRABANK"
    }
    response = requests.post(f"{host}/transaction/transfer/intrabank/", json=data)

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

@pytest.mark.run(order=14)
def test_transaction_debit():
    data = {
        "from_account_number": pytest.ACCOUNT_NUMBER['account_number'],
        "cif_number": pytest.ACCOUNT_NUMBER['cif_number'],
        "amount": 1,
        "description": "TEST INTERBANK",
        "transaction_type" : "INTERBANK"
    }

    response = requests.post(f"{host}/transaction/debit/", json=data)
    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict