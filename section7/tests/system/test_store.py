from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/store/test")

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual(
                    json.loads(response.data), {"name": "test", "id": 1, "items": []}
                )
                self.assertIsNotNone(StoreModel.find_by_name("test"))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test")

                response = client.post("/store/test")

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(
                    json.loads(response.data),
                    {"message": "A store with name 'test' already exists."},
                )

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()

                response = client.delete("/store/test")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(
                    json.loads(response.data), {"message": "Store deleted"}
                )
                self.assertIsNone(StoreModel.find_by_name("test"))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()

                response = client.get("/store/test")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(
                    json.loads(response.data), {"name": "test", "id": 1, "items": []}
                )

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("/store/test")

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(
                    json.loads(response.data), {"message": "Store not found"}
                )

    def test_find_store_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test item", 19.99, 1).save_to_db()
                expected = {
                    "name": "test",
                    "id": 1,
                    "items": [{"name": "test item", "price": 19.99}],
                }

                response = client.get("/store/test")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected)

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()

                response = client.get("/stores")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(
                    json.loads(response.data),
                    {"stores": [{"name": "test", "id": 1, "items": []}]},
                )

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test item", 19.99, 1).save_to_db()
                expected = {
                    "stores": [
                        {
                            "name": "test",
                            "id": 1,
                            "items": [{"name": "test item", "price": 19.99}],
                        }
                    ]
                }

                response = client.get("/stores")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected)
