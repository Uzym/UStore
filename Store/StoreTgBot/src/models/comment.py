from pydantic.v1 import BaseModel


class RequestCreateCommentDto(BaseModel):
    description: str
