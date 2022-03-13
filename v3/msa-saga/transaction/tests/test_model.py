from exception.business_logic_exception import BusinessLogicException
from model.transaction import Transaction, TransferIntrabank, DebitTransaction
from dotenv import load_dotenv
import pytest, requests

load_dotenv()
cif_number = "1681274973"
host = "http://localhost:3010"

def create_account(cif_number):
    data = { 'cif_number' : cif_number }
    return requests.post(f"{host}/account/", json=data).json()['data']

pytest.ACCOUNT = None

# TRANSFER TEST [STARTED]

@pytest.mark.run(order=10)
def test_deposit():
    pytest.ACCOUNT = create_account(cif_number)
    transaction = Transaction()
    journal_number = transaction.deposit(pytest.ACCOUNT['account_number'], 1000)

    assert journal_number != None
    assert type(journal_number) == str

@pytest.mark.run(order=11)
def test_transfer_intrabank():
    account_2 = create_account(cif_number)
    transfer_intrabank = TransferIntrabank()
    transfer_intrabank.from_account_number = pytest.ACCOUNT['account_number']
    transfer_intrabank.to_account_number = account_2['account_number']
    transfer_intrabank.amount = 1
    transfer_intrabank.cif_number = cif_number
    transfer_intrabank.description = "TEST TRANSFER INTRABANK"

    journal_number = transfer_intrabank.transfer()

    assert journal_number != None
    assert type(journal_number) == str

    detail_transfer_intrabank = transfer_intrabank.detail_transaction("INTRABANK", pytest.ACCOUNT['account_number'], journal_number)

    assert detail_transfer_intrabank != None
    assert type(detail_transfer_intrabank) == dict
    assert detail_transfer_intrabank['journal_number'] == journal_number
    assert detail_transfer_intrabank['from_account_number'] == pytest.ACCOUNT['account_number']


@pytest.mark.run(order=13)
def test_debit():

    to_account_number = "3540447401"
    to_bank_code = "014"
    amount = 1
    description = "TEST INTERBANK TRANSFER"
    transaction_type = "INTERBANK"
    transaction = DebitTransaction(from_account_number=pytest.ACCOUNT['account_number'], 
                                            amount=amount, 
                                            cif_number=cif_number,
                                            transaction_type=transaction_type,
                                            description=description)
    journal_number = transaction.debit()

    assert journal_number != None
    assert type(journal_number) == str

    detail_transfer_interbank = transaction.detail_transaction(transaction_type, pytest.ACCOUNT['account_number'], journal_number)

    assert detail_transfer_interbank != None
    assert type(detail_transfer_interbank) == dict
    assert detail_transfer_interbank['journal_number'] == journal_number

    try:
        detail_transfer_interbank = transaction.detail_transaction("INTERBANK", pytest.ACCOUNT['account_number'], "12345")
    except:
        assert 1 == 1

    try:
        detail_transfer_interbank = transaction.detail_transaction("ERROR_KEY", pytest.ACCOUNT['account_number'], "12345")
    except:
        assert 1 == 1

@pytest.mark.run(order=14)
def test_list():
    transaction = Transaction()
    transaction_list = transaction.list(pytest.ACCOUNT['cif_number'])
    assert transaction_list != None
    assert type(transaction_list) == list

@pytest.mark.run(order=15)
def test_reversal():
    transaction = Transaction()
    journal_number = transaction.reversal(pytest.ACCOUNT['account_number'], 1000, "439283")
    assert journal_number != None
    assert type(journal_number) == str

# TRANSFER TEST [ENDED]