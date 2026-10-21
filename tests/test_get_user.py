import pytest
import allure
import messages
from models import ErrorResponseModel, UserResponseModel


class TestGetUser:

    @pytest.mark.smoke
    @allure.title("Получение данных пользователя по токену возвращает 200")
    def test_get_user_with_token_returns_user_data(self, user_api, created_user):
        response = user_api.get_user(created_user["accessToken"])
        user_response = UserResponseModel.model_validate(response.json())

        assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}: {response.text}"
        assert user_response.success is True, "Флаг success не равен True"
        assert user_response.user.email == created_user["email"], "В ответе неверный email"
        assert user_response.user.name == created_user["name"], "В ответе неверное имя"

    @allure.title("Получение данных пользователя без токена возвращает 401")
    def test_get_user_without_token_returns_401(self, user_api):
        response = user_api.get_user(None)
        error = ErrorResponseModel.model_validate(response.json())

        assert response.status_code == 401, \
            f"Ожидался статус 401, получен {response.status_code}: {response.text}"
        assert error.message == messages.USER_GET_AUTHORIZATION_REQUIRED_ERROR, \
            "Неверное сообщение об ошибке"

