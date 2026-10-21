import os

import allure

from api.base_api import BaseApi

# Публичный API, доступный из любой сети (в т.ч. из GitHub Actions).
# Базовый адрес можно переопределить переменной окружения PUBLIC_API_BASE_URL.
BASE_URL = os.getenv("PUBLIC_API_BASE_URL", "https://jsonplaceholder.typicode.com")


class JsonPlaceholderApi(BaseApi):
    """Клиент для публичного API jsonplaceholder.typicode.com."""

    def __init__(self, log_buffer, base_url=None):
        super().__init__(log_buffer)
        self.base_url = (base_url or BASE_URL).rstrip('/')

    @allure.step('Получить пост по id')
    def get_post(self, post_id):
        return self.request('GET', f"{self.base_url}/posts/{post_id}")

    @allure.step('Создать пост')
    def create_post(self, payload):
        return self.request('POST', f"{self.base_url}/posts", json=payload)
