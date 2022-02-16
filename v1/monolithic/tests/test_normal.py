from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

customer_create_request = {
  "name": "User Name",
  "id_number": "31750230059100001",
  "email": "string"
}

account_create_request = {
    "currency": "IDR",
    "balance": 0
}

customer_login = {
    "username" : "username",
    "password" : "password"
}

deposit_request = {
    "amount": 10000
}

pytest.global_cif_number = None
pytest.global_account_number = None
pytest.global_account_number_2 = None

def test_customers_list():
    response = client.get("/customers")
    assert response.status_code == 200

def test_customer_create():
    response = client.post("/customer", json=customer_create_request)
    response_json = response.json()
    pytest.global_cif_number = response_json['cif_number']
    assert response.status_code == 200

def test_customer_all():
    response = client.get("/customers")
    response_json = response.json()
    assert 1 == len(response_json)

def test_customer_by_cif():
    response = client.get(f"/customer/cif?cif_number={pytest.global_cif_number}")
    response_json = response.json()
    assert response.status_code == 200

def test_customer_by_id_number():
    response = client.get(f"/customer/id_number?id_number={customer_create_request['id_number']}")
    response_json = response.json()
    assert response.status_code == 200

def test_customer_update_by_cif_number():
    response = client.put(f"/customer?cif_number={pytest.global_cif_number}", json=customer_create_request)
    response_json = response.json()
    assert response.status_code == 200

def test_update_customer_user():
    customer_login['cif_number'] = pytest.global_cif_number
    response = client.put(f"/customer_user", json=customer_login)
    response_json = response.json()
    assert response.status_code == 200

def test_customer_login():
    response = client.post(f"/customer/login", json=customer_login)
    response_json = response.json()
    assert response.status_code == 200

def test_create_account():
    account_create_request['cif_number'] = pytest.global_cif_number
    response = client.post(f"/account", json=account_create_request)
    response_json = response.json()
    pytest.global_account_number = response_json['account']
    assert response.status_code == 200

def test_create_account_2():
    account_create_request['cif_number'] = pytest.global_cif_number
    response = client.post(f"/account", json=account_create_request)
    response_json = response.json()
    pytest.global_account_number_2 = response_json['account']
    assert response.status_code == 200

def test_detail_account():
    response = client.get(f"/account?account={pytest.global_account_number}")
    response_json = response.json()
    assert response.status_code == 200

def test_all_account():
    response = client.get(f"/accounts")
    response_json = response.json()
    assert 2 == len(response_json)

def test_deposit():
    deposit_request['account_number'] = pytest.global_account_number
    response = client.post(f"/deposit", json=deposit_request)
    assert response.status_code == 200

def test_transfer():
    response = client.post(f"/transfer", json={
        "to_account_number": pytest.global_account_number_2,
        "from_account_number": pytest.global_account_number,
        "amount": 100
    })
    assert response.status_code == 200

def test_bill_inquiry_tax():
    response = client.post(f"/bill/inquiry/tax", json={ "bill_id" : "100" })
    assert response.status_code == 200

def test_bill_payment_tax():
    response = client.post(f"/bill/payment/tax", json={ "bill_id" : "100", "amount" : 100, "account_number" : pytest.global_account_number })
    assert response.status_code == 200

def test_historical_transaction():
    response = client.get(f"/historical_transaction?account_number={pytest.global_account_number}", )
    response_json = response.json()
    assert 3 == len(response_json)

def test_delete_account():
    response = client.delete(f"/account?account={pytest.global_account_number}")
    response_json = response.json()
    assert response.status_code == 200

def test_delete_account_2():
    response = client.delete(f"/account?account={pytest.global_account_number_2}")
    response_json = response.json()
    assert response.status_code == 200

def test_customer_delete_by_cif_number():
    response = client.delete(f"/customer/cif?cif_number={pytest.global_cif_number}")
    assert response.status_code == 200

def test_customer_create_2():
    response = client.post("/customer", json=customer_create_request)
    response_json = response.json()
    pytest.global_cif_number = response_json['cif_number']
    assert response.status_code == 200

def test_customer_delete_by_id_number():
    response = client.delete(f"/customer/id_number?id_number={customer_create_request['id_number']}")
    response_json = response.json()
    assert response.status_code == 200