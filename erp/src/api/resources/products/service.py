from src import exceptions
from src.models import Product


class ProductService:
    def __init__(self, name=None, category=None):
        self.name_filter = name
        self.category_filter = category

    def check_filters(self):
        return any([self.name_filter, self.category_filter])

    def get_products(self):
        # without filters
        if not self.check_filters():
            return [product for product in Product.select()]
        else:
            # with filters
            products_query = Product.select()
            if self.name_filter:
                products_query = products_query.where(
                    Product.name == self.name_filter
                )
            if self.category_filter:
                products_query = products_query.where(
                    Product.category == self.category_filter
                )

            return [product for product in products_query]

    def create_new_product(self, product_info):
        # search for the product if exists
        product = (
            Product.select()
            .where(Product.name == product_info["name"])
            .first()
        )
        if product:
            raise exceptions.NotFound(
                product_name=product_info["name"],
                operation="CREATE_NEW_PRODUCT",
            )

        # create new product
        product = Product(**product_info)
        product.save()
        return product

    def get_one_product(self, product_id):
        product = Product.get_by_id(product_id)
        if not product:
            raise exceptions.NotFound(
                product_id=product_id, operation="GET_ONE_PRODUCT"
            )
        else:
            return product
