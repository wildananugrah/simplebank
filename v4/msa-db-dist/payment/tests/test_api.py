import pytest
import requests

host = "http://localhost:3050"
bill_id = "458625142578"

from_account_number = "1483400512"
cif_number = "1681274973"

# PAYMENT [STARTED]
@pytest.mark.run(order=15)
def test_transaction_eletric_payment_inquiry():
    response = requests.get(f"{host}/transaction/payment/eletrical/?bill_id={bill_id}")
    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

@pytest.mark.run(order=16)
def test_transaction_eletric_payment_pay():
    data = {
        "bill_id":bill_id,
        "amount": 1,
        "description": "TEST PAYMENT ELETRICAL PAYMENT",
        "from_account_number": from_account_number,
        "cif_number": cif_number
    }
    response = requests.post(f"{host}/transaction/payment/eletrical/", json=data)
    assert response is not None
    assert response.status_code in (200, 201)
    assert type(response.json()) is dict

# PAYMENT [ENDED]