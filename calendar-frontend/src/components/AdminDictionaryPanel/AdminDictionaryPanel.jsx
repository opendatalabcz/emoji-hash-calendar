import { useEffect, useState, useContext } from "react";
import { AuthContext } from "../../auth/AuthContext";
import {
    getDictionaries,
    createDictionary,
    deleteDictionary,
    bulkInsertEntries
} from "../../api/dictionary";
import "./AdminDictionaryPanel.css";

function AdminDictionaryPanel({onRefresh}) {
    const { token } = useContext(AuthContext);

    const [dictionaries, setDictionaries] = useState([]);
    const [selectedId, setSelectedId] = useState(null);
    const [newDict, setNewDict] = useState({ name: "", language: "", description: "" });
    const [showCreate, setShowCreate] = useState(false);
    const [showCreateModal, setShowCreateModal] = useState(false);
    const [bulkData, setBulkData] = useState(JSON.stringify());

    useEffect(() => {
        getDictionaries().then(setDictionaries).catch(console.error);
    }, []);

    const handleDelete = async () => {
        if (!selectedId) return;
        await deleteDictionary(token, selectedId);
        onRefresh();
        const updated = await getDictionaries();
        setDictionaries(updated);
        setSelectedId(null);
    };

    const handleBulkInsert = async () => {
        if (!selectedId) return;

        try {
            const entries = JSON.parse(bulkData);
            await bulkInsertEntries(token, selectedId, entries);
            onRefresh();
            alert("Bulk insert successful!");
        } catch {
            alert("Invalid JSON format");
        }
    };

    return (
        <div className="admin-dictionary-panel">
            <h3>Dictionary Management</h3>
            <p>Create and manage dictionaries</p>

            <button
                className="create-toggle-btn"
                onClick={() => setShowCreateModal(true)}
            >
                + Create New Dictionary
            </button>

            {showCreateModal && (
                <div className="admin-modal-overlay" onClick={() => setShowCreateModal(false)}>
                    <div className="admin-modal" onClick={(e) => e.stopPropagation()}>
                        <h2>Create Dictionary</h2>

                        <input
                            placeholder="Name"
                            value={newDict.name}
                            onChange={(e) => setNewDict({ ...newDict, name: e.target.value })}
                        />

                        <input
                            placeholder="Language (ideally add country flag)"
                            value={newDict.language}
                            onChange={(e) => setNewDict({ ...newDict, language: e.target.value })}
                        />

                        <input
                            placeholder="Description"
                            value={newDict.description}
                            onChange={(e) => setNewDict({ ...newDict, description: e.target.value })}
                        />

                        <label>Bulk Insert Entries (JSON)</label>
                        <textarea
                            placeholder='{"hello":"👋","world":"🌍"}'
                            value={bulkData}
                            onChange={(e) => setBulkData(e.target.value)}
                        />

                        <div className="modal-actions">
                            <button className="btn-cancel" onClick={() => setShowCreateModal(false)}>
                                Cancel
                            </button>

                            <button
                                className="btn-create"
                                onClick={async () => {
                                    try {
                                        const entries = JSON.parse(bulkData);

                                        const confirmed = window.confirm(
                                            `Create dictionary "${newDict.name}" and insert ${Object.keys(entries).length} entries?`
                                        );
                                        if (!confirmed) return;

                                        const created = await createDictionary(token, newDict);
                                        onRefresh();
                                        await bulkInsertEntries(token, created.id, entries);

                                        const updated = await getDictionaries();
                                        setDictionaries(updated);

                                        setNewDict({ name: "", language: "", description: "" });
                                        setBulkData("{}");
                                        setShowCreateModal(false);
                                    } catch {
                                        alert("Invalid JSON format");
                                    }
                                }}
                            >
                                Create
                            </button>

                        </div>
                    </div>
                </div>
            )}

            <div className="dict-select-block">
                <label>Select Dictionary to Edit</label>
                <select
                    value={selectedId || ""}
                    onChange={(e) => setSelectedId(Number(e.target.value))}
                >
                    <option value="">-- Choose dictionary --</option>
                    {dictionaries.map((d) => (
                        <option key={d.id} value={d.id}>
                            {d.name} ({d.language})
                        </option>
                    ))}
                </select>
            </div>

            {selectedId && (
                <div className="dict-actions">
                    <textarea
                        placeholder='{"hello":"👋","world":"🌍"}'
                        value={bulkData}
                        onChange={(e) => setBulkData(e.target.value)}
                    />

                    <button className="bulk-btn" onClick={handleBulkInsert}>
                        Bulk Insert Entries
                    </button>
                    <button className="delete-btn" onClick={handleDelete}>
                        Delete Dictionary
                    </button>
                </div>
            )}
        </div>
    );
}

export default AdminDictionaryPanel;
