from models.store import StoreModel
from models.item import ItemModel

from section7.tests.base_test import BaseTest

class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel("Test Store")

        self.assertListEqual(store.items.all(), [])

    def test_crud(self):
        with self.app_context():
            store = StoreModel("Test Store")

            self.assertIsNone(StoreModel.find_by_name("Test Store"))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name("Test Store"))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name("Test Store"))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel("Test Store")
            item = ItemModel("Test Item", 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, "Test Item")

    def test_json_empty_list(self):
        with self.app_context():
            store = StoreModel("Test Store")
            store.save_to_db()
            expected = {
                "name": "Test Store",
                "id": 1,
                "items": []
            }

            self.assertDictEqual(store.json(), expected)

    def test_json_with_list(self):
        with self.app_context():
            store = StoreModel("Test Store")
            item = ItemModel("Test Item", 19.99, 1)
            store.save_to_db()
            item.save_to_db()

            expected = {
                "name": "Test Store",
                "id": 1,
                "items": [{
                    "name": "Test Item",
                    "price": 19.99
                }]
            }

            self.assertDictEqual(store.json(), expected)