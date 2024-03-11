from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    balance = Column(Float, default=100)

class Model(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

class BillingHistory(Base):
    __tablename__ = 'billing_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    price = Column(Float)

class Prediction(Base):
    __tablename__ = 'predictions'

    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('billing_history.id'))
    result = Column(Integer)
    model_id = Column(Integer, ForeignKey('models.id'))
