import allure
import pytest
import messages
from models import ErrorResponseModel, UserOrdersResponseModel

class TestGetUserOrders:

    @pytest.mark.smoke
    @allure.title('Получение заказов пользователя возвращает список его заказов')
    def test_get_user_orders_returns_orders(self, created_user, created_user_orders, order_api):
        response = order_api.get_user_orders(created_user["accessToken"])
        orders_response = UserOrdersResponseModel.model_validate(response.json())

        assert response.status_code == 200
        assert orders_response.success is True
        assert len(orders_response.orders) == len(created_user_orders)
        for i, order in enumerate(created_user_orders):
            assert orders_response.orders[i].ingredients == order["ingredients"]
            assert orders_response.orders[i].number == order["number"]

    @allure.title('Получение заказов пользователя без токена авторизации возвращает ошибку')
    def test_get_user_orders_without_authorization_returns_error(self, order_api):
        response = order_api.get_user_orders()
        error = ErrorResponseModel.model_validate(response.json())

        assert response.status_code == 401
        assert error.success is False
        assert error.message == messages.USER_ORDERS_GET_AUTHORIZATION_REQUIRED_ERROR
