import datetime

from src import exceptions
from src.models import Order, Product, User


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

    def get_product_orders(self, product_id):
        product = Product.get_by_id(product_id)
        if not product:
            raise exceptions.NotFound(
                product_id=product_id, operation="GET_PRODUCT_ORDERS"
            )
        orders = Order.select().where(Order.product == product_id)
        return [order for order in orders]

    def create_new_order(self, product_id, order_detail):
        product = Product.get_by_id(product_id)
        if not product:
            raise exceptions.NotFound(
                product_id=product_id, operation="CREATE_NEW_ORDER"
            )

        user = User.get_user_by_id(order_detail["user_id"])
        if not user:
            raise exceptions.NotFound(
                user_id=order_detail["user_id"], operation="CREATE_NEW_ORDER"
            )

        if product.quantity - order_detail["quantity"] < 0:
            raise exceptions.OrderAborted(
                user_id=order_detail["user_id"],
                product_id=product_id,
                product_quantity=product.quantity,
                order_quantity=order_detail["quantity"],
                reason="STORAGE_LESS_THAN_QUANTITY",
                operation="CREATE_NEW_ORDER",
            )
        # creating a new order
        product.quantity -= 1
        product.save()

        order_price = product.price * order_detail["quantity"]
        order = Order(
            user=user.id,
            product=product.id,
            order_date=datetime.datetime.now(),
            order_quantity=order_detail["quantity"],
            order_price=order_price,
        )
        order.save()

    def get_one_order(self, product_id, order_id):
        product = Product.get_by_id(product_id)
        if not product:
            raise exceptions.NotFound(
                product_id=product_id, operation="CREATE_NEW_ORDER"
            )
        order = Order.get_by_id(order_id)
        if not order:
            raise exceptions.NotFound(
                order_id=order_id, operation="CREATE_NEW_ORDER"
            )
        return order
