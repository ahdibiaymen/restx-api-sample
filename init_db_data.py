from faker import Faker

from erp.models import Product, User

fake = Faker()

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
