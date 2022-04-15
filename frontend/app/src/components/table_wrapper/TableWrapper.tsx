import React from "react";
import TableInner from "../table/TableInner"
import TableRow from "../../interfaces"

const tableRows: TableRow[] = [
    {id: 1, date: new Date(), distance: 242, name: "Hello world!", quantity: 10},
    {id: 2, date: new Date(), distance: 41231, name: "Hello world!", quantity: 20},
    {id: 3, date: new Date(), distance: 2012, name: "Hello world!", quantity: 30},
    {id: 4, date: new Date(), distance: 2013212, name: "Hello world!", quantity: 40},
    {id: 5, date: new Date(), distance: 231212, name: "Hello world!", quantity: 50},
    {id: 6, date: new Date(), distance: 201312, name: "Hello world!", quantity: 60}
];

const TableWrapper: React.FC = () => {
    return <div className="TableWrapper">
        <div className="main-table-card-title">Main Table</div>
        <TableInner tableRows={tableRows}/>
    </div>
}
export default TableWrapper;