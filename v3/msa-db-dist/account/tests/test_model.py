import pytest
from exception.business_logic_exception import BusinessLogicException
from model.account import Account
from dotenv import load_dotenv
import requests

load_dotenv()

host = "http://localhost:3000"

username = "user1"
password = "password"

# HELPERS [STARTED]
def find_customer(usename, password):

    data = {
        "username": username,
        "password" : password
    }

    return requests.post(f"{host}/customer/mobile/login/", json=data).json()['data']

# HELPERS [ENDED]

# ACCOUNT TEST [STARTED]

@pytest.mark.run(order=7)
def test_create_account():
    account = Account()
    customer = find_customer(username, password)
    account = account.create(customer['cif_number'])

    assert account != None
    assert account['cif_number'] == customer['cif_number']

    return account

@pytest.mark.run(order=8)
def test_list_account():
    customer = find_customer(username, password)

    account_list = Account().list(customer['cif_number'])

    assert account_list != None
    assert type(account_list) == list

    return account_list

@pytest.mark.run(order=9)
def test_update_account():
    db_account_list = test_list_account()
    account = Account()

    for _account in db_account_list:
        updated_account = account.update(_account['account_number'], 100)
        assert updated_account != None
        assert type(updated_account) == dict

@pytest.mark.run(order=10)
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