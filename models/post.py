from models.common import ApiModel


class PostModel(ApiModel):
    userId: int
    id: int
    title: str
    body: str
