import { useState, useContext } from "react";
import { login } from "../../api/users";
import { AuthContext } from "../../auth/AuthContext";
import "./Login.css"

function Login({ onClose }) {
    const { login: setAuth } = useContext(AuthContext);

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();

        if (!username || !password) {
            setError("Username and password cannot be empty.");
            return;
        }

        try {
            const data = await login(username, password);
            setAuth(data.access_token);
            onClose();
        } catch (err) {
            setError("Invalid username or password.");
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
                {error && <div className="auth-error">{error}</div>}
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