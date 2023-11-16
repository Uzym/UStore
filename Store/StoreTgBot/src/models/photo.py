from pydantic.v1 import BaseModel
from typing import List, Optional


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
