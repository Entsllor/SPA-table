import operator
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


@pytest.fixture(scope="function")
async def default_table_row(db) -> models.TableRow:
    yield await crud.TableRows.create("default_table_row", quantity=5, distance=10)

@pytest.fixture(scope="function")
async def table(db) -> models.TableRow:
    yield [
        await crud.TableRows.create("row_1", quantity=1, distance=1),
        await crud.TableRows.create("row_2", quantity=2, distance=3),
        await crud.TableRows.create("row_3", quantity=2, distance=3),
    ]

@pytest.mark.asyncio
async def test_update_table_row(db, default_table_row):
    new_row_name = "_test_update_table_row"
    new_row_quantity = 19
    assert new_row_quantity != default_table_row.quantity
    await crud.TableRows.update(
        filters={'id': default_table_row.id},
        new_values={"name": new_row_name, "quantity": new_row_quantity}
    )
    await db.refresh(default_table_row)
    assert default_table_row.name == new_row_name
    assert default_table_row.quantity == new_row_quantity


@pytest.mark.asyncio
async def test_delete_table_row(db, default_table_row):
    assert default_table_row in db
    await crud.TableRows.delete(id=default_table_row.id)
    assert default_table_row not in db


@pytest.mark.asyncio
async def test_read_table_rows(db, table):
    rows = await crud.TableRows.get_many()
    assert sorted(rows, key=operator.attrgetter('id')) == sorted(table, key=operator.attrgetter('id'))
    assert len(rows) == len(table) and len(rows) > 1
