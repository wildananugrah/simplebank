import pytest
import requests

host = "http://localhost:3000"
id_number = "1605058497852873"
cif_number = "1681274973"
username_1 = "user1"
email_1 = "user0@gmail.com"
password_1 = "password"
bill_id = "458625142578"

pytest.ACCOUNT_NUMBER = None

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

@pytest.mark.run(order=5)
def test_customer_internet_banking_login():
    data = {
        "email": email_1,
        "password" : password_1
    }
    response = requests.post(f"{host}/customer/internet_banking/login/", json=data)

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

    return response.json()['data']

@pytest.mark.run(order=6)
def test_customer_internet_banking_logout():

    data = {
        "session_id": test_customer_internet_banking_login()['session_id']
    }

    response = requests.post(f"{host}/customer/internet_banking/logout/", json=data)

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

# CUSTOMER TEST [ENDED]