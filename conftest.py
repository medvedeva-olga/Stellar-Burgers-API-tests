import platform

import allure
import pydantic
import pytest
import requests

from api.ingredients_api import IngredientApi
from api.jsonplaceholder_api import JsonPlaceholderApi
from api.order_api import OrderApi
from api.transport import HTTPLogBuffer
from api.user_api import UserApi
from helpers import generate_user_data
from urls import BASE_URL


def pytest_report_header(config):
    return [
        f'Стенд: {BASE_URL}',
        (
            f'Python {platform.python_version()}, pytest {pytest.__version__}, '
            f'requests {requests.__version__}, pydantic {pydantic.VERSION}'
        ),
    ]


@pytest.fixture
def http_log_buffer(request):
    buffer = HTTPLogBuffer()
    request.node.http_buffer = buffer
    yield buffer


@pytest.fixture
def user_api(http_log_buffer):
    return UserApi(http_log_buffer)


@pytest.fixture
def order_api(http_log_buffer):
    return OrderApi(http_log_buffer)


@pytest.fixture
def ingredients_api(http_log_buffer):
    return IngredientApi(http_log_buffer)


@pytest.fixture
def public_api(http_log_buffer):
    return JsonPlaceholderApi(http_log_buffer)


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


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield

    if report.failed and not getattr(item, '_http_dump_attached', False):
        buffer = getattr(item, 'http_buffer', None)
        if buffer and buffer.logs:
            item._http_dump_attached = True
            full_log = buffer.get_full_log()
            print('\n--- [FAILED TEST HTTP DUMP] ---')
            print(full_log)
            allure.attach(
                full_log,
                name='HTTP Request/Response Dump',
                attachment_type=allure.attachment_type.TEXT,
            )
    elif report.when == 'call' and report.passed:
        reporter = item.config.pluginmanager.get_plugin('terminalreporter')
        if reporter:
            reporter.write_line('INFO     Test passed')

    return report
