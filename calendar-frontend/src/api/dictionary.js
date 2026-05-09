const API_URL = import.meta.env.VITE_API_URL;

// -----------------------------
// PUBLIC ENDPOINTS
// -----------------------------

export async function getDictionaries() {
    const res = await fetch(`${API_URL}/api/dictionaries/`);
    const data = await res.json();

    if (!res.ok) throw new Error(data.error || "Failed to fetch dictionaries");
    return data;
}

export async function getDictionary(dictionaryId) {
    const res = await fetch(`${API_URL}/api/dictionaries/${dictionaryId}`);
    const data = await res.json();

    if (!res.ok) throw new Error(data.error || "Dictionary not found");
    return data;
}

// -----------------------------
// ADMIN ENDPOINTS
// -----------------------------

export async function createDictionary(token, payload) {
    const res = await fetch(`${API_URL}/api/dictionaries/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!res.ok) {
        throw new Error(
            data.error ||
            data.message ||
            "Failed to create dictionary"
        );
    }

    return data;
}

export async function deleteDictionary(token, dictionaryId) {
    const res = await fetch(`${API_URL}/api/dictionaries/${dictionaryId}`, {
        method: "DELETE",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    const data = await res.json();

    if (!res.ok) {
        throw new Error(
            data.error ||
            data.message ||
            "Failed to delete dictionary"
        );
    }

    return data;
}

// -----------------------------
// ENTRY ENDPOINTS
// -----------------------------

export async function getDictionaryEntries(token, dictionaryId) {
    const res = await fetch(`${API_URL}/api/dictionaries/${dictionaryId}/entries`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.error || "Failed to fetch entries");
    return data;
}

export async function addDictionaryEntry(token, dictionaryId, payload) {
    const res = await fetch(`${API_URL}/api/dictionaries/${dictionaryId}/entries`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!res.ok) {
        throw new Error(
            data.error ||
            data.message ||
            "Failed to add entry"
        );
    }

    return data;
}

export async function deleteDictionaryEntry(token, dictionaryId, entryId) {
    const res = await fetch(`${API_URL}/api/dictionaries/${dictionaryId}/entries/${entryId}`, {
        method: "DELETE",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    const data = await res.json();

    if (!res.ok) {
        throw new Error(
            data.error ||
            data.message ||
            "Failed to delete entry"
        );
    }

    return data;
}

export async function bulkInsertEntries(token, dictionaryId, entries) {
    const res = await fetch(`${API_URL}/api/dictionaries/${dictionaryId}/entries/bulk`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(entries),
    });

    const data = await res.json();

    if (!res.ok) {
        throw new Error(
            data.error ||
            data.message ||
            "Bulk insert failed"
        );
    }

    return data;
}
