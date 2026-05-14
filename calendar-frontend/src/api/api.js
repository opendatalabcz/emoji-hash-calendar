const API_URL = import.meta.env.VITE_API_URL;

export async function api(path, options = {}) {
    const res = await fetch(`${API_URL}${path}`, options);

    let data = null;

    try {
        data = await res.json();
    } catch {
    }

    if (!res.ok) {
        const message =
            data?.error ||
            data?.message ||
            data?.detail ||
            data?.messages && JSON.stringify(data.messages) ||
            `Request failed (${res.status})`;

        throw new Error(message);
    }

    return data;
}

export async function getUsers(token) {
    const res = await fetch(`${API_URL}/api/users/`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to fetch users");
    return data;
}