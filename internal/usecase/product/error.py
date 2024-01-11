class DuplicateProductError(Exception):
    def __init__(self, product_name):
        self.product_name = product_name
        super().__init__(f"A product with the name '{product_name}' already exists.")