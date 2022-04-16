import React, {useEffect, useState} from "react";
import TableInner from "../table/TableInner"
import TableRow from "../../interfaces"
import TableService from "../../services/tableService";


const TableWrapper: React.FC = () => {
    const [rows, setRows] = useState<TableRow[]>([]);

    const updateRows = async () => {
        let response = await TableService.getRows();
        setRows(response.data)
    }

    useEffect(() => {
            updateRows();
        }, []
    );

    return <div className="TableWrapper">
        <div className="main-card-title">Main Table</div>
        <TableInner rows={rows}/>
    </div>
};

export default TableWrapper;
