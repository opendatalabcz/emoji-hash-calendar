import { useState, useContext } from "react";
import { login } from "../../api/users";
import { AuthContext } from "../../auth/AuthContext";
import "./Login.css"

function Login({ onClose }) {
    const { login: setAuth } = useContext(AuthContext);

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            const data = await login(username, password);

            setAuth(data.access_token);

            onClose();
        } catch (err) {
            alert(err.message);
        }
    };

    return (
        <div className="auth-modal">
            <form className="auth-card" onSubmit={handleLogin}>
                <h2>Login</h2>

                <input
                    className="auth-input"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="username"
                />

                <input
                    className="auth-input"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="password"
                />

                <button className="btn primary full">
                    Login
                </button>

                <button
                    type="button"
                    className="btn link"
                    onClick={onClose}
                >
                    Cancel
                </button>
            </form>
        </div>
    );
}

export default Login;