```mermaid
sequenceDiagram
    Incoming Request->>+Payment: 
    Payment->>+Transaction: request to debit the account
    Transaction->>+Account: validate the account number
    Account->>+Customer: validate the cif number
    Customer->>+Account: cif number is valid
    Account->>+Transaction: account number is valid
    Transaction->>+Account: deduct the account balance
    Account->>+Transaction: settlement is success
    Transaction->>+Payment:  generating and providing a journal number
    Payment->>+Payment Service: notify the payment
    Payment Service->>+Payment: response OK
    Payment->>+Incoming Request: 
```