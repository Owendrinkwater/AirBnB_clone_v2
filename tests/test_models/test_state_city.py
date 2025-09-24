#!/usr/bin/python3
"""Unit tests for State and City models with storage"""
import os
import unittest
from models import storage
from models.state import State
from models.city import City


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db",
                 "Testing DBStorage only")
class TestDBStorageStateCity(unittest.TestCase):
    """Tests for State <-> City in DBStorage"""

    def setUp(self):
        """Set up clean DB before each test"""
        self.state = State(name="California")
        storage.new(self.state)
        storage.save()

    def tearDown(self):
        """Clean up DB"""
        storage.delete(self.state)
        storage.save()

    def test_create_city_for_state(self):
        """Test creating a City linked to a State"""
        city = City(name="San Francisco", state_id=self.state.id)
        storage.new(city)
        storage.save()

        # Check city is retrievable
        self.assertIn(city, self.state.cities)

    def test_cascade_delete_state_deletes_cities(self):
        """Test that deleting a State also deletes its Cities"""
        city = City(name="Los Angeles", state_id=self.state.id)
        storage.new(city)
        storage.save()

        # Delete state
        storage.delete(self.state)
        storage.save()

        # State should not exist
        self.assertIsNone(storage.all(State).get(f"State.{self.state.id}"))

        # City should also be gone
        self.assertIsNone(storage.all(City).get(f"City.{city.id}"))


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "Testing FileStorage only")
class TestFileStorageStateCity(unittest.TestCase):
    """Tests for State <-> City in FileStorage"""

    def setUp(self):
        self.state = State(name="Nevada")
        storage.new(self.state)
        storage.save()

    def tearDown(self):
        storage.delete(self.state)
        storage.save()

    def test_cities_property_returns_list(self):
        """Test State.cities property works in FileStorage"""
        city = City(name="Las Vegas", state_id=self.state.id)
        storage.new(city)
        storage.save()

        # cities should include Las Vegas
        self.assertIn(city, self.state.cities)


if __name__ == "__main__":
    unittest.main()
