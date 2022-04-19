import React, {FC} from "react";


const Filter: FC<{ setFilter: CallableFunction; }> = (props) => {
    const setFilteringCondition = (): void => {
        let fieldName: string = (document.getElementById("select-filtering-field") as HTMLSelectElement).value;
        let operator: string = (document.getElementById("select-filtering-operator") as HTMLSelectElement).value;
        let value: string = (document.getElementById("input-filtering-value") as HTMLInputElement).value;
        if (operator == "like" && !(value.startsWith("%") || value.endsWith("%"))) {
            value = `%${value}%`;
        }
        props.setFilter(`${fieldName}__${operator}:${value}`)
    };


    return <div className="Filter">
        <div className="input-group">
            <select className="form-select" id="select-filtering-field">
                <option value="name">Name</option>
                <option value="distance">Distance</option>
                <option value="quantity">Quantity</option>
                <option value="id">ID</option>
            </select>
            <select className="form-select" id="select-filtering-operator">
                <option value="like">has</option>
                <option value="eq">equals</option>
                <option value="gt">greater</option>
                <option value="lt">lower</option>
            </select>
            <input type="text" className="form-control" id="input-filtering-value" placeholder="substring"/>
            <button className="btn btn-success" type="button" id="filter_submit-button" onClick={setFilteringCondition}>
                Search
            </button>
        </div>
    </div>;
};

export default Filter