import pytest
import allure
import messages
from models import DeleteUserResponseModel, ErrorResponseModel


class TestDeleteUser:

    @allure.title("Удаление пользователя без токена возвращает 401")
    def test_delete_user_without_token_returns_401(self, user_api):
        response = user_api.delete_user("")
        error = ErrorResponseModel.model_validate(response.json())

        assert response.status_code == 401, \
            f"Ожидался статус 401, получен {response.status_code}: {response.text}"
        assert error.message == messages.USER_DELETE_AUTHORIZATION_REQUIRED_ERROR, \
            "Неверное сообщение об ошибке"

    @allure.title("Удаление пользователя с валидным токеном возвращает 202")
    def test_delete_user_with_token_returns_202(self, user_api, created_user):
        response = user_api.delete_user(created_user["accessToken"])
        deleted = DeleteUserResponseModel.model_validate(response.json())

        assert response.status_code == 202, \
            f"Ожидался статус 202, получен {response.status_code}: {response.text}"
        assert deleted.success is True, "Флаг success не равен True"
        assert user_api.get_user(created_user["accessToken"]).status_code == 404, \
            "Удалённый пользователь всё ещё доступен по токену"