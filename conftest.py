from api.user_api import UserApi
from api.order_api import OrderApi
from api.ingredients_api import IngredientApi
from helpers import generate_user_data
import pytest 

@pytest.fixture(scope='session')
def user_api():
    return UserApi()

@pytest.fixture(scope='session')
def order_api():
    return OrderApi()

@pytest.fixture(scope='session')
def ingredients_api():
    return IngredientApi()

@pytest.fixture
def cleanup_user_data(user_api):
    user_data = {"accessToken": None}
    
    yield user_data

    access_token = user_data.get('accessToken')
    if access_token:
        user_api.delete_user(access_token)
 
@pytest.fixture
def created_user(user_api):
    user_data = generate_user_data()
    response = user_api.register_user(user_data)
    access_token = response.json().get("accessToken")

    yield {
        "email": user_data['email'],
        "password": user_data['password'],
        "name": user_data['name'],
        "accessToken": access_token,
        "response": response     
    }

    if access_token:
        user_api.delete_user(access_token)

@pytest.fixture
def created_user_2(user_api):
    user_data = generate_user_data()
    response = user_api.register_user(user_data)
    access_token = response.json().get("accessToken")

    yield {
        "email": user_data['email'],
        "password": user_data['password'],
        "name": user_data['name'],
        "accessToken": access_token,
        "response": response     
    }

    if access_token:
        user_api.delete_user(access_token)

@pytest.fixture
def created_user_orders(created_user, ingredients, order_api):
    access_token = created_user["accessToken"]
    orders = [
        {"ingredients": [ingredients[0]]}, 
        {"ingredients": [ingredients[1], ingredients[2]]}
    ]
    for order_data in orders:
        response = order_api.create_order(order_data, access_token)
        order_data["number"] = response.json()["order"]["number"]
    return orders

@pytest.fixture
def ingredients(ingredients_api):
    response = ingredients_api.get_ingredients()
    return [ingredient['_id'] for ingredient in response.json()['data'][:3]]


