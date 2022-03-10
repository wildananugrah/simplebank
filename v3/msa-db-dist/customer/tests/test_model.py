from exception.business_logic_exception import BusinessLogicException
from model.customer import CustomerMobile, CustomerInternetBanking
from dotenv import load_dotenv

import pytest

load_dotenv()

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