from pydantic import ConfigDict, Field

from models.common import ApiModel


class IngredientModel(ApiModel):
    model_config = ConfigDict(extra="ignore", validate_by_name=True,  validate_by_alias=True)

    id: str = Field(alias="_id")
    name: str
    type: str
    proteins: int
    fat: int
    carbohydrates: int
    calories: int
    price: int
    image: str


class IngredientsResponseModel(ApiModel):
    success: bool
    data: list[IngredientModel]
