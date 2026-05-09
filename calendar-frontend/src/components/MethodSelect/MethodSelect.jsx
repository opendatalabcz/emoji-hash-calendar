import { useState, useEffect } from "react";
import { getMethods } from "../../api/calendar";
import "./MethodSelect.css";

const METHOD_LABELS = {
    "dictionary": "Exact Matches",
    "embedding - all-MiniLM-L6-v2": "Semantic Match (MiniLM‑L6)",
    "embedding - all-MiniLM-L12-v2": "Semantic Match+ (MiniLM‑L12)",
    "embedding - balanced": "Balanced AI Matching",
    "embedding - multilingual": "Multilingual AI Matching",
    "embedding - bge": "Advanced Semantic (BGE)",
};

function MethodSelect({ method, setMethod }) {
    const [showInfo, setShowInfo] = useState(false);
    const [methods, setMethods] = useState([]);

    useEffect(() => {
        getMethods()
            .then(setMethods)
            .catch(() => setMethods(Object.keys(METHOD_LABELS)));
    }, []);

    return (
        <div className="method-select">
            <div className="method-header">
                <div className="method-header-text">
                    <h3>Transformation Method</h3>
                </div>

                <button
                    className="method-info-btn"
                    onClick={() => setShowInfo(prev => !prev)}
                >
                    ?
                </button>
                {showInfo && (
                    <div className="method-info-box">
                        <p><strong>Exact Matches</strong> — Matches event titles using exact keywords defined by you and in chosen internal dictionary.</p>
                        <p><strong>Semantic Match (MiniLM‑L6)</strong> — Fast AI meaning-based matching.</p>
                        <p><strong>Semantic Match+ (MiniLM‑L12)</strong> — More accurate semantic matching.</p>
                        <p><strong>Balanced AI Matching</strong> — Good all-around AI model.</p>
                        <p><strong>Multilingual AI Matching</strong> — Best for non‑English calendars.</p>
                        <p><strong>Advanced Semantic (BGE)</strong> — Highest accuracy for complex titles.</p>
                    </div>
                )}
            </div>
            <p className="dictionary-description">
                Choose how your calendar event titles will be converted into emojis.
            </p>
            <select value={method} onChange={(e) => setMethod(e.target.value)}>
                {methods.map(m => (
                    <option key={m} value={m}>
                        {METHOD_LABELS[m] ?? m}
                    </option>
                ))}
            </select>
        </div>
    );
}

export default MethodSelect;