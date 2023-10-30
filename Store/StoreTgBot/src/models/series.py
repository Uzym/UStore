from pydantic import BaseModel
from typing import List, Optional


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