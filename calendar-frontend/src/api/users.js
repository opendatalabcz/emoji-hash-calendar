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

export async function signup(username, password, confirm_password) {
    const res = await fetch(`${API_URL}/api/users/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password, confirm_password }),
    });

    const data = await res.json();

    if (!res.ok) {
        const message =
            data.error ||
            data.message ||
            (data.messages && JSON.stringify(data.messages)) ||
            "Signup failed";

        throw new Error(message);
    }

    return data;
}

export async function makeAdmin(id, token) {
    const res = await fetch(`${API_URL}/api/users/${id}/admin`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
    });

    const data = await res.json();

    if (!res.ok) {
        const message =
            data.error ||
            data.message ||
            (data.messages && JSON.stringify(data.messages)) ||
            "Failed to grant admin role";

        throw new Error(message);
    }

    return data;
}

export async function getUsers(token) {
    const res = await fetch(`${API_URL}/api/users/`, {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    const data = await res.json();

    if (!res.ok) {
        const message =
            data.error ||
            data.message ||
            (data.messages && JSON.stringify(data.messages)) ||
            "Failed to fetch users";

        throw new Error(message);
    }

    return data;
}
