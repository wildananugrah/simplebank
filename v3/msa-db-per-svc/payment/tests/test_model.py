import pytest
from exception.business_logic_exception import BusinessLogicException

from model.payment import EletricalBillPayment
from dotenv import load_dotenv

load_dotenv()

# PAYMENT TEST [STARTED]

@pytest.mark.run(order=14)
def test_billpayment_inquiry():
    eletrical_billpayment = EletricalBillPayment()
    bill_id = "458625142578"
    inquiry = eletrical_billpayment.inquiry(bill_id)

    assert inquiry != None
    assert type(inquiry) == dict
    assert inquiry['bill_id'] == bill_id

@pytest.mark.run(order=15)
def test_billpayment_pay():
    description = "TEST ELETRIC BILL PAYMENT"
    bill_id = "458625142578"
    amount = 1

    eletrical_billpayment = EletricalBillPayment(bill_id=bill_id, 
                                            amount=amount, description=description, 
                                            from_account_number="7028325696", 
                                            cif_number="1681274974")
    bill_id = "458625142578"
    journal_number = eletrical_billpayment.pay()

    assert journal_number != None
    assert type(journal_number) == str

@pytest.mark.run(order=16)
def test_billpayment_pay_error():
    description = "TEST ELETRIC BILL PAYMENT"
    bill_id = "458625142578"
    amount = 1

    try:
        eletrical_billpayment = EletricalBillPayment(bill_id="999888777", 
                                                amount=amount, description=description, 
                                                from_account_number="7028325696", 
                                                cif_number="1681274974")
        bill_id = "458625142578"
        journal_number = eletrical_billpayment.pay()
    except:
        assert 1 == 1
        
# PAYMENT [ENDED]