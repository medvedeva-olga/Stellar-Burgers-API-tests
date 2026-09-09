import requests
import allure
from urls import ORDERS_ENDPOINT


class OrderApi:

    @allure.step('Создать заказ')
    def create_order(self, payload, token = None):
        headers = {"Authorization": token} if token else None
        return requests.post(ORDERS_ENDPOINT, json=payload, headers=headers)

    @allure.step('Получить заказы пользователя')
    def get_user_orders(self, token = None):
        headers = {"Authorization": token} if token else None
        return requests.get(ORDERS_ENDPOINT, headers=headers)