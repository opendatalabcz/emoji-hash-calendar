import { useEffect, useState } from "react";
import { getDictionaries } from "../../api/dictionary";
import "./DictionarySelect.css";

function DictionarySelect({ dictionaryId, setDictionaryId, refresh }) {
    const [dictionaries, setDictionaries] = useState([]);
    const [showInfo, setShowInfo] = useState(false);

    useEffect(() => {
        if (dictionaries.length > 0 && !dictionaryId) {
            setDictionaryId(dictionaries[0].id);
        }
    }, [dictionaries]);

    useEffect(() => {
        getDictionaries()
            .then(setDictionaries)
            .catch(console.error);
    }, [refresh]);

    return (
        <div className="dictionary-select">
            <div className="dictionary-header">
                <div className="dictionary-header-text">
                    <h3>Dictionary</h3>
                </div>

                <button
                    className="dictionary-info-btn"
                    onClick={() => setShowInfo(prev => !prev)}
                >
                    ?
                </button>

                {showInfo && (
                    <div className="dictionary-info-box">
                        <p><strong>Dictionaries</strong> contain predefined keyword → emoji mappings.</p>
                        <p>Each dictionary represents a specific theme or language (e.g., English, Czech, Sports).</p>
                        <p>Used by the <strong>Exact Matches</strong> method to map words directly to emojis.</p>
                    </div>
                )}
            </div>

            <p className="dictionary-description">
                Predefined keyword → emoji mappings grouped by theme or language.
            </p>

            <select
                id="dictionary"
                value={dictionaryId || ""}
                onChange={(e) => setDictionaryId(Number(e.target.value))}
            >
                <option value="" disabled>Select a dictionary…</option>

                {dictionaries.map((d) => (
                    <option key={d.id} value={d.id}>
                        {d.name} ({d.language})
                    </option>
                ))}
            </select>
        </div>
    );
}

export default DictionarySelect;