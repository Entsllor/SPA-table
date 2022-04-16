import React, {useState} from 'react';
import TableWrapper from '../table_wrapper/TableWrapper'
import './App.css';
import Header from "../header/Header";
import AuthForm from "../auth_form/AuthForm"


function App() {
    let [jwt, setJWT] = useState<string | null>(localStorage.getItem("JWT"))
    return (
        <div className="App w-100 min-vh-100">
            <Header handleJWT={setJWT} />
            <body className="main-container">
            <div className="row justify-content-center">
                <div className="col col-12 col-lg-9">
                    {jwt ? <TableWrapper/>: <AuthForm handleJWT={setJWT} jwt={jwt}/>}
                </div>
            </div>
            </body>
        </div>
    );
}

export default App;
