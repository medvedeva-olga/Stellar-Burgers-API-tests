import allure
import pytest
import messages
from models import CreateOrderResponseModel, ErrorResponseModel


class TestCreateOrder:

    @pytest.mark.smoke
    @allure.title("Создание заказа авторизованным пользователем с несколькими ингредиентами успешно")
    def test_create_order_with_authorization_with_ingredients_success(self, created_user, ingredients, order_api):
        payload = {
            "ingredients": ingredients
        }
        response = order_api.create_order(payload, created_user["accessToken"])
        created_order = CreateOrderResponseModel.model_validate(response.json())

        assert response.status_code == 200
        assert created_order.success is True
        assert created_order.name
        assert created_order.order.number > 0

    @allure.title("Создание заказа неавторизованным пользователем с несколькими ингредиентами успешно")
    def test_create_order_without_authorization_with_ingredients_success(self, ingredients, order_api):
        payload = {
            "ingredients": ingredients
        }
        response = order_api.create_order(payload)
        created_order = CreateOrderResponseModel.model_validate(response.json())

        assert response.status_code == 200
        assert created_order.success is True
        assert created_order.name
        assert created_order.order.number > 0

    @allure.title("Создание заказа авторизованным пользователем с пустым списком ингредиентов возвращает ошибку")
    def test_create_order_with_authorization_without_ingredients_returns_error(self, created_user, order_api):
        payload = {
            "ingredients": []
        }
        response = order_api.create_order(None, created_user["accessToken"])
        error = ErrorResponseModel.model_validate(response.json())

        assert response.status_code == 400
        assert error.success is False
        assert error.message == messages.ORDER_CREATE_NO_INGREDIENTS_ERROR

    @allure.title("Создание заказа авторизованным пользователем с невалидным хешом ингредиента возвращает ошибку")
    def test_create_order_with_authorization_with_invalid_ingredient_returns_error(self, created_user, ingredients, order_api):
        payload = {
            "ingredients" : ["x" + ingredients[0][1:]] 
        } 
        response = order_api.create_order(payload, created_user["accessToken"])

        assert response.status_code == 500
        assert "Internal Server Error" in response.text
 


