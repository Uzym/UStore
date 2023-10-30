from pydantic import BaseModel
from typing import List, Optional


class OrderProduct(BaseModel):
    order_id: int
    product_id: int
    quantity: int

    def __str__(self):
        return (
            f"product_id: {self.product_id}\n"
            f"quantity: {self.quantity}\n"
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
