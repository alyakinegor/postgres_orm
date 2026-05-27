import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')
if DATABASE_URI is None:
    raise ValueError('database_uri is empty!')

engine = create_engine(
    DATABASE_URI,
    echo=True
)

sesion_local = sessionmaker(
    bind=engine,
    autoflush=False
)

class Base(DeclarativeBase):
    pass

