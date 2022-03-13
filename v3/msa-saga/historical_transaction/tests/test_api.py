import pytest
import requests

host = "http://localhost:3030"

pytest.ACCOUNT_NUMBER = None


# HISTORY TEST [STARTED]

@pytest.mark.run(order=18)      
def test_hist_save():
    data = {
        "transaction_type": "INTERBANK",
        "account_number": "1234567890",
        "amount": 0,
        "journal_number": "123456",
        "current_balance": 1000,
        "description": "TEST DESCRIPTION"
    }

    response = requests.post(f"{host}/historical_transaction/", json=data)

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

@pytest.mark.run(order=18)      
def test_hist_trx():
    response = requests.get(f"{host}/historical_transaction/?account_number=1234567890")

    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict
    assert type(response.json()['data']) is list

# HISTORY TEST [ENDED]