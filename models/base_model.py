#!/usr/bin/python3
"""This module contains the BaseModel class"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """The base model class"""
    def __init__(self, *args, **kwargs):
        """Creates a new BaseModel instance"""
        if kwargs and len(kwargs) > 0:
            for k, v in kwargs.items():
                if k != "__class__":
                    setattr(self, k, v)
            self.created_at = datetime.fromisoformat(self.created_at)
            self.updated_at = datetime.fromisoformat(self.updated_at)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Returns a string representation of a BaseModel instance"""
        cln = self.__class__.__name__
        return "[{}] ({}) {}".format(cln, self.id, self.__dict__)

    def save(self):
        """Updates the updated_at attribute"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns a dictionary containing contents of __dict__"""
        self.created_at = self.created_at.isoformat()
        self.updated_at = self.updated_at.isoformat()
        rep = {k: v for k, v in self.__dict__.items()}
        rep['__class__'] = self.__class__.__name__
        return rep
