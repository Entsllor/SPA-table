import datetime
from decimal import Decimal

from pydantic import BaseModel


class TableRowCreate(BaseModel):
    name: str
    date: datetime.date
    distance: Decimal
    quantity: int

    class Config:
        orm_mode = True


class TableRow(TableRowCreate):
    id: int
