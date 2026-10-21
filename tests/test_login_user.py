import pytest
import allure
import messages
from models import AuthResponseModel, ErrorResponseModel


class TestLoginUser:

    @pytest.mark.smoke
    @allure.title('Авторизация существующего пользователя возвращает ответ об успехе')
    def test_login_registered_user_success(self, created_user, user_api):
        email = created_user["email"]
        password = created_user["password"]
        name = created_user["name"]
        payload = {
            "email": email,
            "password": password
        }
        response = user_api.login_user(payload)
        auth = AuthResponseModel.model_validate(response.json())

        assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}: {response.text}"
        assert auth.success is True, "Флаг success не равен True"
        assert auth.accessToken, "В ответе отсутствует accessToken"
        assert auth.user.email == email, "В ответе неверный email"
        assert auth.user.name == name, "В ответе неверный name"

    @allure.title('Авторизация пользователя с неверным полем {incorrect_field} возвращает ошибку')
    @pytest.mark.parametrize('incorrect_field', ['email', 'password'])
    def test_login_user_with_incorrect_field_returns_401(self, created_user, incorrect_field, user_api):
        payload = {
            "email": created_user["email"],
            "password": created_user["password"]
        }
        payload[incorrect_field] += "a"
        response = user_api.login_user(payload)
        error = ErrorResponseModel.model_validate(response.json())

        assert response.status_code == 401, \
            f"Ожидался статус 401, получен {response.status_code}: {response.text}"
        assert error.success is False, "Флаг success не равен False"
        assert error.message == messages.USER_LOGIN_INCORRECT_FIELD_ERROR, \
            "Неверное сообщение об ошибке"
