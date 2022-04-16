import React, {useEffect, useState} from "react";
import TableRow from "../../interfaces"


const TableInner: React.FC<{ rows: TableRow[] }> = (props) => {
    const [ordering, setOrdering] = useState<"name" | "distance" | "quantity">("name");
    let rows = props.rows;

    useEffect(() => {
        document.getElementsByClassName("TableWrapper")
    });
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
                    {rows.map(value =>
                        <tr key={value.id}>
                            <td>{value.name}</td>
                            <td>{value.distance}</td>
                            <td>{value.quantity}</td>
                            <td>{value.date}</td>
                        </tr>
                    )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TableInner
