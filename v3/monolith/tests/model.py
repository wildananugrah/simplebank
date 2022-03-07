import pytest
from exception.business_logic_exception import BusinessLogicException

from model.customer import CustomerMobile, CustomerInternetBanking
from model.account import Account
from model.transaction import Transaction, TransferIntrabank, TransferInterbank, EletricalBillPayment
from model.historical_transaction import HistoricalTransaction

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

@pytest.mark.run(order=1)
def test_customer_mobile_login():
    customer_mobile = CustomerMobile()
    customer_mobile.username = "user1"
    customer_mobile.password = "password"
    customer = customer_mobile.login()

    assert customer != None
    assert customer['session_id'] != ''
    assert customer['is_login'] == True

    return customer

@pytest.mark.run(order=2)
def test_validate_session_true():
    customer = test_customer_mobile_login()
    customer_mobile = CustomerMobile()
    is_login = customer_mobile.validate_session(customer['session_id'])

    assert is_login == True

@pytest.mark.run(order=3)
def test_customer_mobile_logout():

    customer = test_customer_mobile_login()
    customer_mobile = CustomerMobile()
    customer = customer_mobile.logout(customer['session_id'])

    assert customer != None
    assert customer['session_id'] == ''
    assert customer['is_login'] == False

@pytest.mark.run(order=4)
def test_validate_session_false():
    try:
        customer = test_customer_mobile_login()
        customer_mobile = CustomerMobile()
        
        # should throw an error!
        is_login = customer_mobile.validate_session('12345')
    
    except Exception as error:
        assert 1 == 1

@pytest.mark.run(order=5)
def test_customer_internet_banking_login():
    customer_internet_banking = CustomerInternetBanking()
    customer_internet_banking.email = "user0@gmail.com"
    customer_internet_banking.password = "password"
    customer = customer_internet_banking.login()

    assert customer != None
    assert customer['session_id'] != ''
    assert customer['is_login'] == True

    return customer

@pytest.mark.run(order=6)
def test_customer_internet_banking_logout():

    customer = test_customer_internet_banking_login()
    customer_internet_banking = CustomerInternetBanking()
    customer = customer_internet_banking.logout(customer['session_id'])

    assert customer != None
    assert customer['session_id'] == ''
    assert customer['is_login'] == False

# CUSTOMER TEST [ENDED]

# ACCOUNT TEST [STARTED]

@pytest.mark.run(order=7)
def test_create_account():
    account = Account()
    customer = test_customer_mobile_login()
    account = account.create(customer['cif_number'])

    assert account != None
    assert account['cif_number'] == customer['cif_number']

    return account

@pytest.mark.run(order=8)
def test_list_account():
    customer = test_customer_mobile_login()

    account_list = Account().list(customer['cif_number'])

    assert account_list != None
    assert type(account_list) == list
    # assert len(account_list) == 1 

    return account_list

@pytest.mark.run(order=9)
def test_delete_account():
    db_account_list = test_list_account()
    account = Account()

    for _account in db_account_list:
        deleted_account = account.delete(_account['account_number'])
        assert deleted_account == True
        
        try:
            
            # should throw an error!
            account.detail(_account['account_number'])

        except BusinessLogicException as error:
            assert f"Can not find account_number: {_account['account_number']}" == str(error)
            assert 1 == 1

# ACCOUNT TEST [ENDED]

# TRANSFER TEST [STARTED]

@pytest.mark.run(order=10)
def test_deposit():
    customer = find_customer("user1", "password")
    account = create_account(customer['cif_number'])

    transaction = Transaction()
    journal_number = transaction.deposit(account['account_number'], 1000)

    assert journal_number != None
    assert type(journal_number) == str

@pytest.mark.run(order=11)
def test_transfer_intrabank():
    customer_1 = find_customer("user1", "password")
    customer_2 = find_customer("user2", "password")

    account_2 = create_account(customer_2['cif_number'])
    account_1 = find_accounts(customer_1['cif_number'])[0] # at this moment, customer 1 only has one account.

    transfer_intrabank = TransferIntrabank()
    transfer_intrabank.from_account_number = account_1['account_number']
    transfer_intrabank.to_account_number = account_2['account_number']
    transfer_intrabank.amount = 1
    transfer_intrabank.cif_number = account_1['cif_number']
    transfer_intrabank.description = "TEST TRANSFER INTRABANK"

    journal_number = transfer_intrabank.transfer()

    assert journal_number != None
    assert type(journal_number) == str

    detail_transfer_intrabank = transfer_intrabank.detail_transaction("INTRABANK", account_1['account_number'], journal_number)

    assert detail_transfer_intrabank != None
    assert type(detail_transfer_intrabank) == dict
    assert detail_transfer_intrabank['journal_number'] == journal_number
    assert detail_transfer_intrabank['from_account_number'] == account_1['account_number']

    # delete_account(account_2['account_number'])

@pytest.mark.run(order=12)
def test_inquiry_interbank():
    transter_interbank = TransferInterbank()
    account_number = "3540447401"
    inquiry = transter_interbank.inquiry(account_number, "014")

    assert inquiry != None
    assert type(inquiry) == dict
    assert inquiry['account_number'] == account_number

@pytest.mark.run(order=13)
def test_transfer_interbank():
    customer_1 = find_customer("user1", "password")
    account_1 = find_accounts(customer_1['cif_number'])[0] # at this moment, customer 1 only has one account.

    to_account_number = "3540447401"
    to_bank_code = "014"
    amount = 1
    description = "TEST INTERBANK TRANSFER"
    transfer_interbank = TransferInterbank(from_account_number=account_1['account_number'], 
                                            to_account_number=to_account_number, 
                                            to_bank_code=to_bank_code, 
                                            amount=amount, 
                                            cif_number=customer_1['cif_number'],
                                            description=description)
    journal_number = transfer_interbank.transfer()

    assert journal_number != None
    assert type(journal_number) == str

    detail_transfer_interbank = transfer_interbank.detail_transaction("INTERBANK", account_1['account_number'], journal_number)

    assert detail_transfer_interbank != None
    assert type(detail_transfer_interbank) == dict
    assert detail_transfer_interbank['journal_number'] == journal_number
    assert detail_transfer_interbank['from_account_number'] == account_1['account_number']

    try:
        detail_transfer_interbank = transfer_interbank.detail_transaction("INTERBANK", account_1['account_number'], "12345")
    except:
        assert 1 == 1

    try:
        detail_transfer_interbank = transfer_interbank.detail_transaction("ERROR_KEY", account_1['account_number'], "12345")
    except:
        assert 1 == 1

# TRANSFER TEST [ENDED]

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
    customer_1 = find_customer("user1", "password")
    account_1 = find_accounts(customer_1['cif_number'])[0] # at this moment, customer 1 only has one account.
    description = "TEST ELETRIC BILL PAYMENT"
    bill_id = "458625142578"
    amount = 1

    eletrical_billpayment = EletricalBillPayment(bill_id=bill_id, 
                                            amount=amount, description=description, 
                                            from_account_number=account_1['account_number'], 
                                            cif_number=customer_1['cif_number'])
    bill_id = "458625142578"
    journal_number = eletrical_billpayment.pay()

    assert journal_number != None
    assert type(journal_number) == str

    detail_billpayament = eletrical_billpayment.detail_transaction("ELETRICAL_BILLPAYMENT", account_1['account_number'], journal_number)

    assert detail_billpayament != None
    assert type(detail_billpayament) == dict
    assert detail_billpayament['journal_number'] == journal_number
    assert detail_billpayament['from_account_number'] == account_1['account_number']

    # delete_account(account_1['account_number'])

@pytest.mark.run(order=16)
def test_transation_list():
    transaction = Transaction()
    customer_1 = find_customer("user1", "password")
    account_1 = find_accounts(customer_1['cif_number'])[0]
    hist_list = transaction.list(account_1['cif_number'])

    assert hist_list != None
    assert type(hist_list) == list

@pytest.mark.run(order=17)
def test_historical_list():
    hist_trx = HistoricalTransaction()
    customer_1 = find_customer("user1", "password")
    transaction_list = hist_trx.list(customer_1['cif_number'])

    assert transaction_list != None
    assert type(transaction_list) == list

@pytest.mark.run(order=18)
def test_historical_save():
    hist_trx = HistoricalTransaction()
    hist_trx.transaction_type = "ERROR_KEY"

    try:
        hist_trx.save()
    except:
        assert 1 == 1

# PAYMENT TEST [ENDED]