import pytest
import requests

host = "http://localhost:3040"
from_account_number = "1483400512"
cif_number = "1681274973"
# INTERBANK TEST [STARTED]

@pytest.mark.run(order=13)
def test_transaction_interbank_inquiry():
    response = requests.get(f"{host}/transaction/transfer/interbank/?to_account_number=3540447401&to_bank_code=014")
    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

@pytest.mark.run(order=14)
def test_transaction_interbank_transfer():
    data = {
        "from_account_number": from_account_number,
        "to_account_number": "3540447401",
        "to_bank_code": "014",
        "cif_number": cif_number,
        "amount": 1,
        "description": "TEST INTERBANK"
    }

    response = requests.post(f"{host}/transaction/transfer/interbank/", json=data)
    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

# INTERBANK TEST [ENDED]