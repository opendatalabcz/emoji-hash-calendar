const API_URL = import.meta.env.VITE_API_URL;

export async function transformCalendar(payload) {
    const res = await fetch(`${API_URL}/api/calendars/transform`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.error || "Request failed");
    }

    return data;
}

export async function transformCalendarFile({ file, method, dictionary_id, user_mapping }) {
    const form = new FormData();
    form.append("file", file);
    form.append("method", method);

    if (dictionary_id !== undefined && dictionary_id !== null) {
        form.append("dictionary_id", dictionary_id);
    }

    if (user_mapping) {
        form.append("user_mapping", JSON.stringify(user_mapping));
    }

    const res = await fetch(`${API_URL}/api/calendars/transform-file`, {
        method: "POST",
        body: form,
    });

    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.message || data.error || "File transform failed");
    }

    return data;
}

export async function transformText(payload) {
    const res = await fetch(`${API_URL}/api/calendars/transform-text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.error || "Request failed");
    }

    return data;
}

export async function generateCalendarLink(payload) {
    const res = await fetch(`${API_URL}/api/calendars/link`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) {
        throw new Error(data.error || "Request failed");
    }
    return data;
}

export async function getMethods() {
    const res = await fetch(`${API_URL}/api/calendars/methods`);
    const data = await res.json();
    if (!res.ok) {
        throw new Error(data.error || "Request failed");
    }
    return data.methods;
}