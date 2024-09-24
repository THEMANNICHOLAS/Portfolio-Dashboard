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

#Will be imported as session in other .py files
session = Session()

def add_user(username, password):
    #verify user exists before adding to database
    existing_user = session.query(User).filter_by(username = username).first()
    if existing_user:
        logging.info("User already exists")
        return None
    try:
        hashed_password = hash_password(password)
        new_user = User(username=username, password=hashed_password)
        session.add(new_user)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        logging.info(e.orig)
        logging.info(e.statement)
    except Exception as e:
        session.rollback()
        logging.info(f"Error adding user: {e}")
    else:
        return new_user

def add_portfolio(portfolio_name, user_id):
    #verify is portfolio exists before adding to database
    existing_portfolio = session.query(Portfolio).filter_by(name = portfolio_name, user_id = user_id).first()
    if existing_portfolio:
        logging.info("Portfolio already exists")
        return None
    try:
        portfolio = Portfolio(name=portfolio_name, user_id=user_id)
        session.add(portfolio)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        logging.info(e.orig)
        logging.info(e.statement)
    except Exception as e:
        session.rollback()
        logging.info(f"Error adding portfolio: {e}")
    else:
        return portfolio

def add_transaction(portfolio_id:int, asset_type_id:int,
                    amount:float , price:float, transaction_date:datetime):
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

    try:
        transaction = Transaction(portfolio_id=portfolio_id, asset_type_id=asset_type_id,
                              amount=amount, price=price, transaction_date=transaction_date)
        session.add(transaction)
        session.commit()
    except IntegrityError as e:
        logging.info(e.orig)
        logging.info(e.statement)
        session.rollback()
    except Exception as e:
        session.rollback()
        logging.info(f"Error adding historical data: {e}")
    else:
        return transaction


def add_historical_data(asset_name:str, price:float, date:datetime):
    try:
        historical_data = HistoricalData(asset_name=asset_name, price=price, date=date)
        session.add(historical_data)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        logging.info(e.orig)
        logging.info(e.statement)
    except Exception as e:
        session.rollback()
        logging.info(f"Error adding transaction: {e}")
    else:
        return historical_data

def create_asset_type(name:str):
    existing_asset_type = session.query(AssetType).filter_by(name=name).first()
    if existing_asset_type is None:
        try:
            #Try creating the asset type
            asset_type = AssetType(name=name)
            session.add(asset_type)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            logging.info(e.orig)
            logging.info(e.statement)
        except Exception as e:
            logging.info(f"An unexpected error occurred: {e}")
        else:
            return asset_type
    else:
        logging.info("Asset Type Already Exists")
        return existing_asset_type




