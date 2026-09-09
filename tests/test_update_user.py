import pytest
import allure
import messages
from helpers import generate_user_data


class TestUpdateUser:

    @allure.title('Обновление поля {field} пользователя с авторизацией возвращает ответ об успехе')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_update_user_field_with_authorization_success(self, created_user, field, user_api):
        access_token = created_user['accessToken']
        payload = {
            'email': created_user['email'],
            'password': created_user['password'],
            'name': created_user['name']
        } 
        payload[field] = generate_user_data()[field]
        response = user_api.update_user(payload, access_token)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["success"] is True       
        assert response_data["user"]["email"] == payload['email']
        assert response_data["user"]["name"] == payload['name'] 

    @allure.title('Обновление поля {field} пользователя без авторизации возвращает ошибку')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_update_user_field_with_authorization_returns_error(self, created_user, field, user_api):
        payload = {
            'email': created_user['email'],
            'password': created_user['password'],
            'name': created_user['name']
        } 
        payload[field] = generate_user_data()[field]
        response = user_api.update_user(payload)
        response_data = response.json()

        assert response.status_code == 401
        assert response_data["success"] is False       
        assert response_data['message'] == messages.USER_UPDATE_AUTHORIZATION_REQUIRED_ERROR

    @allure.title('Изменение почты пользователя на существующую возвращает сообщение об ошибке')
    def test_update_user_with_duplicate_email_returns_error(self, created_user, created_user_2, user_api):
        access_token = created_user['accessToken']
        payload = {
            'email': created_user_2['email']
        } 
        response = user_api.update_user(payload, access_token)
        response_data = response.json()

        assert response.status_code == 403
        assert response_data["success"] is False       
        assert response_data["message"] == messages.USER_UPDATE_DUPLICATE_EMAIL_ERROR 