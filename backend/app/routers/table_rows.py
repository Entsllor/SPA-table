from fastapi import Depends, APIRouter, status

from ..utils import exceptions
from ..utils.dependencies import get_many_options, get_current_active_user
from ..schemas.table_rows import TableRowCreate, TableRow, TableRowUpdate
from ..crud import TableRows

router = APIRouter(prefix="/table/rows", dependencies=[])


@router.get("/", response_model=list[TableRow])
async def read_table_rows(options: get_many_options = Depends()):
    return await TableRows.get_many(_options=options)


@router.get("/{row_id}", response_model=TableRow)
async def read_table_row(row_id: int):
    return await TableRows.get_one(id=row_id)


@router.post("/", response_model=TableRow, status_code=status.HTTP_201_CREATED)
async def create_table_row(table_row: TableRowCreate):
    return await TableRows.create(**table_row.dict())


async def update_table_row(row_id: int, new_values: TableRowUpdate):
    result = await TableRows.update(filters={'id': row_id}, new_values=new_values.dict())
    if not result.rowcount:
        raise exceptions.InstanceNotFound


router.put("/{row_id}")(update_table_row)
router.patch("/{row_id}")(update_table_row)


@router.delete("/{row_id}")
async def delete_table_row(row_id: int):
    result = await TableRows.delete(id=row_id)
    if not result.rowcount:
        raise exceptions.InstanceNotFound
