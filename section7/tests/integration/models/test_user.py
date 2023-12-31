from models.user import UserModel

from section7.tests.base_test import BaseTest

class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel("Test User", "Test Password")

            self.assertIsNone(UserModel.find_by_username("Test User"))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()
            
            self.assertIsNotNone(UserModel.find_by_username("Test User"))
            self.assertIsNotNone(UserModel.find_by_id(1))
