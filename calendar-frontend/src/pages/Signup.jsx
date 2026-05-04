import { useContext, useState } from "react";
import { signup } from "../api/users";
import { AuthContext } from "../auth/AuthContext";

function Signup({ onClose }) {
    const { login } = useContext(AuthContext);

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleSignup = async (e) => {
        e.preventDefault();

        try {
            const data = await signup(username, password);

            // 🔑 auto-login after signup
            login(data.access_token);

            onClose(); // close modal
        } catch (err) {
            alert(err.message);
        }
    };

    return (
        <div className="auth-modal">
            <form className="auth-card" onSubmit={handleSignup}>
                <h2>Create account</h2>

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
                    Sign up
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

export default Signup;