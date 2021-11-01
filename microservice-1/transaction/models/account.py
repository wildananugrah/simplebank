from fastapi import HTTPException
import requests, os

class AccountModel():

    def detail(self, account):
        account_host = os.environ.get("ACCOUNT_HOST")
        account = requests.get(f"{account_host}/account?account={account}")

        if account.status_code == 200:
            return account.json()
        else:
            raise HTTPException(status_code=500, detail="ACCOUNT HOST ERROR") 