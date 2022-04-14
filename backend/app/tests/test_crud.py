from decimal import Decimal

import pytest

from app import models, crud
from datetime import datetime


@pytest.mark.asyncio
async def test_create_table_row(db):
    table_row_name = "_test_create_table_row"
    date_now = datetime.now().date()
    table_row = await crud.TableRows.create(name=table_row_name, date=date_now, quantity=10, distance=15)
    assert isinstance(table_row, models.TableRow)
    assert table_row.distance == 15
    assert isinstance(table_row.distance, Decimal)
    assert table_row.name == table_row_name
    assert table_row.date == date_now
    assert table_row.quantity == 10


@pytest.mark.asyncio
async def test_create_table_row_with_default_time_value(db):
    table_row_name = "_test_create_table_row"
    table_row = await crud.TableRows.create(name=table_row_name, quantity=10, distance=15)
    assert table_row.date == datetime.now().date()  # don't run this test at midnight
