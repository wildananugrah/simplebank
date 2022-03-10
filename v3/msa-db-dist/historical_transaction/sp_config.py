import os

# MONGODB_READ_HOST="mongodb://45.113.235.79:6030/?readPreference=secondary&directConnection=true"
# MONGODB_WRITE_HOST="mongodb://45.113.235.79:6000/?readPreference=primary&directConnection=true"

MONGODB_READ_HOST=os.getenv("MONGODB_READ_HOST")
MONGODB_WRITE_HOST=os.getenv("MONGODB_WRITE_HOST")