import pytest
import requests

host = "http://localhost:3010"
cif_number = "1681274973"

pytest.ACCOUNT_NUMBER = None

# ACCOUNT TEST [STARTED]

@pytest.mark.run(order=7)
def test_account_create():

    data = {
        "cif_number": cif_number
    }

    response = requests.post(f"{host}/account/", json=data)

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

    return response.json()

@pytest.mark.run(order=8)
def test_account_list():
    response = requests.get(f"{host}/account/list/?cif_number={cif_number}")

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict
    assert type(response.json()['data']) is list

    return response.json()['data']

@pytest.mark.run(order=9)
def test_account_detail():
    account = test_account_list()[0]
    response = requests.get(f"{host}/account/?account_number={account['account_number']}")

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

@pytest.mark.run(order=10)
def test_account_update():
    account = test_account_list()[0]
    data = {
        'account_number' : account['account_number'],
        'current_balance' : 100
    }

    response = requests.put(f"{host}/account/", json=data)

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

@pytest.mark.run(order=11)
def test_account_delete():
    account = test_account_list()[0]
    response = requests.delete(f"{host}/account/?account_number={account['account_number']}")

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

# ACCOUNT TEST [ENDED]