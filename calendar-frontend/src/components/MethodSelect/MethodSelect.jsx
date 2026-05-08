import { useState, useEffect } from "react";
import { getMethods } from "../../api/calendar";
import "./MethodSelect.css";

const METHOD_LABELS = {
    "dictionary": "Dictionary",
    "embedding - all-MiniLM-L6-v2": "MiniLM-L6",
    "embedding - all-MiniLM-L12-v2": "MiniLM-L12",
    "embedding - balanced": "Balanced",
    "embedding - multilingual": "Multilingual",
    "embedding - bge": "BGE",
};

function MethodSelect({ method, setMethod }) {
    const [methods, setMethods] = useState([]);

    useEffect(() => {
        getMethods()
            .then(setMethods)
            .catch(() => setMethods(Object.keys(METHOD_LABELS)));
    }, []);

    return (
        <div className="method-select">
            <div className="method-header">
                <h3>Transformation Method</h3>
                <p>
                    Choose how your calendar event titles
                    will be converted into emojis.
                </p>
            </div>

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