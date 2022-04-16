import React, {useState} from "react";
import AuthService from "../../services/authService";

const AuthForm: React.FC<{ jwt: string | null; handleJWT: CallableFunction }> = (props) => {
    const [email, setEmail] = useState<string>('')
    const [password, setPassword] = useState<string>('')
    const [username, setUsername] = useState<string>('')

    return <div className="AuthForm">
        <div className="card">
            <div className="main-card-title">Sign In</div>
            <div className="card-body">

                <input
                    name="username" required
                    placeholder="username"
                    type="text"
                    className="form-control mb-3"
                    onChange={event => setUsername(event.target.value)}
                />
                <input
                    name="email"
                    placeholder="email (for registration)"
                    type="text"
                    className="form-control mb-3"
                    onChange={event => setEmail(event.target.value)}
                />
                <input
                    name="password" required
                    type="password"
                    placeholder="password"
                    className="form-control mb-3"
                    onChange={event => setPassword(event.target.value)}
                />
                <div className="d-flex flex-row justify-content-end gap-2">
                    <button className="btn btn-dark"
                            onClick={() => AuthService.login(username, password).then(response => {
                                props.handleJWT(response.data.access_token)
                            })}>Login
                    </button>
                    <button className="btn btn-dark"
                            onClick={() => AuthService.registration(username, password, email)}>Registration
                    </button>
                    <button className="btn btn-dark" onClick={() => AuthService.revoke().then(response => {
                        props.handleJWT(response.data.access_token)
                    })}>Revoke
                    </button>
                </div>

            </div>
        </div>
    </div>
};

export default AuthForm
