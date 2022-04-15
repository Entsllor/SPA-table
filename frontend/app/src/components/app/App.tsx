import React from 'react';
import TableWrapper from '../table_wrapper/TableWrapper'
import './App.css';
import Header from "../header/Header";

function App() {
    return (
        <div className="App w-100">
            <Header/>
            <body className="container-fluid w-100">
            <div className="row justify-content-center">
                <div className="col col-12 col-lg-9">
                    <TableWrapper/>
                </div>
            </div>
            </body>
        </div>
    );
}

export default App;
