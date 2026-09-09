import allure
import messages

class TestGetUserOrders:

    @allure.title('Получение заказов пользователя возвращает список его заказов')
    def test_get_user_orders_returns_orders(self, created_user, created_user_orders, order_api):
        response = order_api.get_user_orders(created_user["accessToken"])
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["success"] is True
        assert "orders" in response_data
        assert len(response_data["orders"]) == len(created_user_orders)
        for i, order in enumerate(created_user_orders):
            assert response_data["orders"][i]["ingredients"] == order["ingredients"]
            assert response_data["orders"][i]["number"] == order["number"]
        assert "total" in response_data
        assert "totalToday" in response_data

    @allure.title('Получение заказов пользователя без токена авторизации возвращает ошибку')
    def test_get_user_orders_without_authorization_returns_error(self, order_api):
        response = order_api.get_user_orders()
        response_data = response.json()

        assert response.status_code == 401
        assert response_data["success"] is False
        assert (response_data["message"]) == messages.USER_ORDERS_GET_AUTHORIZATION_REQUIRED_ERROR
