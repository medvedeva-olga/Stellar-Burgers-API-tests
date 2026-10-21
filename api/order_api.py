import allure

from api.base_api import BaseApi
from urls import ORDERS_ENDPOINT


class OrderApi(BaseApi):

    @allure.step('Создать заказ')
    def create_order(self, payload, token=None):
        headers = {'Authorization': token} if token else None
        return self.request(
            'POST', ORDERS_ENDPOINT, json=payload, headers=headers
        )

    @allure.step('Получить заказы пользователя')
    def get_user_orders(self, token=None):
        headers = {'Authorization': token} if token else None
        return self.request('GET', ORDERS_ENDPOINT, headers=headers)
