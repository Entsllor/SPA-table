import React, {useEffect, useState} from "react";
import TableInner from "../table/TableInner"
import {TableRow, IOrderingFields} from "../../interfaces"
import TableService from "../../services/tableService";
import Paginator from "../paginator/Paginator";


const TableWrapper: React.FC = () => {
    const [rows, setRows] = useState<TableRow[]>([]);
    const [ordering, setOrdering] = useState<IOrderingFields>({})
    const [page, setPage] = useState<number>(1)
    const updateRows = async () => {
        let response = await TableService.getRows(ordering, page, 20);
        setRows(response.data)
    }

    useEffect(() => {
            updateRows();
        }, [ordering, page]
    );
    return <div className="TableWrapper">
        <div className="card">
            <div className="main-card-title">Main Table</div>
            <TableInner handleOrdering={setOrdering} rows={rows}/>
        </div>
        <div className="d-flex flex-row justify-content-end mt-2">
            <Paginator page={page} setPage={setPage}/>
        </div>
    </div>
};

export default TableWrapper;
