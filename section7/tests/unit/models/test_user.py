from tests.unit.unit_base_test import UnitBaseTest
from models.user import UserModel

class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel("Test User", "Test Password")

        self.assertEqual(user.username, "Test User")
        self.assertEqual(user.password, "Test Password")