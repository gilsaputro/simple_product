class DuplicateProductError(Exception):
    def __init__(self, name):
        self.name = name
        super().__init__(f"A product with the name '{name}' already exists.")

class ProductNotFoundError(Exception):
    def __init__(self):
        super().__init__(f"Product is not exists.")

class SortFieldIsNotValidError(Exception):
    def __init__(self):
        super().__init__(f"Invalid sort_by field.")