#!/usr/bin/python3
"""This module contains the base model class"""
import uuid
from datetime import datetime


class BaseModel:
    """The base model class"""
    def __init__(self):
        """Creates a new BaseModel instance"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()

    def __str__(self):
        cln = self.__class__.__name__
        return "[{}] ({}) {}".format(cln, self.id, self.__dict__)
    
    def save(self):
        """Updates the updated_at attribute"""
        self.updated_at = datetime.today()

    def to_dict(self):
        """Returns a dictionary containing contents of __dict__"""
        self.created_at = self.created_at.isoformat()
        self.updated_at = self.updated_at.isoformat()
        rep = {k: v for k, v in self.__dict__.items()}
        rep['__class__'] = self.__class__.__name__
        return rep
