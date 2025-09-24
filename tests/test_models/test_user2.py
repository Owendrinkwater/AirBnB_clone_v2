#!/usr/bin/python3
"""Unit tests for User model in DBStorage"""
import os
import unittest
from models import storage
from models.user import User


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db",
                 "DBStorage only")
class TestUserDBStorage(unittest.TestCase):
    """Test User table in DB"""

    def test_user_creation(self):
        user = User(email="bob@hbtn.io", password="pwd",
                    first_name="Bob", last_name="Dylan")
        storage.new(user)
        storage.save()

        # Fetch from DB
        db_user = storage.all(User).get(f"User.{user.id}")
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.email, "bob@hbtn.io")
        self.assertEqual(db_user.first_name, "Bob")
        self.assertEqual(db_user.last_name, "Dylan")


if __name__ == "__main__":
    unittest.main()