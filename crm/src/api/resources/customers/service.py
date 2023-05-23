from src import exceptions
from src.models import Order, Product, UserRoles


class CustomersService:
    def __init__(
        self, name_filter=None, last_name_filter=None, email_filter=None
    ):
        self.name_filter = name_filter
        self.last_name = last_name_filter
        self.email_filter = email_filter

    def check_filters(self):
        return any([self.name_filter, self.category_filter, self.email_filter])

    def get_customers(self):
        customers = UserRoles.get_users_by_role(
            "webshop-client",
            self.name_filter,
            self.last_name,
            self.email_filter,
        )
        return customers

    def get_one_customer(self, customer_id):
        customer = UserRoles.get_users_by_role(
            "webshop-client", user_id_filter=customer_id
        )
        if not customer:
            raise exceptions.NotFound(
                customer_id=customer_id, operation="GET_ONE_CUSTOMER"
            )
        return customer[0]

    def get_customer_orders(self, customer_id):
        customer = self.get_one_customer(customer_id)
        orders = Order.select().where(Order.user == customer)
        return [order for order in orders]

    def get_customer_order_detail(self, customer_id, order_id):
        orders = self.get_customer_orders(customer_id)

        products = []
        for order in orders:
            if order.order_id == order_id:
                products.append(
                    Product.select().where(Product.id == order.product).first()
                )

        if not products:
            raise exceptions.NotFound(
                order_id=order_id, operation="GET_ONE_CUSTOMER"
            )

        return products
