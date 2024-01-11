import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
from internal.controller.product.product_controller import ProductController

class TestProductController(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.product_usecase_mock = MagicMock()
        self.controller = ProductController(self.product_usecase_mock)

    def test_create_product_success(self):
        request_data = {
            'name': 'Test Product',
            'price': 10.99,
            'description': 'This is a test product.',
            'quantity': 5
        }

        with self.app.test_request_context('/', json=request_data):
            product_mock =  {
                "product_id": 1,
                "name": "name",
                "created_time": "2021/01/01 00:00:00",
                'price': 10,
                'description': "description",
                'quantity': 10
            }
            self.product_usecase_mock.create_product.return_value = product_mock

            response = self.controller.create_product()

            self.product_usecase_mock.create_product.assert_called_once_with(
                'Test Product', 10.99, 'This is a test product.', 5
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, product_mock)

    def test_create_product_fail(self):
        request_data = {
            'name': 'Test Product',
            'price': 10.99,
            'description': 'This is a test product.',
            'quantity': 5
        }

        with self.app.test_request_context('/', json=request_data):
            self.product_usecase_mock.create_product.raise_exception.side_effect = Exception('Test Exception')

            response = self.controller.create_product()
            self.product_usecase_mock.create_product.assert_called_once_with(
                'Test Product', 10.99, 'This is a test product.', 5
            )

            self.assertEqual(response[1], 500)
    
    def test_get_product_success(self):
        with self.app.test_request_context('/'):
            product_id = 1
            product_mock = {'id': product_id, 'name': 'Test Product', 'price': 10.99, 'quantity': 5}
            self.product_usecase_mock.get_product.return_value = product_mock

            response = self.controller.get_product(product_id)

            self.product_usecase_mock.get_product.assert_called_once_with(product_id)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, product_mock)
    
    def test_get_product_fail(self):
        with self.app.test_request_context('/'):
            product_id = 1
            self.product_usecase_mock.get_product.raise_exception.side_effect = Exception('Test Exception')

            response = self.controller.get_product(product_id)

            self.product_usecase_mock.get_product.assert_called_once_with(product_id)

            self.assertEqual(response[1], 500)
    
    def test_get_all_products_success(self):
        with self.app.test_request_context('/'):
            product_mock = {'id': 1, 'name': 'Test Product', 'price': 10.99, 'quantity': 5}
            self.product_usecase_mock.get_all_products.return_value = [product_mock]

            response = self.controller.get_all_products()

            self.product_usecase_mock.get_all_products.assert_called_once_with('created_time', True)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [product_mock])
    
    def test_get_all_products_fail(self):
        with self.app.test_request_context('/'):
            self.product_usecase_mock.get_all_products.raise_exception.side_effect = Exception('Test Exception')

            response = self.controller.get_all_products()

            self.product_usecase_mock.get_all_products.assert_called_once_with('created_time', True)

            self.assertEqual(response[1], 500)

if __name__ == '__main__':
    unittest.main()