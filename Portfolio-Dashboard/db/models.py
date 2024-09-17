from sqlalchemy import Column, Integer, String, NUMERIC, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()
'''
Using SQLAlchemy's Object-Relational Mapping (ORM). From my understanding,
this mapping allows us to develop structure so we can later query from the 
database.
'''
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    #When back-populating, make sure back_populates matches with the variable from the
    #relationship you are back-populating
    portfolios = relationship('Portfolio', back_populates='user')

    # Allows me to create a printable version of the object, so I can debug if needed
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}>"

class Portfolio(Base):
    __tablename__ = 'portfolios'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False)

    user = relationship("User", back_populates="portfolios")
    transactions = relationship("Transaction", back_populates="portfolio")

    def __repr__(self):
        return (f"<Portfolio(id={self.id},user_id ={self.user_id},"
        f"name={self.name}, user={self.user})>")

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True) #primary key of transaction
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'))
    asset_type_id = Column(Integer, ForeignKey('asset_types.id'))
    asset_name = Column(String, nullable=False)
    amount = Column(NUMERIC(15,2), nullable=False)
    price = Column(NUMERIC(15,2), nullable=False)
    transaction_date = Column(DateTime, server_default=func.now(), nullable=False)

    asset_type = relationship("AssetType", back_populates="transactions")
    portfolio = relationship('Portfolio', back_populates='transactions')

    def __repr__(self):
        return (f"<Transaction(id={self.id}, portfolio_id={self.portfolio_id}, "
                f"asset_type_id={self.asset_type_id}, asset_name={self.asset_name}, "
                f"amount={self.amount}, price={self.price}), transaction_date={self.transaction_date}>")

class AssetType(Base):
    __tablename__ = 'asset_types'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    transactions = relationship('Transaction', back_populates='asset_type')

    def __repr__(self):
        return f"<AssetType(id={self.id}, name={self.name})>"


class HistoricalData(Base):
    __tablename__ = 'historical_data'
    id = Column(Integer, primary_key=True)
    asset_name = Column(String, nullable=False)
    price = Column(NUMERIC(15,2), nullable=False)
    date = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return(f"<HistoricalData(id={self.id}, asset_name={self.asset_name}, "
               f"price={self.price}, date={self.date})>")