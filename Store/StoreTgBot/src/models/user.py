from pydantic.v1 import BaseModel
from typing import List, Optional


class RequestCreateUser(BaseModel):
    tg_id: str
    name: Optional[str] = None
    adress: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    tg_ref: Optional[str] = None
    admin: Optional[bool] = None

    def __str__(self):
        return (
            f"tg_id: {self.tg_id}\n"
            f"name: {self.name}\n"
            f"adress: {self.adress}\n"    # TODO: заменить везде adress на address
            f"telephone: {self.telephone}\n"
            f"email: {self.email}\n"
            f"tg_ref: {self.tg_ref}\n"
            f"admin: {self.admin}\n"
        )