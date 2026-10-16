import allure
import pytest


class TestPublicApi:

    @pytest.mark.ci
    @allure.title('Получение поста из публичного API возвращает корректную схему ответа')
    def test_get_post_returns_post_with_expected_schema(self, public_api):
        # Given: в публичном API существует пост с id = 1

        # When: клиент запрашивает пост по id
        response = public_api.get_post(1)
        response_data = response.json()

        # Then: приходит 200 и пост с обязательными полями
        assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}: {response.text}"
        assert response.headers["Content-Type"].startswith("application/json"), \
            "Неверный Content-Type ответа"
        assert {"userId", "id", "title", "body"} <= set(response_data), \
            f"В ответе не хватает обязательных полей: {response_data}"
        assert response_data["id"] == 1, "В ответе неверный id поста"
        assert isinstance(response_data["title"], str) and response_data["title"], \
            "Поле title пустое или не строка"

    @pytest.mark.ci
    @allure.title('Создание поста в публичном API возвращает 201 и данные поста')
    def test_create_post_returns_created_post(self, public_api):
        # Given: подготовлены данные нового поста
        payload = {
            "title": "Stellar Burgers",
            "body": "Проверка публичного API из CI",
            "userId": 1,
        }

        # When: клиент создаёт пост
        response = public_api.create_post(payload)
        response_data = response.json()

        # Then: приходит 201 и данные созданного поста
        assert response.status_code == 201, \
            f"Ожидался статус 201, получен {response.status_code}: {response.text}"
        assert response.headers["Content-Type"].startswith("application/json"), \
            "Неверный Content-Type ответа"
        assert response_data["title"] == payload["title"], "В ответе неверный title"
        assert response_data["body"] == payload["body"], "В ответе неверный body"
        assert response_data["userId"] == payload["userId"], "В ответе неверный userId"
        assert "id" in response_data, "В ответе отсутствует id созданного поста"
