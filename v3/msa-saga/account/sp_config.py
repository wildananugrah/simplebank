import os

# MONGODB_HOST="mongodb://45.113.235.79:5010"
# CUSTOMER_HOST="http://localhost:3000"

MONGODB_HOST=os.getenv("MONGODB_HOST")
CUSTOMER_HOST=os.getenv("CUSTOMER_HOST")