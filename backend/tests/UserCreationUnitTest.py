import unittest
from models import User
from database import SessionLocal

class TestUserCreation(unittest.TestCase):
    """
    This class contains unit tests for verifying user creation functionality.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up the database session for the tests.
        """
        cls.db = SessionLocal()

    @classmethod
    def tearDownClass(cls):
        """
        Close the database session after tests are done.
        """
        cls.db.close()

    def setUp(self):
        """
        Ensure a clean state before each test.
        """
        try:
            self.db.query(User).filter(User.email == "test@example.com").delete()
            self.db.commit()
        except Exception:
            self.db.rollback()  # Ensure rollback to reset session

    def tearDown(self):
        """
        Clean up after each test.
        """
        try:
            self.db.query(User).filter(User.email == "test@example.com").delete()
            self.db.commit()
        except Exception:
            self.db.rollback()  # Ensure rollback to reset session

    def test_user_creation(self):
        """
        Tests the creation of a user in the database.
        """
        # Create a new user
        user = User(full_name="Test User", email="test@example.com", password="password123")
        self.db.add(user)
        self.db.commit()

        # Fetch the user from the database
        fetched_user = self.db.query(User).filter(User.email == "test@example.com").first()

        # Assert that the user is created correctly
        self.assertIsNotNone(fetched_user)  # Ensure the user is not None
        self.assertEqual(fetched_user.email, "test@example.com")  # Check if email matches
        self.assertEqual(fetched_user.full_name, "Test User")  # Check if full_name matches

    def test_duplicate_user_creation(self):
        """
        Tests that creating a duplicate user fails.
        """
        # Create a new user
        user = User(full_name="Test User", email="test@example.com", password="password123")
        self.db.add(user)
        self.db.commit()

        # Attempt to create a duplicate user
        duplicate_user = User(full_name="Duplicate User", email="test@example.com", password="password123")
        self.db.add(duplicate_user)

        with self.assertRaises(Exception):  # Adjust to the specific exception raised
            try:
                self.db.commit()
            except Exception:
                self.db.rollback()  # Reset the session after the exception
                raise

if __name__ == "__main__":
    unittest.main()
