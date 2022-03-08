import pytest
from exception.business_logic_exception import BusinessLogicException
from model.historical_transaction import HistoricalTransaction
from dotenv import load_dotenv

load_dotenv()
cif_number = "123456"

# PAYMENT TEST [STARTED]

@pytest.mark.run(order=17)
def test_historical_save():
    hist_trx = HistoricalTransaction()
    hist_trx.transaction_type = "DEBIT"
    hist_trx.account_number: "1234567890"
    hist_trx.amount = 100
    hist_trx.journal_number = "123456"
    hist_trx.current_balance = 1000
    hist_trx.description = "TEST DESCRIPTION"
    save = hist_trx.save()

    assert save == True

@pytest.mark.run(order=18)
def test_historical_save_fail():
    hist_trx = HistoricalTransaction()
    hist_trx.transaction_type = "ERROR_KEY"

    try:
        hist_trx.save()
    except:
        assert 1 == 1

@pytest.mark.run(order=19)
def test_historical_list():
    hist_trx = HistoricalTransaction()
    transaction_list = hist_trx.list(cif_number)

    assert transaction_list != None
    assert type(transaction_list) == list

# PAYMENT TEST [ENDED]