from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                client.post("/register", json={"username": "test", "password": "123"})
                auth_response = client.post(
                    "/auth", json={"username": "test", "password": "123"}
                )
                access_token = json.loads(auth_response.data)["access_token"]
                self.header = {"Authorization": f"Bearer {access_token}"}

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get("/item/test")

                self.assertEqual(resp.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get("/item/test", headers=self.header)

                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual(
                    json.loads(resp.data), {"message": "Item not found"}
                )

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 19.99, 1).save_to_db()
                resp = client.get("/item/test", headers=self.header)

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(
                    json.loads(resp.data), {"name": "test", "price": 19.99}
                )

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 19.99, 1).save_to_db()

                resp = client.delete("/item/test")

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {"message": "Item deleted"})

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                resp = client.post("/item/test", json={"price": 19.99, "store_id": 1})

                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual(
                    json.loads(resp.data), {"name": "test", "price": 19.99}
                )

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 19.99, 1).save_to_db()

                resp = client.post("/item/test", json={"price": 19.99, "store_id": 1})

                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual(
                    json.loads(resp.data),
                    {"message": "An item with name 'test' already exists."},
                )

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()

                resp = client.put("/item/test", json={"price": 19.99, "store_id": 1})

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(
                    json.loads(resp.data), {"name": "test", "price": 19.99}
                )

    def test_put_item_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 19.99, 1).save_to_db()

                resp = client.put("/item/test", json={"price": 10, "store_id": 1})

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(
                    json.loads(resp.data), {"name": "test", "price": 10}
                )

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 19.99, 1).save_to_db()

                resp = client.get("/items")
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(
                    json.loads(resp.data), {"items": [{"name": "test", "price": 19.99}]}
                )
