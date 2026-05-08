const API_URL = import.meta.env.VITE_API_URL;

/**
 * Get all mapping sets for logged-in user
 */
export async function getMappingSets(token) {
    const res = await fetch(`${API_URL}/api/mappings/sets`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to load sets");

    return data;
}

/**
 * Create new mapping set
 */
export async function createMappingSet(token, name) {
    const res = await fetch(`${API_URL}/api/mappings/sets`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ name }),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to create set");

    return data;
}

/**
 * Get mappings inside a set
 */
export async function getMappings(token, setId) {
    const res = await fetch(
        `${API_URL}/api/mappings/sets/${setId}/mappings`,
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to load mappings");

    return data;
}

export async function updateMappingSet(token, setId, payload) {
    const res = await fetch(`${API_URL}/api/mappings/sets/${setId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to update set");

    return data;
}

export async function deleteMappingSet(token, setId) {
    const res = await fetch(`${API_URL}/api/mappings/sets/${setId}`, {
        method: "DELETE",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to delete set");

    return data;
}

