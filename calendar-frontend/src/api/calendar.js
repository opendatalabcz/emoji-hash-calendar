const API_URL = import.meta.env.VITE_API_URL;

export async function transformCalendar(payload) {
    const res = await fetch(`${API_URL}/api/calendars/transformation`, {
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