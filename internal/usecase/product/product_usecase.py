class ProductUseCase:
    def __init__(self, product_repository):
        self.product_repository = product_repository

    def create_product(self, product_name, price, description, quantity):
        return self.product_repository.create_product(product_name, price, description, quantity)

    def get_product(self, product_id):
        return self.product_repository.get_product_by_id(product_id)

    def get_all_products(self, sort_by, is_ascending):
        return self.product_repository.get_all_products(sort_by, is_ascending)