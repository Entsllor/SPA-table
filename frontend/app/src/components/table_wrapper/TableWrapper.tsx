import React, {useEffect, useState} from "react";
import TableInner from "../table/TableInner"
import {TableRow, IOrderingFields} from "../../interfaces"
import TableService from "../../services/tableService";


const TableWrapper: React.FC = () => {
    const [rows, setRows] = useState<TableRow[]>([]);
    const [ordering, setOrdering] = useState<IOrderingFields>({})
    const updateRows = async () => {
        let response = await TableService.getRows(ordering);
        setRows(response.data)
    }

    useEffect(() => {
            updateRows();
        }, [ordering]
    );
    return <div className="TableWrapper">
        <div className="main-card-title">Main Table</div>
        <TableInner handleOrdering={setOrdering} rows={rows}/>
    </div>
};

export default TableWrapper;
