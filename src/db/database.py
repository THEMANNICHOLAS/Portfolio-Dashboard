from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from models import User, Portfolio, Transaction, AssetType, HistoricalData
from ..utility.security import hash_password
import os
import logging


logging.basicConfig(level=logging.INFO)

#Creating and starting the database engine and session. Schema already made
#using SQL commands in PostgreSQL
DATABASE_URL = os.getenv('DB_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def handle_session_commit(session):
    """Helper function for handling commits and errors. Returns
    true if no issues found"""
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        logging.error(f"Integrity error: {e.orig}")
        logging.info(e.statement)
    except Exception as e:
        session.rollback()
        logging.error(f"Unexpected error: {e}")
        return None
    return True

def add_user(username, password, session):
    #verify user exists before adding to database
    existing_user = session.query(User).filter_by(username = username).first()
    if existing_user:
        logging.info("User already exists")
        return None

    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password)
    session.add(new_user)

    if handle_session_commit(session):
        return new_user
    return None

def add_portfolio(portfolio_name, user_id, session):
    #verify is portfolio exists before adding to database
    existing_portfolio = session.query(Portfolio).filter_by(name = portfolio_name, user_id = user_id).first()
    if existing_portfolio:
        logging.info("Portfolio already exists")
        return None


    portfolio = Portfolio(name=portfolio_name, user_id=user_id)
    session.add(portfolio)

    if handle_session_commit(session):
        return portfolio
    return None

def add_transaction(portfolio_id:int, asset_type_id:int,
                    amount:float , price:float, transaction_date:datetime, session):
    #verify that portfolio and asset_type exists
    existing_portfolio = session.query(Portfolio).filter_by(id = portfolio_id).first()
    existing_asset_type = session.query(AssetType).filter_by(id = asset_type_id).first()
    #both must exists before adding to database
    if not existing_portfolio:
        logging.info(f"Portfolio ID {portfolio_id} does not exist")
        return None
    if not existing_asset_type:
        logging.info(f"Asset type ID {asset_type_id} does not exist")
        return None

    transaction = Transaction(
        portfolio_id=portfolio_id, asset_type_id=asset_type_id,
        amount=amount, price=price, transaction_date=transaction_date)
    session.add(transaction)

    if handle_session_commit(session):
        return transaction
    return None

def add_historical_data(asset_name:str, price:float, date:datetime, session):
    historical_data = HistoricalData(asset_name=asset_name, price=price, date=date)
    session.add(historical_data)

    if handle_session_commit(session):
        return historical_data
    return None

def create_asset_type(name:str, session):
    existing_asset_type = session.query(AssetType).filter_by(name=name).first()
    if existing_asset_type:
        logging.info("Asset type already exists")
        return existing_asset_type

    asset_type = AssetType(name=name)
    session.add(asset_type)

    if handle_session_commit(session):
        return asset_type
    return None

