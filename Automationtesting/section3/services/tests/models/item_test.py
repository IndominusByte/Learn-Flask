from basetest import BaseTest
from services.models.ItemsModel import ItemModel

class ItemTest(BaseTest):
    def test_create_item(self):
        item = ItemModel('name',2.0,1)
        self.assertEqual(item.name,'name')
        self.assertEqual(item.price,2.0)
