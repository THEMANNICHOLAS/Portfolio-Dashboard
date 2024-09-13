from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
'''
Using SQLAlchemy's Object-Relational Mapping (ORM). From my understanding,
this mapping allows us to develop structure so we can later query from the 
database
'''
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True) #primary key of transaction
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'))
    asset_type_id = Column(Integer, ForeignKey('asset_types.id'))
    asset_name = Column(String)
    amount = Column(Float)
    price = Column(Float)
    transaction_date = Column(Date)

    asset_type = relationship("AssetType", back_populates="transactions")
    portfolio = relationship('Portfolio', back_populates='transactions')
    #Allows me to create a printable version of the object, so I can debug if needed
    def __repr__(self):
        return (f"<Transaction(id={self.id}, portfolio_id={self.portfolio_id}, "
                f"asset_type_id={self.asset_type_id}, asset_name={self.asset_name}, "
                f"amount={self.amount}, price={self.price}), transaction_date={self.transaction_date}>")
class AssetType(Base):
    __tablename__ = 'asset_types'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    transactions = relationship('Transaction', back_populates='asset_type')

    def __repr__(self):
        return (f"<AssetType(id={self.id}, name={self.name})>")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

    portfolio = relationship('Portfolio', back_populates='users')

    def __repr__(self):
        return (f"<User(id={self.id}, username={self.username}>")

class Portfolio(Base):
    __tablename__ = 'portfolios'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)

    user = relationship("User", back_populates="portfolios.id")
    transactions = relationship("Transaction", back_populates="portfolio")

    def __repr__(self):
        return (f"<Portfolio(id={self.id},user_id ={self.user_id},"
                f"name={self.name}, ")
