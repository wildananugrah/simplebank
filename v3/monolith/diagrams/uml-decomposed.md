classDiagram
  
    Customer <|-- CustomerMobile
    Customer <|-- CustomerInternetBanking
    Payment <|-- ElectricalBillPayment

    class Customer{

        - detail(key_type, value): dict
        # create_session_id(cif_number): dict
        # update_session_id(cif_number, session_id, is_login): dict
        - extract_cif_number(session_id): string
        - validate_session(session_id): bool
        + logout(session_id): dict
        
    }

    class CustomerMobile{
        + login(): dict
    }

    class CustomerInternetBanking{
        + login(): dict
    }

    class Account{
        + detail(account_number): dict
        + create(cif_number, currency = 'IDR', balance = 0): dict
        + update(account_number, current_balance): dict
        + delete(account_number): bool
        + list(cif_number): list
    }

    class Transaction{
        - generate_journal_number(size): str
        - detail(account_number, journal_number): dict
        # save(save_params): bool
        # store_to_historical_transaction(historical_transaction_params): bool
        + list(cif_number): list
        + deposit(account_number, amount): str
        + detail_transaction(transaction_type, account_number, journal_number): dict
        + transfer()    
    }

    class TransferInterbank{
        + save()
        + detail()
        + list()
        + inquiry(to_account_number, to_bank_code): dict
        + transfer(): str
    }

    class Payment{
      + save()
      + list()
      + detail()
    }

    class ElectricalBillPayment{
        + inquiry(bill_id): dict
        + pay(self): str
    }

    class HistoricalTransaction{
        + save(): bool
        + list(account_number): list
    }