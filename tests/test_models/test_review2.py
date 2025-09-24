#!/usr/bin/python3
"""Unit tests for Review model in DBStorage"""
import os
import unittest
from models import storage
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db",
                 "DBStorage only")
class TestReviewDBStorage(unittest.TestCase):
    """Test Review table in DB"""

    def setUp(self):
        """Create User, City, Place for Review foreign keys"""
        self.user = User(email="alex@hbtn.io", password="pwd")
        self.city = City(name="Kisumu", state_id="fake")
        storage.new(self.user)
        storage.new(self.city)
        storage.save()

        self.place = Place(city_id=self.city.id, user_id=self.user.id,
                           name="Lakeview", number_rooms=2,
                           number_bathrooms=1, max_guest=4,
                           price_by_night=80)
        storage.new(self.place)
        storage.save()

    def test_review_creation(self):
        review = Review(text="Amazing stay!", place_id=self.place.id,
                        user_id=self.user.id)
        storage.new(review)
        storage.save()

        db_review = storage.all(Review).get(f"Review.{review.id}")
        self.assertIsNotNone(db_review)
        self.assertEqual(db_review.text, "Amazing stay!")
        self.assertEqual(db_review.place_id, self.place.id)
        self.assertEqual(db_review.user_id, self.user.id)


if __name__ == "__main__":
    unittest.main()
