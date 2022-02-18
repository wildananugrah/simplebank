import pytest, os, requests
from dotenv import load_dotenv

load_dotenv()

host = "http://localhost:3000"

id_number_success = '3175023005910005'
id_number_fail = '3175023005910001'

def test_inquiry_customer_by_id_number_success():
    response = requests.get(f"{host}/customer/?id_type=id_number&value={id_number_success}")
    assert 201 == response.status_code

def test_inquiry_customer_by_id_number_fail():
    response = requests.get(f"{host}/customer/?id_type=id_number&value={id_number_fail}")
    assert 400 == response.status_code