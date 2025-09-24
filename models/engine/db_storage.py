#!/usr/bin/python3
"""DBStorage engine"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
import os

class DBStorage:
    """Database storage engine"""
    
    __engine = None
    __session = None
    
    def __init__(self):
        """Initialize DBStorage"""
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV")
        
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(user, pwd, host, db),
                                      pool_pre_ping=True,
                                      )
        
        if env == "test":
            Base.metadata.drop_all(self.__engine)
            
    def all(self, cls=None):
        """Query on current database session"""
        objs = {}
        if cls:
            query = self.__session.query(cls).all()
            for obj in query:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                objs[key] = obj
        else:
            for cl in [State, City, User, Place, Review, Amenity]:
                query = self.__session.query(cl).all()
                for obj in query:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    objs[key] = obj
        return objs
        
    def new(self, obj):
        """Add object to session"""
        self.__session.add(obj)
            
    def save(self):
        """commit changes"""
        self.__session.commit()
            
    def delete(self, obj=None):
        """Delete obj from session"""
        if obj:
            self.__session.delete(obj)
               
    def reload(self):
        """Reload database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()