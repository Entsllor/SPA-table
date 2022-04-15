import React from "react";
import TableRow from "../../interfaces"


const TableInner: React.FC<{ tableRows: TableRow[] }> = (props) => {
    return (
        <div className="Table">
            <div style={{overflowX: "auto"}}>
                <table className="table">
                    <thead>
                    <tr>
                        <th>Name</th>
                        <th>Distance</th>
                        <th>Quantity</th>
                        <th>Date</th>
                    </tr>
                    </thead>
                    <tbody>
                    {props.tableRows.map(value =>
                        <tr key={value.id}>
                            <td>{value.name}</td>
                            <td>{value.distance}</td>
                            <td>{value.quantity}</td>
                            <td>{value.date.toDateString()}</td>
                        </tr>
                    )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TableInner
