import React, {useState} from "react";
import AuthService from "../../services/authService";

const AuthForm: React.FC<{ jwt: string | null; handleJWT: CallableFunction}> = (props) => {
    const [email, setEmail] = useState<string>('')
    const [password, setPassword] = useState<string>('')
    const [username, setUsername] = useState<string>('')

    return <div className="AuthForm">
        <div className="card">
            <div className="main-card-title">
                <input
                    name="username"
                    placeholder="username"
                    type="text"
                    onChange={event => setUsername(event.target.value)}
                />
                <input
                    name="email"
                    placeholder="email"
                    type="text"
                    onChange={event => setEmail(event.target.value)}
                />
                <input
                    name="password"
                    type="password"
                    placeholder="password"
                    onChange={event => setPassword(event.target.value)}
                />
                <button onClick={() => AuthService.login(username, password).then(response => {props.handleJWT(response.data.access_token)})}>Login</button>
                <button onClick={() => AuthService.registration(username, password, email)}>Registration</button>
                <button onClick={() => AuthService.revoke().then(response => {props.handleJWT(response.data.access_token)})}>Revoke</button>
            </div>
        </div>
    </div>
        ;
};

export default AuthForm
