import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


def get_optional_schema(base_model_class):
    return {k: Optional[v] for k, v in base_model_class.__annotations__.items()}


class TableRowCreate(BaseModel):
    name: str
    date: datetime.date = None
    distance: Decimal
    quantity: int

    class Config:
        orm_mode = True


class TableRowUpdate(TableRowCreate):
    __annotations__ = get_optional_schema(TableRowCreate)


class TableRow(TableRowCreate):
    id: int
