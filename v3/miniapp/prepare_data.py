from pymongo import MongoClient
import json, random, string

client = MongoClient("mongodb://mongoadmin:secret@localhost:5000/")
db = client.simplebank_db

NUMBER_OF_CUSTOMERS = 100

def find_cif_number(cif_number):
    return db.customers.find_one({ 'cif_number' : cif_number }, {'_id' : False})

def find_id_number(id_number):
    return db.customers.find_one({ 'id_number' : id_number }, {'_id' : False})

def find_account_number(account_number):
    return db.accounts.find_one({ 'account_number' : account_number }, {'_id' : False})

def generate_cif_number(cif_number="", size=10):
        cif_number = ''.join(random.choice(string.digits) for _ in range(size))
        db_cif_number = find_cif_number(cif_number)
        if db_cif_number:
            self.generate_cif_number(cif_number)
        return cif_number

def generate_id_number(id_number="", size=16):
        id_number = ''.join(random.choice(string.digits) for _ in range(size))
        db_id_number = find_id_number(id_number)
        if db_id_number:
            self.generate_id_number(id_number)
        return id_number

def generate_account_number(account_number="", size=10):
        account_number = ''.join(random.choice(string.digits) for _ in range(size))
        db_account_number = find_account_number(account_number)
        if db_account_number:
            self.generate_account_number(account_number)
        return account_number

f = open("customers.json", "a")

cif_numbers = []
for x in range(NUMBER_OF_CUSTOMERS):

    id_number = generate_id_number()
    cif_number = generate_cif_number()

    data = {
        "username": f"user{x + 1}",
        "cif_number": cif_number,
        "email": f"user{x}@gmail.com",
        "id_number": id_number,
        "name": f"User {x}",
        "password": "password",
        "is_login": False,
        "session_id": ""
    }   

    cif_numbers.append(cif_number)

    f.write(f"{json.dumps(data)}\n")
f.close()

f = open("accounts.json", "a")

account_numbers = []
for cif_number in cif_numbers:
    
    account_number = generate_account_number()

    data = {
        "account_number": account_number,
        "cif_number": cif_number,
        "currency": "IDR",
        "balance": 1000
    }

    account_numbers.append(data)
    f.write(f"{json.dumps(data)}\n")

f.close()