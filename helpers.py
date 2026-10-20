from faker import Faker
from datetime import datetime

def generate_user_data():
    faker = Faker()
    timestamp = int(datetime.now().timestamp() * 1000)
    name = faker.first_name()
    unique_email = (f"{name}_{timestamp}@yandex.ru").lower()   
    return {
        "email": unique_email,
        "password": faker.password(),
        "name": name
        }