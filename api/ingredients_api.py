import allure

from api.base_api import BaseApi
from urls import INGREDIENTS_ENDPOINT


class IngredientApi(BaseApi):

    @allure.step('Получить список ингредиентов')
    def get_ingredients(self):
        return self.request('GET', INGREDIENTS_ENDPOINT)
