from pydantic import BaseModel, ConfigDict


class ApiModel(BaseModel):
    """Базовая модель ответа API: лишние поля в ответе игнорируются."""

    model_config = ConfigDict(extra="ignore")


class ErrorResponseModel(ApiModel):
    success: bool
    message: str
