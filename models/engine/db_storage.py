#!/usr/bin/python3
"""DB Storage module for AirBnB clone"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    '''A class to mange the db storage'''

    __engine = None
    __session = None

    def __init__(self):
        '''A method to create an instance'''

        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        db = os.getenv('HBNB_MYSQL_DB')
        host = os.getenv('HBNB_MYSQL_HOST')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, pwd, host, db),
                                      pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        ''' handles queries according to clasname '''

        classes = {
            'State': State,
            'City': City,
            'User': User,
            'Place': Place,
            'Review': Review,
            'Amenity': Amenity
        }
        res = {}
        if cls and cls in classes:
            if isinstance(cls, str):
                cls = classes.get(cls)
            objs = self.__session.query(cls).all()
            for obj in objs:
                k = f"{cls.__name__}.{obj.id}"
                res[k] = obj
        else:
            for cls in classes.values():
                objs = self.__session.query(cls).all()
                for obj in objs:
                    k = f"{cls.__name__}.{obj.id}"
                    res[k] = obj
        return res

    def new(self, obj):
        '''add the object to the current database session'''
        try:
            self.__session.add(obj)
        except Exception as e:
            self.__session.rollback()
            raise

    def save(self):
        '''commit all changes of the current database session'''
        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise

    def delete(self, obj=None):
        '''delete from the current database session obj if not None'''
        try:
            self.__session.delete(obj)
        except Exception as e:
            self.__session.rollback()
            raise

    def reload(self):
        ''' create all tables in the database '''

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
