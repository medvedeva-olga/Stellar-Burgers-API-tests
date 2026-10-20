from models.common import ApiModel


class UserModel(ApiModel):
    email: str
    name: str


class AuthResponseModel(ApiModel):
    """Ответ на регистрацию или логин."""

    success: bool
    user: UserModel
    accessToken: str
    refreshToken: str


class UserResponseModel(ApiModel):
    """Ответ при получении или обновлении данных пользователя."""

    success: bool
    user: UserModel


class DeleteUserResponseModel(ApiModel):
    success: bool
    message: str
