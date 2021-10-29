from databases.account import AccountDB

class AccountModel():
    def __init__(self, db):
        self.db = db

    def create(self, account_dict):
        db_account = AccountDB(**account_dict)
        self.db.add(db_account)
        self.db.commit()
        self.db.refresh(db_account)
        return account_dict

    def detail(self, account):
        return self.db.query(AccountDB).filter(AccountDB.account == account).first()

    def all(self):
        return self.db.query(AccountDB).offset(skip).limit(limit).all()

    def delete(self, db_account):
        self.db.delete(db_account)
        self.db.commit()
        return True
    
    def all(self, skip: int = 0, limit: int = 100):
        return self.db.query(AccountDB).offset(skip).limit(limit).all()