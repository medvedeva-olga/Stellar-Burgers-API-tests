import pytest
import allure
import messages


class TestLoginUser:

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
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["success"] is True
        assert "accessToken" in response_data         
        assert response_data["user"]["email"] == email
        assert response_data["user"]["name"] == name 

    @allure.title('Авторизация пользователя с неверным полем {incorrect_field} возвращает ошибку')
    @pytest.mark.parametrize('incorrect_field', ['email', 'password'])
    def test_login_user_with_incorrect_field_returns_error(self, created_user, incorrect_field, user_api):
        payload = {
            "email": created_user["email"],
            "password": created_user["password"]
        }
        payload[incorrect_field] += "a"
        response = user_api.login_user(payload)
        response_data = response.json()

        assert response.status_code == 401
        assert response_data["success"] is False       
        assert response_data["message"] == messages.USER_LOGIN_INCORRECT_FIELD_ERROR
