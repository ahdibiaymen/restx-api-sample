import datetime
import random

from faker import Faker

from erp.src.models import Order, Product, Prospect, Role, User, UserRoles

fake = Faker()

# init roles
Role.init_roles()

print("Populate DB with prospects ...")

leads_list = [
    "REFERRAL",
    "WEBSITE",
    "SOCIAL_MEDIA",
    "EVENT",
    "ADVERTISING",
    "EMAIL",
    "SALES_OUTREACH",
    "PARTNERSHIP",
    "OTHER",
]

status_list = [
    "NEW_LEAD",
    "CONTACTED",
    "QUALIFIED",
    "PROPOSAL_SENT",
    "NEGOTIATING",
    "CLOSED_WON",
    "CLOSED_LOST",
    "ON_HOLD",
    "DISQUALIFIED",
    "OTHER",
]
for i in range(10):
    name = fake.first_name()
    last_name = fake.last_name()
    user_data = {
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=65),
        "name": name + " " + last_name,
        "email": name + "-" + last_name + "@mail.com",
        "company": fake.company(),
        "phone_number": fake.phone_number(),
        "lead_source": random.choice(leads_list),
        "status": random.choice(status_list),
    }
    prospect = Prospect(**user_data)
    prospect.save()
print("Done!")

print("Populate DB with products ...")
products = {
    "product1": Product(
        name="Espresso", quantity="110", category="Dark Roast", price=2.99
    ),
    "product2": Product(
        name="Cappuccino",
        quantity="115",
        category="Blended Coffee",
        price=3.49,
    ),
    "product3": Product(
        name="Latte", quantity="112", category="Flavored Coffee", price=4.99
    ),
    "product4": Product(
        name="Americano", quantity="118", category="Medium Roast", price=2.79
    ),
    "product5": Product(
        name="Mocha", quantity="113", category="Chocolate Coffee", price=4.29
    ),
    "product6": Product(
        name="Macchiato", quantity="115", category="Light Roast", price=2.49
    ),
    "product7": Product(
        name="Irish Coffee",
        quantity="127",
        category="Alcoholic Coffee",
        price=5.99,
    ),
    "product8": Product(
        name="Frappuccino",
        quantity="111",
        category="Frozen Coffee",
        price=4.49,
    ),
    "product9": Product(
        name="Turkish Coffee",
        quantity="116",
        category="Specialty Coffee",
        price=3.99,
    ),
    "product10": Product(
        name="Drip Coffee",
        quantity="141",
        category="Classic Coffee",
        price=1.99,
    ),
}

for product in products.values():
    product.save()
print("Done!")

# users
# admin
print("Populate DB with Admin user ...")
admin_user_data = {
    "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=65),
    "name": fake.first_name(),
    "last_name": fake.last_name(),
    "email": "webshop-admin@paytonkawa.com",
    "password": "AdminPwForTest1234",
}
db_user = User.create_new_user(
    name=admin_user_data["name"],
    last_name=admin_user_data["last_name"],
    birth_date=admin_user_data["birth_date"],
    email=admin_user_data["email"],
    password=admin_user_data["password"],
)
# grant privileges
db_user.add_new_role("webshop-admin")
print("Done!")

# resellers
print("Populate DB with resellers ...")
for i in range(10):
    name = fake.first_name()
    last_name = fake.last_name()
    user_data = {
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=65),
        "name": name,
        "last_name": last_name,
        "email": name + "-" + last_name + "@paytonkawa.com",
        "password": "PwForTest1234",
    }
    db_user = User.create_new_user(
        name=user_data["name"],
        last_name=user_data["last_name"],
        birth_date=user_data["birth_date"],
        email=user_data["email"],
        password=user_data["password"],
    )
    # grant privileges
    db_user.add_new_role("reseller")
print("Done!")

# customers
print("Populate DB with customers ...")
for i in range(10):
    name = fake.first_name()
    last_name = fake.last_name()
    user_data = {
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=65),
        "name": name,
        "last_name": last_name,
        "email": name + "-" + last_name + "@mail.com",
        "password": "PwForTest1234",
    }
    db_user = User.create_new_user(
        name=user_data["name"],
        last_name=user_data["last_name"],
        birth_date=user_data["birth_date"],
        email=user_data["email"],
        password=user_data["password"],
    )
    # grant privileges
    db_user.add_new_role("webshop-client")
print("Done!")

# orders
print("Populate DB with orders ...")
# get customers
customers = UserRoles.get_users_by_role("webshop-client")
# get resellers
resellers = UserRoles.get_users_by_role("reseller")
# get all products
all_products = Product.select()

for i in customers:
    product = random.choice(all_products)
    product_price = product.price
    product_id = product.id
    order_quantity = fake.random_int(min=1, max=5)
    order_price = float(order_quantity) * float(product_price)
    order = Order(
        user=i,
        product=product_id,
        order_date=fake.date_time_between(
            start_date=datetime.datetime(2019, 3, 20, 7, 46, 39),
            end_date=datetime.datetime.now(),
        ),
        order_quantity=order_quantity,
        order_price=order_price,
    )
    order.save()

for i in resellers:
    product = random.choice(all_products)
    product_price = product.price
    product_id = product.id
    order_quantity = fake.random_int(min=50, max=1500)
    order_price = float(order_quantity) * float(product_price)
    order = Order(
        user=i.id,
        product=product_id,
        order_date=fake.date_time_between(
            start_date=datetime.datetime(2019, 3, 20, 7, 46, 39),
            end_date=datetime.datetime.now(),
        ),
        order_quantity=order_quantity,
        order_price=order_price,
    )
    order.save()
print("Done!")
