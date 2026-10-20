import requests
import allure
from urls import INGREDIENTS_ENDPOINT


class IngredientApi:

    @allure.step('Получить список ингредиентов')
    def get_ingredients(self):
        return requests.get(INGREDIENTS_ENDPOINT)