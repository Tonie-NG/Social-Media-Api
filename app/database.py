from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
    


# connecting to database. Old method, checkout database.py
# while True:
#     try: 
#         # conn = psycopg2.connect(host='localhost', database= 'socialmedia', user ='postgres', password='tonie0810', cursor_factory= RealDictCursor)
#         cursor = connect.cursor()
#         print("Database connection established")
#         break
#     except Exception as error:
#         print("Error connecting to database")
#         print("Error", error)
#         time.sleep(5)
 