#!/usr/bin/python3
"""Unit tests for Place model in DBStorage"""
import os
import unittest
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db",
                 "DBStorage only")
class TestPlaceDBStorage(unittest.TestCase):
    """Test Place table in DB"""

    def setUp(self):
        """Create a City and User for Place foreign keys"""
        self.user = User(email="jane@hbtn.io", password="123")
        self.city = City(name="Nairobi", state_id="fake")
        storage.new(self.user)
        storage.new(self.city)
        storage.save()

    def test_place_creation(self):
        place = Place(city_id=self.city.id, user_id=self.user.id,
                      name="Lovely place", number_rooms=3,
                      number_bathrooms=1, max_guest=2, price_by_night=100,
                      latitude=1.303, longitude=36.822)
        storage.new(place)
        storage.save()

        db_place = storage.all(Place).get(f"Place.{place.id}")
        self.assertIsNotNone(db_place)
        self.assertEqual(db_place.name, "Lovely place")
        self.assertEqual(db_place.number_rooms, 3)
        self.assertEqual(db_place.max_guest, 2)


if __name__ == "__main__":
    unittest.main()
