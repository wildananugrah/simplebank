import requests

host = "http://localhost:8000"

response = requests.post(f"{host}/customer", json={
  "name": "User Name",
  "id_number": "31730059100009",
  "email": "user@gmail.com"
})
print(response)
print(response.json())

cif_number = response.json()["cif_number"]

response = requests.put(f"{host}/customer_user", json={
    "username": "username",
    "password": "password",
    "cif_number": cif_number
})
print(response)
print(response.json())

response = requests.post(f"{host}/account", json={
    "cif_number": cif_number,
    "currency": "IDR",
    "balance": 0
})
print(response)
print(response.json())
account_number_1 = response.json()['account']

response = requests.post(f"{host}/account", json={
    "cif_number": cif_number,
    "currency": "IDR",
    "balance": 0
})
print(response)
print(response.json())
account_number_2 = response.json()['account']

# account_number_1 = "0452025509"
# account_number_2 = "2966931377"

response = requests.post(f"{host}/deposit", json={
  "account_number": account_number_1,
  "amount": 1000
})
print(response)
print(response.json())

response = requests.post(f"{host}/transfer", json={
    "to_account_number": account_number_2,
    "from_account_number": account_number_1,
    "amount": 100
})
print(response)
print(response.json())

response = requests.post(f"{host}/bill/payment/tax", json={
    "bill_id" : "001",
    "account_number": account_number_1,
    "amount": 10
})
print(response)
print(response.json())

print("DONE!")