import requests
import allure
from urls import REGISTER_USER_ENDPOINT, LOGIN_USER_ENDPOINT, LOGOUT_USER_ENDPOINT, USER_ENDPOINT

class UserApi:

    @allure.step('Создать пользователя')
    def register_user(self, payload):
        return requests.post(REGISTER_USER_ENDPOINT, json=payload)

    @allure.step('Логин пользователя')
    def login_user(self, payload):
        return requests.post(LOGIN_USER_ENDPOINT, json=payload)

    @allure.step('Выход пользователя из системы')
    def logout_user(self, payload):
        return requests.post(LOGOUT_USER_ENDPOINT, json=payload)

    @allure.step('Получить данные пользователя')    
    def get_user_data(self, token):
        headers = {"Authorization": token}   
        return requests.get(USER_ENDPOINT, headers=headers)
    
    @allure.step('Обновить данные пользователя')
    def update_user(self, payload, token=None):
        headers = {"Authorization": token} if token else None
        return requests.patch(USER_ENDPOINT, json=payload, headers=headers)

    @allure.step('Удалить пользователя')
    def delete_user(self, token):
        headers = {"Authorization": token}   
        return requests.delete(USER_ENDPOINT, headers=headers)
