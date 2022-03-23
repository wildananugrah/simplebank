```mermaid
erDiagram
    CUSTOMER ||--|{ ACCOUNT : has
    ACCOUNT ||--|{ TRANSACTION : has
    ACCOUNT ||--|{ HISTORICAL_TRANSACTION : has
    TRANSACTION ||--|| PAYMENT : has
    TRANSACTION ||--|| INTERBANK_TRANSFER : has
    
```