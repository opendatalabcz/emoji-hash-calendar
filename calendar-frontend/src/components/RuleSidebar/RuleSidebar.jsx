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
    const EMOJIS = emojis.slice(0, 5000).map(e => e.char);

    const [openPickerIndex, setOpenPickerIndex] = useState(null);

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
        const data = await loadSet(selectedSetId);

        setUserMappings(
            data.map(m => ({
                keyword: m.word,
                emoji: m.emoji
            }))
        );
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
                setId = newSet.id;
                setSelectedSetId(newSet.id);
            } else {
                name =
                    mappingSets.find(s => s.id === setId)?.name || "Untitled";
            }

            await saveSet(setId, {
                name,
                mappings: userMappings.map(m => ({
                    word: m.keyword,
                    emoji: m.emoji
                }))
            });

            alert("Saved successfully 🎉");
        } catch (err) {
            console.error(err);
            alert(err.message || "Save failed");
        }
    };

    return (
        <div className="sidebar">
            {isLoggedIn && (
                <>
                    <h3>Mapping Sets</h3>

                    <div className="set-controls">
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
                <div className="rule-row" key={i}>
                    <input
                        className="rule-keyword"
                        placeholder="keyword"
                        value={m.keyword}
                        onChange={(e) =>
                            updateRule(i, "keyword", e.target.value)
                        }
                    />

                    {/* Emoji button */}
                    <button
                        className="rule-emoji"
                        onClick={() =>
                            setOpenPickerIndex(openPickerIndex === i ? null : i)
                        }
                    >
                        {m.emoji || "➕"}
                    </button>

                    <button onClick={() => removeRule(i)}>X</button>

                    {/* Emoji picker dropdown */}
                    {openPickerIndex === i && (
                        <div className="emoji-picker">
                            {EMOJIS.map((emoji) => (
                                <button
                                    key={emoji}
                                    className="emoji-option"
                                    onClick={() => {
                                        updateRule(i, "emoji", emoji);
                                        setOpenPickerIndex(null);
                                    }}
                                >
                                    {emoji}
                                </button>
                            ))}
                        </div>
                    )}
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
        </div>
    );
}

export default RuleSidebar;