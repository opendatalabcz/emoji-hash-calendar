import { useContext, useState } from "react";
import { signup } from "../../api/users";
import { AuthContext } from "../../auth/AuthContext";
import "./Signup.css"

function Signup({ onClose }) {
    const { login } = useContext(AuthContext);

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirm_password, setConfirmPassword] = useState("");

    const [error, setError] = useState("");

    const handleSignup = async (e) => {
        e.preventDefault();
        setError("");

        if (password !== confirm_password) {
            setError("Passwords do not match");
            return;
        }

        try {
            const data = await signup(username, password, confirm_password);

            login(data.access_token);

            onClose();
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

                <input
                    className="auth-input"
                    type="password"
                    value={confirm_password}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="confirm password"
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

                {error && (
                    <div className="auth-error">
                        {error}
                    </div>
                )}
            </form>
        </div>
    );
}

export default Signup;