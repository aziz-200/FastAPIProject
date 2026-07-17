from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine("postgresql://aziz:0201@localhost:5432/delivery_db",
                       echo=True)

class Base(DeclarativeBase):
    pass
session = sessionmaker(bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
