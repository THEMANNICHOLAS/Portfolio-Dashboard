from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os
from dotenv import load_dotenv

DATABASE_URL = os.getenv('DB_URL')

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

#Will be imported as session in other .py files
session = Session()

Base.metadata.create_all(engine)