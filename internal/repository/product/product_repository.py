from models.product import Product
from sqlalchemy.exc import SQLAlchemyError

class ProductRepository:
    def __init__(self, database):
        self.Session = database.Session
        
    def create_product(self, name, price, description, quantity):
        try:
            new_product = Product(name=name, price=price, description=description, quantity=quantity)
            with self.Session() as session:
                session.add(new_product)
                session.commit()
                session.refresh(new_product)
            return new_product
        except SQLAlchemyError as e:
            self.Session.rollback()
            raise e

    def get_product_by_id(self, product_id):
        with self.Session() as session:
            return session.query(Product).filter_by(id=product_id).first()

    def get_all_products(self, sort_by='created_time', is_ascending=True):
        with self.Session() as session:
            sort_column = getattr(Product, sort_by, Product.created_time)

            query = session.query(Product).order_by(
                sort_column.asc() if is_ascending else sort_column.desc()
            )

            return query.all()
    
    def count_products_with_filter(self, filter_criteria):
        with self.Session() as session:
            query = session.query(Product)

            if filter_criteria:
                for key, value in filter_criteria.items():
                    if hasattr(Product, key):
                        query = query.filter(getattr(Product, key) == value)
            return query.count()
