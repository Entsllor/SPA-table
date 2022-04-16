import React from "react";


const Header: React.FC<{"handleJWT": CallableFunction}> = (props) => {
    return <div className="Header">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <div className="container-fluid">
                <a className="navbar-brand" href="#">TableApp</a>
                <a className="link-light" href="#" onClick={() => props.handleJWT("")}>
                    {localStorage.getItem("JWT") ? "Log Out" : "Sign In"}
                </a>
            </div>
        </nav>
    </div>
}


export default Header
