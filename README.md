# API-тестирование Stellar Burgers

## Описание
Автоматизированные API-тесты для учебного сервиса [Stellar Burgers](https://stellarburgers.education-services.ru).

Тестируемая функциональность:
- регистрация, авторизация, изменение и удаление пользователя;
- создание и получение заказов;
- работа с ингредиентами.

## Стек технологий
- Python 3.11+ (проект локально на 3.14)
- pytest 9.0
- requests 2.34
- allure-pytest 2.16
- Faker 40.28

## Структура проекта
```
├── api/              # клиенты API
├── tests/            # тесты по функционалу
├── conftest.py       # фикстуры
├── helpers.py        # вспомогательные функции
├── messages.py       # сообщения об ошибках
├── urls.py           # эндпоинты
└── requirements.txt  # зависимости
```

## Установка зависимостей
```bash
pip install -r requirements.txt
```

## Запуск тестов
Запуск всех тестов:
```bash
pytest -v --no-cov
```

Запуск конкретного файла:
```bash
pytest tests/test_login_user.py -v --no-cov
```

Запуск с маркером (при наличии):
```bash
pytest -m smoke -v --no-cov
```

## Отчёт Allure
Сбор результатов:
```bash
pytest tests/ --alluredir=allure_results --no-cov
```

Просмотр отчёта локально:
```bash
allure serve allure_results
```

## CI/CD
В репозитории настроен GitHub Actions (`.github/workflows/api-tests.yml`), который автоматически запускает API-тесты при `push` и `pull_request` в ветки `main`, `develop`, `develop2`.

### Просмотр отчётов после прогона

**1. GitHub Pages (HTML-отчёт онлайн)**

После каждого `push` workflow генерирует HTML-отчёт Allure и публикует его на GitHub Pages.
Ссылка:

```
https://medvedeva-olga.github.io/Stellar-Burgers-API-tests/
```

Чтобы отчёт начал публиковаться, нужно **один раз** включить Pages:
`Settings → Pages → Build and deployment → Source: GitHub Actions`.

**2. Скачать артефакт**

На вкладке **Actions** → нужный запуск → блок **Artifacts** →
скачать `allure-results.zip` (сырые результаты) или `allure-report.zip` (готовый HTML-отчёт).

Локальный просмотр сырых результатов:

```bash
allure serve allure_results
```

## Реализованные автотесты

### Регистрация пользователя
- `test_register_new_user_success` — создание уникального пользователя
- `test_register_duplicate_user_returns_error` — нельзя создать пользователя, который уже зарегистрирован
- `test_register_user_without_required_field_returns_error` — нельзя создать пользователя без обязательного поля

### Авторизация пользователя
- `test_login_registered_user_success` — успешный логин зарегистрированного пользователя
- `test_login_user_with_incorrect_field_returns_401` — ошибка при неверных логине/пароле

### Изменение данных пользователя
- `test_update_user_field_with_authorization_success` — обновление данных с авторизацией
- `test_update_user_field_without_authorization_returns_401` — обновление без авторизации возвращает 401
- `test_update_user_with_duplicate_email_returns_403` — нельзя изменить email на уже занятый

### Получение данных пользователя
- `test_get_user_with_authorization_success` — получение данных пользователя с авторизацией
- `test_get_user_without_authorization_returns_401` — получение данных без авторизации

### Создание заказа
- `test_create_order_with_authorization_with_ingredients_success` — создание заказа с авторизацией и ингредиентами
- `test_create_order_without_authorization_with_ingredients_success` — создание заказа без авторизации с ингредиентами
- `test_create_order_with_authorization_without_ingredients_returns_400` — создание заказа без ингредиентов
- `test_create_order_with_authorization_with_invalid_ingredient_returns_500` — создание заказа с невалидным хешем ингредиента

### Получение заказов пользователя
- `test_get_user_orders_with_authorization_returns_orders` — получение заказов авторизованного пользователя
- `test_get_user_orders_without_authorization_returns_401` — получение заказов без авторизации

### Удаление пользователя
- `test_delete_user_without_token_returns_401` — удаление без токена
- `test_delete_user_with_token_returns_202` — успешное удаление пользователя
