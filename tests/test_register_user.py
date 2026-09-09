import allure
import pytest
from helpers import generate_user_data
import messages 


class TestRegisterUser:

    @allure.title('Создание уникального пользователя возвращает ответ об успехе')
    def test_register_new_user_success(self, cleanup_user_data, user_api):
        payload = generate_user_data()
        response = user_api.register_user(payload)
        response_data = response.json()
        cleanup_user_data['accessToken'] = response_data['accessToken']

        assert response.status_code == 200
        assert response_data['success']== True
        assert response_data["user"]["email"] == payload["email"]
        assert response_data["user"]["name"] == payload["name"]   

    @allure.title('Создание пользователя, который уже существует, возвращает ошибку')
    def test_register_duplicate_user_returns_error(self, created_user, user_api):
        payload = {
            "email": created_user["email"],
            "password": created_user["password"],
            "name": created_user["name"]
        }
        response = user_api.register_user(payload)
        response_data = response.json()

        assert response.status_code == 403
        assert response_data["success"] is False 
        assert response_data["message"] == messages.USER_ALREADY_EXISTS_ERROR 

    @allure.title('Создание пользователя без обязательноего поля {missed_field} возвращает ошибку')
    @pytest.mark.parametrize('missed_field', ['email', 'password', 'name'])
    def test_register_user_without_required_field_returns_error(self, missed_field, user_api):
        payload = generate_user_data()
        payload.pop(missed_field)
        response = user_api.register_user(payload)
        response_data = response.json()

        assert response.status_code == 403
        assert response_data["success"] is False 
        assert response.json()["message"] == messages.USER_REGISTER_MISSING_FIELD_ERROR
       