from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()

engine = create_engine(os.getenv("DATABASE_URL"), echo=False)

def get_db():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()

def create_tables():
    with engine.begin():
        Base.metadata.create_all(bind=engine)
        print("Database conexion success")