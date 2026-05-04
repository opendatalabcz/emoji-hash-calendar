import { useState } from "react";
import { signup } from "../api/users";

function Signup() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleSignup = async (e) => {
        e.preventDefault();

        try {
            await signup(username, password);
            alert("Account created");
        } catch (err) {
            alert(err.message);
        }
    };

    return (
        <form onSubmit={handleSignup}>
            <input value={username} onChange={(e) => setUsername(e.target.value)} />
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <button>Create account</button>
        </form>
    );
}

export default Signup;