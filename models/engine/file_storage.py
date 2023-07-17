#!/usr/bin/python3
"""This module contains the FileStorage class"""
import json
import os
import datetime


class FileStorage:
    """Serializes instances to JSON files
    and deserializes JSON files to instances"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Adds obj to __objects"""
        entry = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[entry] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        objs = FileStorage.__objects
        final = {obj_id: obj.to_dict() for obj_id, obj in objs.items()}
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(final, f)

    def reload(self):
        """Deserializes the JSON file to __objects, if it exists"""
        if not os.path.isfile(FileStorage.__file_path):
            return
        if not os.path.getsize(FileStorage.__file_path) > 0:
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            obj_dict = json.load(f)
            for obj in obj_dict.values():
                cln = obj["__class__"]
                if self.actual_class(cln):
                    self.new(self.actual_class(cln)(**obj))

    @staticmethod
    def actual_class(name):
        """Returns class references for creation of new instances"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        classes = {
                "BaseModel": BaseModel,
                "User": User,
                "State": State,
                "City": City,
                "Amenity": Amenity,
                "Place": Place,
                "Review": Review}
        for cls in classes.keys():
            if name == cls:
                return classes[cls]
        return None

    @staticmethod
    def attrs(cln):
        """Returns valid attributes and their types for a class"""
        attribs = {
                "BaseModel": {
                    "id": str,
                    "created_at": datetime.datetime,
                    "updated_at": datetime.datetime},
                "User": {
                    "email": str,
                    "password": str,
                    "first_name": str,
                    "last_name": str},
                "State": {
                    "name": str},
                "City": {
                    "state_id": str,
                    "name": str},
                "Amenity": {
                    "name": str},
                "Place": {
                    "city_id": str,
                    "user_id": str,
                    "name": str,
                    "description": str,
                    "number_rooms": int,
                    "number_bathrooms": int,
                    "max_guest": int,
                    "price_by_night": int,
                    "latitude": float,
                    "longitude": float,
                    "amenity_ids": list},
                "Review": {
                    "place_id": str,
                    "user_id": str,
                    "text": str}}
        for attrib in attribs.keys():
            if cln == attrib:
                return attribs[cln]
        return None
