import { useState } from "react";
import emojis from "emoji.json";
import "./RuleSidebar.css";

function RuleSidebar({
                         userMappings,
                         setUserMappings,
                         mappingSets,
                         selectedSetId,
                         setSelectedSetId,
                         createSet,
                         loadSet,
                         saveSet,
                         isLoggedIn
                     }) {
    const EMOJIS = emojis.slice(0, 2000).map(e => e.char);

    const addRule = () => {
        setUserMappings([...userMappings, { keyword: "", emoji: "" }]);
    };

    const updateRule = (i, field, value) => {
        const copy = [...userMappings];
        copy[i][field] = value;
        setUserMappings(copy);
    };

    const removeRule = (i) => {
        setUserMappings(userMappings.filter((_, idx) => idx !== i));
    };

    const handleLoad = async () => {
        if (!selectedSetId) return;

        const data = await loadSet(selectedSetId);

        const mapped = data.map(m => ({
            keyword: m.word,
            emoji: m.emoji
        }));

        setUserMappings(mapped);
    };

    const handleSave = async () => {
        try {
            let setId = selectedSetId;
            let name;

            if (!setId) {
                const input = prompt("Enter a name for this set:");
                if (!input || !input.trim()) return;

                name = input.trim();

                const newSet = await createSet(name);
                if (!newSet) throw new Error("Failed to create set");

                setId = newSet.id;
                setSelectedSetId(newSet.id);
            } else {
                name =
                    mappingSets.find(s => s.id === setId)?.name || "Untitled";
            }

            await saveSet(setId, {
                name,
                mappings: userMappings
            });

            alert("Saved successfully ✅");

        } catch (err) {
            console.error(err);
            alert(err.message || "Save failed ❌");
        }
    };
    return (
        <div className="sidebar">
            {isLoggedIn && (
                <>
                    <h3>Mapping Sets</h3>

                    <div style={{ display: "flex", gap: "8px", marginBottom: "10px" }}>
                        <select
                            value={selectedSetId ?? ""}
                            onChange={(e) =>
                                setSelectedSetId(
                                    e.target.value ? Number(e.target.value) : null
                                )
                            }
                        >
                            <option value="">-- Select set --</option>
                            {mappingSets.map(set => (
                                <option key={set.id} value={set.id}>
                                    {set.name}
                                </option>
                            ))}
                        </select>

                        <button
                            disabled={!selectedSetId}
                            onClick={handleLoad}
                        >
                            Load
                        </button>
                    </div>
                </>
            )}

            <h3>Rules</h3>

            {userMappings.map((m, i) => (
                <div key={i}>
                    <input
                        placeholder="keyword"
                        value={m.keyword}
                        onChange={(e) =>
                            updateRule(i, "keyword", e.target.value)
                        }
                    />

                    <select
                        value={m.emoji}
                        onChange={(e) =>
                            updateRule(i, "emoji", e.target.value)
                        }
                    >
                        <option value="">?</option>
                        {EMOJIS.map((emoji) => (
                            <option key={emoji} value={emoji}>
                                {emoji}
                            </option>
                        ))}
                    </select>

                    <button onClick={() => removeRule(i)}>X</button>
                </div>
            ))}

            <button onClick={addRule}>+ Add rule</button>

            {isLoggedIn && (
                <div style={{ marginTop: "10px" }}>
                    <button
                        disabled={userMappings.length === 0}
                        onClick={handleSave}
                    >
                        Save set
                    </button>
                </div>
            )}

            {!isLoggedIn && (
                <p style={{ marginTop: 10 }}>
                    Login to save and manage rule sets.
                </p>
            )}
        </div>
    );
}

export default RuleSidebar;