import unittest
from unittest.mock import MagicMock
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models.product import Product, BaseProduct
from internal.repository.product.product_repository import ProductRepository
from pkg.postgres.client import DatabaseClient

class TestProductRepository(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database
        db = DatabaseClient('sqlite:///:memory:')
        # Create tables in the in-memory database
        BaseProduct.metadata.create_all(db.engine)

        # Create a ProductRepository instance with the in-memory database
        self.product_repository = ProductRepository(db)
        self.session = db.Session()
        self.engine = db.engine

    def tearDown(self):
        # Close the session and drop tables after each test
        self.session.close()
        BaseProduct.metadata.drop_all(self.engine)

    def test_create_product(self):
        # Arrange
        name = 'Test Product'
        price = 9.99
        description = 'Test description'
        quantity = 5

        # Act
        created_product = self.product_repository.create_product(name, price, description, quantity)

        # Assert
        self.assertIsNotNone(created_product.id)
        self.assertEqual(created_product.name, name)
        self.assertEqual(created_product.price, price)
        self.assertEqual(created_product.description, description)
        self.assertEqual(created_product.quantity, quantity)

        # Check if the product was added to the database
        product_in_db = self.session.query(Product).filter_by(id=created_product.id).first()
        print(product_in_db.id)
        self.assertIsNotNone(product_in_db)
    
    def test_get_product_by_id(self):
        # Arrange
        name = 'Test Product'
        price = 9.99
        description = 'Test description'
        quantity = 5
        created_product = self.product_repository.create_product(name, price, description, quantity)

        # Act
        product = self.product_repository.get_product_by_id(created_product.id)

        # Assert
        self.assertEqual(product.id, created_product.id)
        self.assertEqual(product.name, name)
        self.assertEqual(product.price, price)
        self.assertEqual(product.description, description)
        self.assertEqual(product.quantity, quantity)
    
    def test_get_all_products(self):
        # Arrange
        name = 'Test Product'
        price = 9.99
        description = 'Test description'
        quantity = 5
        created_product = self.product_repository.create_product(name, price, description, quantity)

        # Act
        products = self.product_repository.get_all_products()

        # Assert
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, created_product.id)
        self.assertEqual(products[0].name, name)
        self.assertEqual(products[0].price, price)
        self.assertEqual(products[0].description, description)
        self.assertEqual(products[0].quantity, quantity)
        
    def test_count_products_with_filter(self):
        # Arrange
        name = 'Test Product'
        price = 9.99
        description = 'Test description'
        quantity = 5
        _ = self.product_repository.create_product(name, price, description, quantity)

        # Act
        count = self.product_repository.count_products_with_filter({})

        # Assert
        self.assertEqual(count, 1)

if __name__ == '__main__':
    unittest.main()
