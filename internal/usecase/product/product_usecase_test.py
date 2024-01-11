import unittest
from unittest.mock import MagicMock
from internal.usecase.product.product_usecase import ProductUseCase
from models.product import Product
import datetime
import gzip
import json

class TestProductUseCase(unittest.TestCase):
    def setUp(self):
        self.product_repository = MagicMock()
        self.cache = MagicMock()
        self.usecase = ProductUseCase(self.product_repository, self.cache)

    def test_create_product(self):
        # Mock the necessary dependencies
        name = "Test Product"
        price = 10.99
        description = "This is a test product"
        quantity = 5
        created_time = datetime.datetime.now()
        self.product_repository.count_products_with_filter.return_value = 0
        self.product_repository.create_product.return_value = Product(id=1, name=name, price=price, description=description, quantity=quantity, created_time=created_time)

        # Call the function under test
        result = self.usecase.create_product(name, price, description, quantity)
            
        # Assert the expected behavior
        self.assertEqual(result["name"], name)
        self.product_repository.count_products_with_filter.assert_called_once_with({"name": "Test Product"})
        self.product_repository.create_product.assert_called_once_with(name, price, description, quantity)
        self.cache.setx.assert_called_once()

    def test_get_product_from_redis(self):
        # Mock the necessary dependencies
        product_id = 1
        cache_key = "pid#1"
        payload = {"product_id": 1, "name": "Test Product"}
        compressed_payload = b"compressed_payload"
        self.cache.get.return_value = compressed_payload
        result = json.dumps(payload)
        gzip.decompress = MagicMock(return_value=result)

        # Call the function under test
        result = self.usecase.get_product(product_id)

        # Assert the expected behavior
        self.assertEqual(result["name"], payload["name"])
        self.cache.get.assert_called_once_with(cache_key)
    
    def test_get_product_from_database(self):
        # Mock the necessary dependencies
        product_id = 1
        cache_key = "pid#1"
        payload = {"product_id": 1, "name": "Test Product"}
        self.cache.get.return_value = None
        self.product_repository.get_product_by_id.return_value = Product(id=1, name="Test Product", price=10, description="desc", quantity=1, created_time=datetime.datetime.now())

        # Call the function under test
        result = self.usecase.get_product(product_id)

        # Assert the expected behavior
        self.assertEqual(result["name"], payload["name"])
        self.cache.get.assert_called_once_with(cache_key)
        self.product_repository.get_product_by_id.assert_called_once_with(product_id)
        self.cache.setx.assert_called_once()
    def test_get_all_products_from_redis(self):
        # Mock the necessary dependencies
        sort_by = "name"
        is_ascending = True
        cache_key = "list#1#1"
        payload = [{"product_id": 1, "name": "Test Product"}]
        compressed_payload = b"compressed_payload"
        self.cache.get.return_value = compressed_payload
        result = json.dumps(payload)
        gzip.decompress = MagicMock(return_value=result)

        # Call the function under test
        result = self.usecase.get_all_products(sort_by, is_ascending)

        # Assert the expected behavior
        self.assertEqual(result[0]["name"], payload[0]["name"])
        self.cache.get.assert_called_once_with(cache_key)
    def test_get_all_products_from_database(self):
        # Mock the necessary dependencies
        sort_by = "name"
        is_ascending = True
        cache_key = "list#1#1"
        payload = [{"product_id": 1, "name": "Test Product"}]
        self.cache.get.return_value = None
        self.product_repository.get_all_products.return_value = [Product(id=1, name="Test Product", price=10, description="desc", quantity=1, created_time=datetime.datetime.now())]
        
        # Call the function under test
        result = self.usecase.get_all_products(sort_by, is_ascending)

        # Assert the expected behavior
        self.assertEqual(result[0]["name"], payload[0]["name"])
        self.cache.get.assert_called_once_with(cache_key)
        self.product_repository.get_all_products.assert_called_once()
        self.cache.setx.assert_called_once()

if __name__ == "__main__":
    unittest.main()