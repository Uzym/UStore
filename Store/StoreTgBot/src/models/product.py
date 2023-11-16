from pydantic.v1 import BaseModel
from typing import List, Optional


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


