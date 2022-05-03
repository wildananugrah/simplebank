from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sp_config import DATABASE_CONN_STR

engine = create_engine(DATABASE_CONN_STR)
Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()