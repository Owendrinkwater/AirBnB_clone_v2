#!/usr/bin/python3
"""User Module for HBNB project"""
from sqlalchemy import Column, String
from models.place import Place
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """User class for DBStorage"""
    __tablename__ = "users"

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    
    places = relationship("Place", backref="user", cascade="all, delete, delete-orphan")
    reviews = relationship("Review", backref="user", cascade="all, delete, delete-orphan")

