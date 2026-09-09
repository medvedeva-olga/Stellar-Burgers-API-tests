import allure
import messages


class TestCreateOrder:

    @allure.title("Создание заказа авторизованным пользователем с несколькими ингредиентами успешно")
    def test_create_order_with_authorization_with_ingredients_success(self, created_user, ingredients, order_api):
        payload = {
            "ingredients": ingredients
        }
        response = order_api.create_order(payload, created_user["accessToken"])
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["success"] is True
        assert "name" in response_data
        assert "order" in response_data
        assert "number" in response_data["order"]
        assert isinstance(response_data["order"]["number"], int)
        assert response_data["order"]["number"] > 0

    @allure.title("Создание заказа неавторизованным пользователем с несколькими ингредиентами успешно")
    def test_create_order_without_authorization_with_ingredients_success(self, ingredients, order_api):
        payload = {
            "ingredients": ingredients
        }
        response = order_api.create_order(payload)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["success"] is True
        assert "name" in response_data
        assert "order" in response_data
        assert "number" in response_data["order"]
        assert isinstance(response_data["order"]["number"], int)
        assert response_data["order"]["number"] > 0

    @allure.title("Создание заказа авторизованным пользователем с пустым списком ингредиентов возвращает ошибку")
    def test_create_order_with_authorization_without_ingredients_returns_error(self, created_user, order_api):
        payload = {
            "ingredients": []
        }
        response = order_api.create_order(None, created_user["accessToken"])
        response_data = response.json()

        assert response.status_code == 400
        assert response_data["success"] is False
        assert response_data["message"] == messages.ORDER_CREATE_NO_INGREDIENTS_ERROR

    @allure.title("Создание заказа авторизованным пользователем с невалидным хешом ингредиента возвращает ошибку")
    def test_create_order_with_authorization_with_invalid_ingredient_returns_error(self, created_user, ingredients, order_api):
        payload = {
            "ingredients" : ["x" + ingredients[0][1:]] 
        } 
        response = order_api.create_order(payload, created_user["accessToken"])

        assert response.status_code == 500
        assert "Internal Server Error" in response.text
 


