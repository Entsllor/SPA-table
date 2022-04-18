from app import models
from .base import BaseCrudDB, create_instance, filter_by_condition, get_many_by_query
from datetime import datetime

from ..utils.options import GetManyOptions


class TableRowsCRUD(BaseCrudDB):
    model = models.TableRow
    allowed_filters = {
        "id": model.id,
        "name": model.name,
        "distance": model.distance,
        "quantity": model.quantity,
        "count": model.quantity  # alias
    }

    async def create(self, name: str, quantity: int, distance: str, date: datetime = None) -> models.TableRow:
        table_row = self.model(name=name, date=date, quantity=quantity, distance=distance)
        return await create_instance(table_row)

    async def search(self, condition, options: GetManyOptions = None):
        query = self._select
        if condition:
            query = filter_by_condition(query, condition, self.allowed_filters)
        return await get_many_by_query(query, options)


TableRows = TableRowsCRUD()
