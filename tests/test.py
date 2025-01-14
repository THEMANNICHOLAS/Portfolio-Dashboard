import pytest
import sys
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import user

from src.db.models import Base, User, Portfolio, AssetType
from src.db.database import add_user, add_portfolio, add_transaction, create_asset_type
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def engine():
    """Engine Generator Function via  pytest fixture"""
    #Create test_engine
    test_db_url = os.getenv('DB_URL')
    test_engine = create_engine(test_db_url)
    Base.metadata.create_all(test_engine)

    #yield test_engine to DB transaction
    yield test_engine

    Base.metadata.drop_all(test_engine)


@pytest.fixture
def db_session(engine):
    """Session generator via pytest fixture"""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection) #check later
    session = Session()

    #yield session to the test
    yield session

    #Teardown and rollback transaction after test
    transaction.rollback()
    session.rollback()
    session.close()


def test_add_user(db_session):
    """Test adding user to database using pytest fixture"""
    user = add_user('TEST_USER', "TEST_PASSWORD", db_session)
    assert user is not None
    assert user.username == 'TEST_USER'


def test_add_existing_user(db_session):
    """Test adding a user with a username that already exists"""
    add_user('TEST_USER', "TEST_PASSWORD", db_session)
    user = add_user('TEST_USER', "TEST_PASSWORD", db_session)
    assert user is None


def test_add_portfolio(db_session):
    """Test adding a portfolio to a user using pytest fixture"""
    user = add_user('TEST_USER', "TEST_PASSWORD", db_session)
    portfolio = add_portfolio("TEST_PORTFOLIO", user.id, db_session)
    print(portfolio.__repr__) #Print representation of class ensuring members are not Null
    assert portfolio is not None


def test_establish_asset_types(db_session):
    assets = ["Stock", "Bond", "ETF", "Mutual Fund", "Crypto"]
    for asset in assets:
        create_asset_type(asset, db_session)
        assert asset in assets is not None
    print(db_session.query(AssetType).all())









