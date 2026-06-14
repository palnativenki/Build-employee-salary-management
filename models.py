# Database informations.
from sqlalchemy import Column, String, Float, DateTime, func
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(String, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String, unique=True)
    department = Column(String)
    country = Column(String)
    salary = Column(Float)
    currency = Column(String)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
