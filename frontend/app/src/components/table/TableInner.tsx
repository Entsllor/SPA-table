import React, {MouseEvent} from "react";
import {TableRow, IOrderingFields} from "../../interfaces"

const TableInner: React.FC<{ rows: TableRow[], handleOrdering: CallableFunction }> = (props) => {
    let rows = props.rows;

    const changeOrdering = (event: MouseEvent<HTMLButtonElement>) => {
        let element = event.target as HTMLButtonElement;
        let fieldName = element.name as "name" | "distance" | "quantity" | "id";
        props.handleOrdering((oldOrdering: IOrderingFields) => {
            let ordering = {...oldOrdering};
            if (fieldName in ordering)
                switch (ordering[fieldName]) {
                    case true:
                        ordering[fieldName] = false;
                        props.handleOrdering(ordering);
                        element.classList.remove("btn-success")
                        element.classList.add("btn-danger")
                        break
                    default:
                        delete ordering[fieldName]
                        props.handleOrdering(ordering);
                        element.classList.remove("btn-danger")
                        break
                } else {
                ordering[fieldName] = true
                props.handleOrdering(ordering);
                element.classList.add("btn-success")
            }
        });
    };

    return (
        <div className="Table">
            <div style={{overflowX: "auto"}}>
                <table className="table">
                    <thead>
                    <tr>
                        <th>
                            <button
                                name="id"
                                className="btn" onClick={(event) => changeOrdering(event)}>ID
                            </button>
                        </th>
                        <th>
                            <button
                                name="name"
                                className="btn" onClick={(event) => changeOrdering(event)}>Name
                            </button>
                        </th>
                        <th>
                            <button
                                name="distance"
                                className="btn"
                                onClick={(event) => changeOrdering(event)}>Distance
                            </button>
                        </th>
                        <th>
                            <button
                                name="quantity"
                                className="btn"
                                onClick={(event) => changeOrdering(event)}>Quantity
                            </button>
                        </th>
                        <th>
                            <div className="btn">Date</div>
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                    {rows.map(value =>
                        <tr key={value.id}>
                            <td>{value.id}</td>
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
