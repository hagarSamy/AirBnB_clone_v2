#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import os
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship, backref
import models
from models. city import City


class State(BaseModel, Base):
    """ State class """
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref=backref('state'))

    else:
        name = ""

        @property
        def cities(self):
            """getter for cities relationship for FileStorage"""
            cities = [city for city in models.storage.all(
                City).values() if city.state_id == self.id]
            return cities
