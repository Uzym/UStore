from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class Card(BaseModel):
    card_id: int
    title: str
    description: Optional[str] = None
    due: Optional[datetime] = None
    complete: Optional[datetime] = None
    tags: List[str] = []
    created: datetime
    section_id: int

    def __str__(self):
        return (
            f"card_id: {self.card_id}\n"
            f"title: {self.title}\n"
            f"description: {self.description}\n"
            f"due: {self.due}\n"
            f"complete: {self.complete}\n"
            f"tags: {self.tags}\n"
            f"created: {self.created}\n"
            f"section_id: {self.section_id}\n"
        )


class Category(BaseModel):
    category_id: int
    title: str
    description: Optional[str] = None
    discount: float

    def __str__(self):
        return (
            f"category_id: {self.category_id}\n"
            f"title: {self.title}\n"
            f"description: {self.description}\n"
            f"discount: {self.discount}\n"
        )


class Firm(BaseModel):
    firm_id: int
    title: str
    description: Optional[str] = None
    discount: float

    def __str__(self):
        return (
            f"firm_id: {self.firm_id}\n"
            f"title: {self.title}\n"
            f"description: {self.description}\n"
            f"discount: {self.discount}\n"
        )


class Link(BaseModel):
    href: Optional[str] = None
    rel: Optional[str] = None
    method: Optional[str] = None

    def __str__(self):
        return (
            f"href: {self.href}\n"
            f"rel: {self.rel}\n"
            f"method: {self.method}\n"
        )


# TODO: перенести в Order model
class OrderProduct(BaseModel):
    product_id: int
    quantity: int

    def __str__(self):
        return (
            f"product_id: {self.product_id}\n"
            f"quantity: {self.quantity}\n"
        )


class Photo(BaseModel):
    photo_id: int
    name: str
    product_id: Optional[int] = None
    category_id: Optional[int] = None
    series_id: Optional[int] = None
    firm_id: Optional[int] = None

    def __str__(self):
        return (
            f"photo_id: {self.photo_id}\n"
            f"name: {self.name}\n"
            f"product_id: {self.product_id}\n"
            f"category_id: {self.category_id}\n"
            f"series_id: {self.series_id}\n"
            f"firm_id: {self.firm_id}\n"
        )


# TODO перенести в соответствующие классы
class RequestCreateCategory(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    discount: Optional[float] = None

    def __str__(self):
        return (
            f"title: {self.title}\n"
            f"description: {self.description}\n"
            f"discount: {self.discount}\n"
        )


class RequestCreateFirm(BaseModel):
    title: str
    description: Optional[str] = None
    discount: Optional[float] = None

    def __str__(self):
        return (
            f"title: {self.title}\n"
            f"description: {self.description}\n"
            f"discount: {self.discount}\n"
        )


class RequestCreateOrder(BaseModel):
    user_id: int
    card_id: Optional[int] = None
    finished: Optional[bool] = None
    price: Optional[float] = None

    def __str__(self):
        return (
            f"user_id: {self.user_id}\n"
            f"card_id: {self.card_id}\n"
            f"finished: {self.finished}\n"
            f"price: {self.price}\n"
        )


class RequestCreatePhoto(BaseModel):
    name: str
    product_id: Optional[int] = None
    category_id: Optional[int] = None
    series_id: Optional[int] = None
    firm_id: Optional[int] = None

    def __str__(self):
        return (
            f"name: {self.name}\n"
            f"product_id: {self.product_id}\n"
            f"category_id: {self.category_id}\n"
            f"series_id: {self.series_id}\n"
            f"firm_id: {self.firm_id}\n"
        )


class RequestCreateProduct(BaseModel):
    category_id: int
    series_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[float] = None
    delivery_time: Optional[str] = None
    discount: Optional[float] = None

    def __str__(self):
        return (
            f"category_id: {self.category_id}\n"
            f"series_id: {self.series_id}\n"
            f"title: {self.title}\n"
            f"description: {self.description}\n"
            f"cost: {self.cost}\n"
            f"delivery_time: {self.delivery_time}\n"
            f"discount: {self.discount}\n"
        )


class RequestCreateSeries(BaseModel):
    title: str
    description: Optional[str] = None
    discount: Optional[float] = None
    firm_id: Optional[int] = None

    def __str__(self):
        return (
            f"title: {self.title}\n"
            f"description: {self.description}\n"
            f"discount: {self.discount}\n"
            f"firm_id: {self.firm_id}\n"
        )


class RequestCreateUser(BaseModel):
    tg_id: str
    name: Optional[str] = None
    address: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    tg_ref: Optional[str] = None
    admin: Optional[bool] = None

    def __str__(self):
        return (
            f"tg_id: {self.tg_id}\n"
            f"name: {self.name}\n"
            f"address: {self.address}\n"    # TODO: заменить везде adress на address
            f"telephone: {self.telephone}\n"
            f"email: {self.email}\n"
            f"tg_ref: {self.tg_ref}\n"
            f"admin: {self.admin}\n"
        )


class CardDto(BaseModel):
    card_id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    due: Optional[str]
    complete: Optional[str]
    tags: Optional[List[str]]
    created: Optional[str]
    section_id: Optional[int]

    def __str__(self):
        pass


class ResponseGetCardDto(BaseModel):
    card: CardDto
    links: List[Link]

    def __str__(self):
        pass


class SeriesDto(BaseModel):
    series_id: int
    title: str
    description: Optional[str] = None
    discount: Optional[float] = None
    firm_id: Optional[int] = None

    def __str__(self):
        return (
            f"series_id: {self.series_id}\n"
            f"title: {self.title}\n"
            f"description: {self.description}\n"
            f"discount: {self.discount}\n"
            f"firm_id: {self.firm_id}\n"
        )


class UserDto(BaseModel):
    user_id: int
    tg_id: Optional[str] = None
    name: str
    adress: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    tg_ref: Optional[str] = None
    admin: Optional[bool] = None

    def __str__(self):
        return (
            f"user_id: {self.user_id}\n"
            f"tg_id: {self.tg_id}\n"
            f"name: {self.name}\n"
            f"adress: {self.adress}\n"
            f"telephone: {self.telephone}\n"
            f"email: {self.email}\n"
            f"tg_ref: {self.tg_ref}\n"
            f"admin: {self.admin}\n"
        )