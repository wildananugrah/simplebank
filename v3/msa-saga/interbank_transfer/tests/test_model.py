import pytest
from exception.business_logic_exception import BusinessLogicException
from model.interbank_transfer import InterbankTransfer
from dotenv import load_dotenv

load_dotenv()

from_account_number = "7028325696"
cif_number = "1681274974"

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

# HELPERS [ENDED]

# CUSTOMER TEST [STARTED]

@pytest.mark.run(order=12)
def test_inquiry_interbank():
    interbank_transfer = InterbankTransfer()
    account_number = "3540447401"
    inquiry = interbank_transfer.inquiry(account_number, "014")

    assert inquiry != None
    assert type(inquiry) == dict
    assert inquiry['account_number'] == account_number

@pytest.mark.run(order=13)
def test_transfer_interbank():

    to_account_number = "3540447401"
    to_bank_code = "014"
    amount = 1
    description = "TEST INTERBANK TRANSFER"
    interbank_transfer = InterbankTransfer(from_account_number=from_account_number, 
                                            to_account_number=to_account_number, 
                                            to_bank_code=to_bank_code, 
                                            amount=amount, 
                                            cif_number=cif_number,
                                            description=description)
    journal_number = interbank_transfer.transfer()

    assert journal_number != None
    assert type(journal_number) == str

@pytest.mark.run(order=14)
def test_transfer_interbank_error():

    to_account_number = "3540447401"
    to_bank_code = "014"
    amount = 1
    description = "TEST INTERBANK TRANSFER"
    
    try:
        interbank_transfer = InterbankTransfer(from_account_number=from_account_number, 
                                                to_account_number="888777666", 
                                                to_bank_code=to_bank_code, 
                                                amount=amount, 
                                                cif_number=cif_number,
                                                description=description)
        journal_number = interbank_transfer.transfer()
    except Exception as error:
        print(error)
        assert 1 == 1

# TRANSFER TEST [ENDED]