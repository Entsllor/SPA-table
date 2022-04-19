import React, {useEffect, useState} from "react";
import TableInner from "../table/TableInner"
import {TableRow, IOrderingFields} from "../../interfaces"
import TableService from "../../services/tableService";
import Paginator from "../paginator/Paginator";
import Filter from "../filter/Filter";


const TableWrapper: React.FC = () => {
    const [rows, setRows] = useState<TableRow[]>([]);
    const [ordering, setOrdering] = useState<IOrderingFields>({});
    const [filter, setFilter] = useState<string>("")
    const [page, setPage] = useState<number>(1)
    const updateRows = async () => {
        let response = await TableService.getRows(ordering, page, 20, filter);
        setRows(response.data)
    }

    useEffect(() => {
            updateRows();
        }, [ordering, page, filter]
    );
    return <div className="TableWrapper">
        <div className="card">
            <div className="main-card-title">Main Table</div>
            <TableInner handleOrdering={setOrdering} rows={rows}/>
        </div>
        <div className="d-flex flex-row justify-content-between flex-wrap mt-2">
            <Paginator page={page} setPage={setPage}/>
            <Filter setFilter={setFilter}/>
        </div>
    </div>
};

export default TableWrapper;
