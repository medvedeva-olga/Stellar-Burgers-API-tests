from uuid import uuid4

from faker import Faker


def generate_user_data():
    faker = Faker()
    name = faker.first_name()
    # uuid4 гарантирует уникальность email даже при параллельном запуске (pytest-xdist).
    unique_email = f"{name}_{uuid4().hex}@yandex.ru".lower()
    return {
        "email": unique_email,
        "password": faker.password(),
        "name": name
    }
