import pytest
from pydash import is_equal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import Base, User, Portfolio, AssetType, Transaction
from src.db.database import add_user, add_portfolio, add_transaction, add_historical_data
from datetime import datetime
import os


@pytest.fixture
def engine():
    """Engine Generator Function via  pytest fixture"""
    #Create test_engine
    db_url = os.getenv('DATABASE_URL')
    test_engine = create_engine(db_url)
    Base.metadata.create_all(test_engine)

    #yield test_engine to DB transaction
    yield test_engine

    Base.metadata.drop_all(test_engine)


@pytest.fixture
def db_session(engine):
    """Session generator via pytest fixture"""
    Session = sessionmaker(bind=engine) #check later
    session = Session()

    #yield session to the test
    yield session

    #Teardown and rollback transaction after test
    session.rollback()
    session.close()


def test_add_user(db_session):
    user = add_user('TEST_USER', "TEST_PASSWORD", db_session)
    assert user is not None
    assert user.username == 'TEST_USER'









