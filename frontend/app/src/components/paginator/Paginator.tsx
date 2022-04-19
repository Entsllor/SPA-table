import React from "react";

const Paginator: React.FC<{setPage: CallableFunction, page: number}> = (props) => {

    return <div className="Paginator">
        <ul className="pagination">
            {props.page > 1 ? <li className="page-item"><button className="page-link" onClick={() => props.setPage(props.page - 1)}>{"<"}</button></li> : null}
            {props.page > 1 ? <li className="page-item"><button className="page-link" onClick={() => props.setPage(1)}>1</button></li> : null}
            <li className="page-item"><div className="page-link link-success fw-bold">{props.page}</div></li>
            <li className="page-item"><button className="page-link link-success" onClick={() => props.setPage(props.page + 1)}>{">"}</button></li>
        </ul>
    </div>
}


export default Paginator
