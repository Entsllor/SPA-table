from fastapi import Depends, APIRouter
from ..utils.dependencies import get_many_options
from ..schemas.table_rows import TableRowCreate, TableRow, TableRowUpdate
from ..crud import TableRows

router = APIRouter(prefix="/table/rows", )


@router.get("/", response_model=list[TableRow])
async def read_table_rows(options: get_many_options = Depends()):
    return await TableRows.get_many(_options=options)


@router.get("/{row_id}", response_model=TableRow)
async def read_table_row(row_id: int):
    return await TableRows.get_one(id=row_id)


@router.post("/", response_model=TableRow)
async def create_table_row(table_row: TableRowCreate):
    return await TableRows.create(**table_row.dict())


async def update_table_row(row_id: int, new_values: TableRowUpdate):
    return await TableRows.update(filters={'id': row_id}, new_values=new_values.dict())


router.put("/{row_id}", response_model=TableRow)(update_table_row)
router.patch("/{row_id}", response_model=TableRow)(update_table_row)


@router.delete("/{row_id}")
async def delete_table_row(row_id):
    return await TableRows.delete(id=row_id)
