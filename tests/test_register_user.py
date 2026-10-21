import allure
import pytest
from helpers import generate_user_data
import messages 
from models import AuthResponseModel, ErrorResponseModel


class TestRegisterUser:

    @pytest.mark.smoke
    @allure.title('Регистрация нового пользователя возвращает 200 и токен доступа')
    def test_register_new_user_returns_access_token(self, cleanup_user_data, user_api):
        payload = generate_user_data()
        response = user_api.register_user(payload)
        auth = AuthResponseModel.model_validate(response.json())
        cleanup_user_data['accessToken'] = auth.accessToken

        assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}: {response.text}"
        assert auth.success is True, "Флаг success не равен True"
        assert auth.accessToken, "В ответе отсутствует accessToken"
        assert auth.user.email == payload["email"], "В ответе неверный email"
        assert auth.user.name == payload["name"], "В ответе неверное имя пользователя"

    @allure.title('Регистрация пользователя с существующим email возвращает 403')
    def test_register_duplicate_user_returns_error(self, created_user, user_api):
        payload = {
            "email": created_user["email"],
            "password": created_user["password"],
            "name": created_user["name"]
        }
        response = user_api.register_user(payload)
        error = ErrorResponseModel.model_validate(response.json())

        assert response.status_code == 403, \
            f"Ожидался статус 403, получен {response.status_code}: {response.text}"
        assert error.success is False, "Флаг success не равен False"
        assert error.message == messages.USER_ALREADY_EXISTS_ERROR, "Неверное сообщение об ошибке"

    @allure.title('Регистрация пользователя без обязательноего поля {missed_field} возвращает ошибку')
    @pytest.mark.parametrize('missed_field', ['email', 'password', 'name'])
    def test_register_user_without_required_field_returns_error(self, missed_field, user_api):
        payload = generate_user_data()
        payload.pop(missed_field)
        response = user_api.register_user(payload)
        error = ErrorResponseModel.model_validate(response.json())

        assert response.status_code == 403, \
            f"Ожидался статус 403, получен {response.status_code}: {response.text}"
        assert error.success is False, "Флаг success не равен False"
        assert error.message == messages.USER_REGISTER_MISSING_FIELD_ERROR, \
            "Неверное сообщение об ошибке"
       