from models.user import UserModel
from tests.base_test import BaseTest
import json

class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/register", json={"username": "test", "password": "123"})

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual(json.loads(response.data), {"message": "User created successfully."})
                self.assertIsNotNone(UserModel.find_by_username("test"))


    def test_authenticate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register", json={"username": "test", "password": "123"})
                response = client.post("/auth", json={"username": "test", "password": "123"})

                self.assertIn("access_token", json.loads(response.data))
                self.assertIn("refresh_token", json.loads(response.data))


    def test_user_exists(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register", json={"username": "test", "password": "123"})
                
                response = client.post("/register", json={"username": "test", "password": "123"})

                self.assertEqual(response.status_code, 409)
                self.assertDictEqual(json.loads(response.data), {"message": "A user with that username already exists"})
