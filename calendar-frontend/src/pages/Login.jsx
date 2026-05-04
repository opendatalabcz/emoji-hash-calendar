import { useState, useContext } from "react";
import { login } from "../api/users";
import { AuthContext } from "../auth/AuthContext";

function Login() {
    const { login: setAuth } = useContext(AuthContext);

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            const data = await login(username, password);
            setAuth(data.access_token);
        } catch (err) {
            alert(err.message);
        }
    };

    return (
        <form onSubmit={handleLogin}>
            <input value={username} onChange={(e) => setUsername(e.target.value)} />
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <button>Login</button>
        </form>
    );
}

export default Login;