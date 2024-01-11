from internal.usecase.product.error import *
class ProductUseCase:
    def __init__(self, product_repository):
        self.product_repository = product_repository

    def create_product(self, product_name, price, description, quantity):
        filter_criteria = {"name": product_name}
        count = self.product_repository.count_products_with_filter(filter_criteria)
        if count > 0 :
            raise DuplicateProductError(product_name)
        
        return self.product_repository.create_product(product_name, price, description, quantity)

    def get_product(self, product_id):
        return self.product_repository.get_product_by_id(product_id)

    def get_all_products(self, sort_by, is_ascending):
        return self.product_repository.get_all_products(sort_by, is_ascending)