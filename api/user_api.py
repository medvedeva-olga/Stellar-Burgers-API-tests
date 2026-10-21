import allure

from api.base_api import BaseApi
from urls import (
    LOGIN_USER_ENDPOINT,
    LOGOUT_USER_ENDPOINT,
    REGISTER_USER_ENDPOINT,
    USER_ENDPOINT,
)


class UserApi(BaseApi):

    @allure.step('Создать пользователя')
    def register_user(self, payload):
        return self.request('POST', REGISTER_USER_ENDPOINT, json=payload)

    @allure.step('Логин пользователя')
    def login_user(self, payload):
        return self.request('POST', LOGIN_USER_ENDPOINT, json=payload)

    @allure.step('Выход пользователя из системы')
    def logout_user(self, payload):
        return self.request('POST', LOGOUT_USER_ENDPOINT, json=payload)

    @allure.step('Получить данные пользователя')
    def get_user(self, token):
        headers = {'Authorization': token} if token else None
        return self.request('GET', USER_ENDPOINT, headers=headers)

    @allure.step('Обновить данные пользователя')
    def update_user(self, payload, token=None):
        headers = {'Authorization': token} if token else None
        return self.request(
            'PATCH', USER_ENDPOINT, json=payload, headers=headers
        )

    @allure.step('Удалить пользователя')
    def delete_user(self, token):
        headers = {'Authorization': token} if token else None
        return self.request('DELETE', USER_ENDPOINT, headers=headers)
