from flask import jsonify, request
from internal.usecase.product.error import *

class ProductController:
    def __init__(self, product_usecase):
        self.product_usecase = product_usecase
    
    def define_routes(self, app):
        app.add_url_rule('/products', 'create_product', self.create_product, methods=['POST'])
        app.add_url_rule('/products/<int:product_id>', 'get_product', self.get_product, methods=['GET'])
        app.add_url_rule('/products', 'get_all_products', self.get_all_products, methods=['GET'])
        return app

    def create_product(self):
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Invalid request. JSON data is required.'}), 400
        
        product_name = data.get('product_name')
        price = data.get('price')
        description = data.get('description')
        quantity = data.get('quantity')
        
        # validate request value
        if not all([product_name, price, quantity]):
            return jsonify({'error': 'Incomplete data. Please provide all required fields.'}), 400

        try:
            price = float(price)
            quantity = int(quantity)
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid data type for price or quantity.'}), 400
        
        # validate price and quantity value
        if price <= 0 or quantity <= 0:
            return jsonify({'error': 'Price and quantity must be greater than or equal to 0.'}), 400

        try:
            product = self.product_usecase.create_product(product_name, price, description, quantity)
            if product:
                return jsonify(product)
            else:
                return jsonify({"error": "Failed to create product"}), 400
        except Exception as e:
            if isinstance(e, DuplicateProductError):
                return jsonify({"error": str(e)}), 409
            return jsonify({"error": str(e)}), 500
            
    def get_product(self, product_id):
        try:
            product = self.product_usecase.get_product(product_id)
            if product:
                return jsonify(product)
            else:
                return jsonify({"error": "Product not found"}), 404
        except Exception as e:
            if isinstance(e, ProductNotFoundError):
                return jsonify({"error": str(e)}), 404
            return jsonify({"error": str(e)}), 500

    def get_all_products(self):
        sort_by = request.args.get('sort_by', default="created_time")
        is_ascending = request.args.get('is_ascending', default=True, type=bool)
        try:
            products = self.product_usecase.get_all_products(sort_by, is_ascending)
            return jsonify(products)
        except Exception as e:
            if isinstance(e, SortFieldIsNotValidError):
                return jsonify({"error": str(e)}), 400
            return jsonify({"error": str(e)}), 500