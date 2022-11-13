from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:admin@postgres/alem'

SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:admin@localhost/alem'



engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    print("Db start connectiion")
    try:
        yield db
    finally:
        print('Db session closed')
        db.close()