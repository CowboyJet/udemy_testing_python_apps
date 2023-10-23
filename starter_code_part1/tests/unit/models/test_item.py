from unittest import TestCase
from unittest.mock import patch

from models.item import ItemModel


class TestItem(TestCase):
    def test_init(self):
        name, price = "Test", 10
        item = ItemModel(name, price)

        self.assertEqual(item.name, name)
        self.assertEqual(item.price, price)

    def test_json(self):
        name, price = "Test", 10
        item = ItemModel(name, price)
        expected_json = {'name': name, 'price': price}

        self.assertDictEqual(item.json(), expected_json)
