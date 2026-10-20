import os

import allure
import requests

# Публичный API, доступный из любой сети (в т.ч. из GitHub Actions).
# Базовый адрес можно переопределить переменной окружения PUBLIC_API_BASE_URL.
BASE_URL = os.getenv("PUBLIC_API_BASE_URL", "https://jsonplaceholder.typicode.com")


class JsonPlaceholderApi:
    """Клиент для публичного API jsonplaceholder.typicode.com."""

    @allure.step('Получить пост по id')
    def get_post(self, post_id):
        return requests.get(f"{BASE_URL}/posts/{post_id}")

    @allure.step('Создать пост')
    def create_post(self, payload):
        return requests.post(f"{BASE_URL}/posts", json=payload)
