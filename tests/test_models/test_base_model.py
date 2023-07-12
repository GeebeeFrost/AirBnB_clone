#!/usr/bin/python3
"""This module contains unittests for the base_model.py file"""
import unittest
from models.base_model import BaseModel
from datetime import datetime
from time import sleep


class TestBaseModelClass(unittest.TestCase):
    """Unit test cases for the BaseModel class"""

    def setUp(self):
        """Set up class"""
        self.my_model = BaseModel()
        sleep(0.05)
        self.new_model = BaseModel()

    def test_attr_type(self):
        """Test default attribute types"""
        self.assertIs(type(self.my_model.id), str)
        self.assertEqual(len(self.my_model.id), 36)
        self.assertIs(type(self.my_model.created_at), datetime)
        self.assertIs(type(self.my_model.updated_at), datetime)

    def test_unique_id(self):
        """Test uniqueness of two instance ids"""
        self.assertNotEqual(self.my_model.id, self.new_model.id)

    def test_diff_objs_mod_time(self):
        """Test that new_model is created after my_model"""
        self.assertLess(self.my_model.created_at, self.new_model.created_at)
        self.assertLess(self.my_model.updated_at, self.new_model.updated_at)

    def test_save_method(self):
        """Test updated_at attribute change after save"""
        initial = self.my_model.updated_at
        self.my_model.save()
        self.assertLess(initial, self.my_model.updated_at)

    def test_to_dict_method(self):
        """Test to_dict method"""
        self.my_model.name = "A model"
        my_json = self.my_model.to_dict()
        self.assertIn("id", my_json)
        self.assertIn("__class__", my_json)
        self.assertIn("created_at", my_json)
        self.assertIn("updated_at", my_json)
        self.assertIn("name", my_json)

    def test_create_from_dict(self):
        """Test creation of instance from a dictionary"""
        self.my_model.name = "A model"
        my_json = self.my_model.to_dict()
        another_model = BaseModel(**my_json)
        self.assertIs(type(another_model), BaseModel)
        self.assertIsNot(self.my_model, another_model)


if __name__ == "__main__":
    unittest.main()
