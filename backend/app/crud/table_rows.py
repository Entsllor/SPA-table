from app import models
from .base import BaseCrudDB, create_instance
from datetime import datetime


class TableRowsCRUD(BaseCrudDB):
    model = models.TableRow

    async def create(self, name: str, quantity: int, distance: str, date: datetime = None) -> models.TableRow:
        table_row = self.model(name=name, date=date, quantity=quantity, distance=distance)
        return await create_instance(table_row)


TableRows = TableRowsCRUD()
