from models.common import ApiModel


class CreatedOrderModel(ApiModel):
    number: int


class CreateOrderResponseModel(ApiModel):
    success: bool
    name: str
    order: CreatedOrderModel


class UserOrderModel(ApiModel):
    number: int
    ingredients: list[str]


class UserOrdersResponseModel(ApiModel):
    success: bool
    orders: list[UserOrderModel]
    total: int
    totalToday: int
