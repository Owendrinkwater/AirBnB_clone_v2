#!/usr/bin/python3
import unittest
from console import HBNBCommand
from models import storage
from models.state import State
from models.place import Place
from models.user import User
import re


class TestConsoleCreate(unittest.TestCase):
    """Unittest for HBNBCommand do_create with parameters"""

    def setUp(self):
        """Set up a new console instance and clear storage"""
        self.console = HBNBCommand()
        storage._FileStorage__objects = {}

    def tearDown(self):
        """Clear storage after each test"""
        storage._FileStorage__objects = {}

    def test_create_state_name(self):
        """Test creating a State with name parameter"""
        self.console.onecmd('create State name="California"')
        objs = storage.all()
        self.assertEqual(len(objs), 1)
        obj = list(objs.values())[0]
        self.assertIsInstance(obj, State)
        self.assertEqual(obj.name, "California")

    def test_create_state_name_with_underscore(self):
        """Test underscores in name are converted to spaces"""
        self.console.onecmd('create State name="New_York"')
        obj = list(storage.all().values())[0]
        self.assertEqual(obj.name, "New York")

    def test_create_place_multiple_params(self):
        """Test creating Place with multiple types of parameters"""
        self.console.onecmd(
            'create Place city_id="001" user_id="002" name="My_little_house" '
            'number_rooms=3 number_bathrooms=2 max_guest=5 price_by_night=150 '
            'latitude=37.77 longitude=-122.43'
        )
        obj = list(storage.all().values())[0]
        self.assertIsInstance(obj, Place)
        self.assertEqual(obj.city_id, "001")
        self.assertEqual(obj.user_id, "002")
        self.assertEqual(obj.name, "My little house")
        self.assertEqual(obj.number_rooms, 3)
        self.assertEqual(obj.number_bathrooms, 2)
        self.assertEqual(obj.max_guest, 5)
        self.assertEqual(obj.price_by_night, 150)
        self.assertAlmostEqual(obj.latitude, 37.77)
        self.assertAlmostEqual(obj.longitude, -122.43)

    def test_create_user_with_name_params(self):
        """Test creating User with first_name and last_name"""
        self.console.onecmd(
            'create User email="test@test.com" password="pwd" first_name="John" last_name="Doe"'
        )
        obj = list(storage.all().values())[0]
        self.assertIsInstance(obj, User)
        self.assertEqual(obj.first_name, "John")
        self.assertEqual(obj.last_name, "Doe")
        self.assertEqual(obj.email, "test@test.com")
        self.assertEqual(obj.password, "pwd")

    def test_create_invalid_params_are_skipped(self):
        """Test invalid parameters are skipped"""
        self.console.onecmd('create State invalid=123 name="ValidName"')
        obj = list(storage.all().values())[0]
        self.assertTrue(hasattr(obj, 'name'))
        self.assertEqual(obj.name, "ValidName")
        self.assertFalse(hasattr(obj, 'invalid'))

    def test_create_escaped_quotes_in_string(self):
        """Test escaped quotes inside string value"""
        self.console.onecmd('create State name="My_\\"Quoted\\"_State"')
        obj = list(storage.all().values())[0]
        self.assertEqual(obj.name, 'My "Quoted" State')


if __name__ == "__main__":
    unittest.main()