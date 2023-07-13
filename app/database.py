from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .setting import Database_Name, Database_Password, Database_Username, IP_Address


#All other options for the database
#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db" #SQL LITE
#SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{Database_Username}:{Database_Password}@{IP_Address}/{Database_Name}" #MYSQL
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{Database_Username}:{Database_Password}@{IP_Address}/{Database_Name}" #PostgreSQL

print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)# for all other database,  this is all what we need.
'''
This is what we need for sqlLite DB.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
'''

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()