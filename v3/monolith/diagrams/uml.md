```mermaid
classDiagram

    Customer <|-- CustomerMobile
    Customer <|-- CustomerInternetBanking
    Customer o-- Account
    Transaction <|-- TransferIntrabank
    Transaction <|-- TransferInterbank
    Transaction <|-- EletricalBillPayment
    Account o-- Transaction
    HistoricalTransaction o-- Transaction 

    class Customer{
        - id_number: str
        - name: str
        - cif_number: str
        - is_loggin: bool
        - session_id: str

        - detail(key_type, value): dict
        # create_session_id(cif_number): dict
        # update_session_id(cif_number, session_id, is_login): dict
        - extract_cif_number(session_id): string
        - validate_session(session_id): bool
        + logout(session_id): dict
        
    }

    class CustomerMobile{
        + username: str
        + password: str
        + login(): dict
    }

    class CustomerInternetBanking{
        + email: str
        + password: str
        + login(): dict
    }

    class Account{
        - account_number: str
        - currency: str
        - balance: int
        - generate_account_number(size): str
        + detail(account_number): dict
        + create(cif_number, currency = 'IDR', balance = 0): dict
        + update(account_number, current_balance): dict
        + delete(account_number): bool
        + list(cif_number): list
    }

    class Transaction{
        journal_number: str
        - generate_journal_number(size): str
        - detail(account_number, journal_number): dict
        # save(save_params): bool
        # store_to_historical_transaction(historical_transaction_params): bool
        + list(cif_number): list
        + deposit(account_number, amount): str
        + detail_transaction(transaction_type, account_number, journal_number): dict
    }

    class TransferIntrabank{
        + from_account_number: str
        + to_account_number: str
        + cif_number: str
        + description: str
        + amount: int
        + transfer()
    }

    class TransferInterbank{
        + from_account_number: str
        + to_account_number: str
        + cif_number: str
        + description: str
        + amount: int
        + inquiry(to_account_number, to_bank_code): dict
        + transfer(): str
    }

    class ElectricalBillPayment{
        + bill_id: str
        + amount: int
        + description: str
        + from_account_number: str
        + cif_number: str

        + inquiry(bill_id): dict
        + pay(self): str
    }

    class HistoricalTransaction{
        + transaction_type: str
        + account_number: str
        + amount: str
        + journal_number: str
        + current_balance: int
        + description: str

        + save(): bool
        + list(account_number): list
    }
```   