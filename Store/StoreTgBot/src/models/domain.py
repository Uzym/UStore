from pydantic.v1 import BaseModel
from datetime import datetime
from typing import List, Optional


class Card(BaseModel):
    card_id: int
    title: str
    description: Optional[str] = None
    due: Optional[str] = None
    complete: Optional[str] = None
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


class Product(BaseModel):
    product_id: int
    category_id: int
    series_id: int
    title: str
    description: Optional[str] = None
    cost: float
    delivery_time: str
    discount: float

    def __str__(self):
        return (
            f"product_id: {self.product_id}\n"
            f"category_id: {self.category_id}\n"
            f"series_id: {self.series_id}\n"
            f"title: {self.title}\n"
            f"description: {self.description}\n"
            f"cost: {self.cost}\n"
            f"delivery_time: {self.delivery_time}\n"
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


class Series(BaseModel):
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


class User(BaseModel):
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


class Order(BaseModel):
    order_id: int
    user_id: int
    card_id: int
    finished: bool
    price: float

    def __str__(self):
        return (
            f"order_id: {self.order_id}\n"
            f"user_id: {self.user_id}\n"
            f"card_id: {self.card_id}\n"
            f"finished: {self.finished}\n"
            f"price: {self.price}\n"
        )
