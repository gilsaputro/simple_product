from internal.usecase.product.error import *
import json
import gzip
from internal.usecase.product.error import DuplicateProductError, ProductNotFoundError, SortFieldIsNotValidError

ExpiredTimeGetData = 60 * 60 
ExpiredTimeListData = 60 * 2 
class ProductUseCase:
    def __init__(self, product_repository, cache):
        self.product_repository = product_repository
        self.cache = cache

    def create_product(self, name, price, description, quantity):
        filter_criteria = {"name": name}
        count = self.product_repository.count_products_with_filter(filter_criteria)
        if count > 0 :
            raise DuplicateProductError(name)
        
        # create product
        product = self.product_repository.create_product(name, price, description, quantity)
        if product:
            # compress payload
            cache_key = generate_cache_key_by_id(product.id)
            payload = self.serialize_product(product)
            compressed_payload = gzip.compress(json.dumps(payload).encode())
            # set payload to redis for by id key
            self.cache.setx(cache_key,compressed_payload,ExpiredTimeGetData)
            return payload
        return 

    def get_product(self, product_id):
        cache_key = generate_cache_key_by_id(product_id)
        # check to cache
        products = self.cache.get(cache_key)
        if products and len(products) > 0:
            #decompress payload
            payload = gzip.decompress(products)
            return json.loads(payload)
        
        # get data from db if cache is empty
        products = self.product_repository.get_product_by_id(product_id)
        if products:
            #compress payload
            payload = self.serialize_product(products)
            compressed_payload = gzip.compress(json.dumps(payload).encode())
            # set payload to redis for by id key
            self.cache.setx(cache_key,compressed_payload,ExpiredTimeGetData)
            return payload
        raise ProductNotFoundError() 

    def get_all_products(self, sort_by, is_ascending):
        # checking sort file
        valid_sort_fields = ['name', 'price', 'created_time']
        if sort_by not in valid_sort_fields:
            raise SortFieldIsNotValidError()
        
        cache_key = generate_cache_key_by_filter(sort_by, is_ascending)
        # check to cache
        products = self.cache.get(cache_key)
        if products and len(products) > 0:
            #decompress payload
            payload = gzip.decompress(products)
            return json.loads(payload)
        
        # get data from db if cache is empty
        products = self.product_repository.get_all_products(sort_by, is_ascending)
        if products:
                #compress payload
                payload = [self.serialize_product(product) for product in products]
                compressed_payload = gzip.compress(json.dumps(payload).encode())
                # set payload to redis for list key
                self.cache.setx(cache_key,compressed_payload,ExpiredTimeListData)
                return payload
        raise ProductNotFoundError()

        
    def serialize_product(self, product):
        return {
            "product_id": product.id,
            "name": product.name,
            "created_time": product.created_time.strftime("%m/%d/%Y, %H:%M:%S"),
            'price': product.price,
            'description': product.description,
            'quantity': product.quantity
        }


def generate_cache_key_by_id(id):
    return f"pid#{id}"

def generate_cache_key_by_filter(sort_by, is_ascending):
    flag = 0
    if is_ascending :
        flag = 1
    
    sort_type = 0
    match sort_by:
        case "name":
            sort_type = 1
        case "price":
            sort_type = 2
        case "created_time":
            sort_type = 3
        case _ :
            sort_type = 0
            
    return f"list#{sort_type}#{flag}"
