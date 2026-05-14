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
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const usernameValid = username.length === 0 || (
        username.length >= 3 &&
        username.length <= 20 &&
        /^[a-zA-Z0-9_]+$/.test(username)
    );
    const passwordValid = password.length === 0 || (
        password.length >= 8 &&
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/.test(password)
    );
    const passwordsMatch = confirm_password.length === 0 || password === confirm_password;

    const handleSignup = async (e) => {
        e.preventDefault();
        setError("");

        if (username.length < 3 || username.length > 20 || !/^[a-zA-Z0-9_]+$/.test(username)) {
            setError("Username must be 3–20 characters, letters, numbers and underscores only");
            return;
        }
        if (!passwordValid) {
            setError("Password must be at least 8 characters and contain a number, a capital and a lowercase letter");
            return;
        }
        if (password !== confirm_password) {
            setError("Passwords do not match");
            return;
        }
        try {
            const data = await signup(username, password, confirm_password);
            login(data.access_token);
            onClose();
        } catch (err) {
            setError("Username already taken");
        }
    };

    return (
        <div className="auth-modal">
            <form className="auth-card" onSubmit={handleSignup}>
                <h2>Create account</h2>

                <div className="auth-field">
                    <input
                        className={`auth-input ${!usernameValid ? "auth-input-error" : ""}`}
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="username"
                    />
                    <span className={`auth-field-hint ${!usernameValid ? "hint-error" : ""}`}>
                        3–20 characters, letters, numbers and underscores only
                    </span>
                </div>

                <div className="auth-field password-field">
                    <div className="password-input-wrapper">
                        <input
                            className={`auth-input ${!passwordValid ? "auth-input-error" : ""}`}
                            type={showPassword ? "text" : "password"}
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="password"
                        />
                        <span
                            className="password-toggle"
                            onClick={() => setShowPassword(!showPassword)}
                        >
                            {showPassword ? "🙈" : "👁️"}
                        </span>
                    </div>

                    <span className={`auth-field-hint ${!passwordValid ? "hint-error" : ""}`}>
                        min. 8 characters, with a number, a capital and a lowercase letter
                    </span>
                </div>


                <div className="auth-field password-field">
                    <div className="password-input-wrapper">
                        <input
                            className={`auth-input ${!passwordsMatch ? "auth-input-error" : ""}`}
                            type={showConfirmPassword ? "text" : "password"}
                            value={confirm_password}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            placeholder="confirm password"
                        />
                        <span
                            className="password-toggle"
                            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        >
                            {showConfirmPassword ? "🙈" : "👁️"}
                        </span>
                    </div>

                    {!passwordsMatch && (
                        <span className="auth-field-hint hint-error">Passwords do not match</span>
                    )}
                </div>


                <button className="btn primary full">Sign up</button>
                <button type="button" className="btn link" onClick={onClose}>Cancel</button>

                {error && <div className="auth-error">{error}</div>}
            </form>
        </div>
    );
}

export default Signup;