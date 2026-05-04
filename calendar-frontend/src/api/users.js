const API_URL = import.meta.env.VITE_API_URL;

export async function login(username, password) {
    const res = await fetch(`${API_URL}/api/users/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.error || "Login failed");

    return data;
}

export async function signup(username, password) {
    const res = await fetch(`${API_URL}/api/users/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.error || "Signup failed");

    return data;
}