from utils import mongo_client, hash_password
import secrets

initial_products = [
    {"name": "Pencil", "price": 1.50, "inventory": 35},
    {"name": "Pen", "price": 10.00, "inventory": 30},
    {"name": "Scale", "price": 15.00, "inventory": 20},
]

mongo_client.db.products.insert_many(initial_products)

# we shouldn't put any credentials here but we since this is just for dev
# login as admin using username test_user and password Test_password1
TEST_SALT = secrets.token_hex(16)
TEST_USER = {
    "email": "test_user",
    "salt": TEST_SALT,
    "password": hash_password("Test_password1", TEST_SALT),
    "role": "Admin",
}

mongo_client.db.users.insert_one(TEST_USER)
