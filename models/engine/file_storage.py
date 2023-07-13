#!/usr/bin/python3
"""This module contains the FileStorage class"""
import json
import os


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
        final = {obj_id: objs[obj_id].to_dict() for obj_id in objs.keys()}
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(final, f)

    def reload(self):
        """Deserializes the JSON file to __objects, if it exists"""
        if not (os.path.isfile(FileStorage.__file_path) and
                os.path.getsize(FileStorage.__file_path) > 0):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            obj_dict = json.load(f)
            for obj in obj_dict.values():
                cln = obj["__class__"]
                self.new(self.actual_class(cln)(**obj))

    @staticmethod
    def actual_class(name):
        """Returns class references for creation of new instances"""
        from models.base_model import BaseModel
        classes = {"BaseModel": BaseModel}
        for cls in classes.keys():
            if name == cls:
                return classes[cls]
