import { useState } from "react";
import { transformCalendar } from "../../api/calendar.js";
import { buildUserMapping } from "../../utils/mapping.js";
import "./TransformForm.css";

function TransformForm({ userMappings, setPreview, setResult }) {
    const [icsUrl, setIcsUrl] = useState("");
    const [method, setMethod] = useState("dictionary");
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setResult(null);
        setPreview([]);

        try {
            const data = await transformCalendar({
                ics_url: icsUrl,
                method: method,
                dictionary_id: 1,
                user_mapping: buildUserMapping(userMappings),
            });

            setResult(data.ics_base64);
            setPreview(data.preview || []);
        } catch (err) {
            setError(err.message || "Backend connection failed");
        }
    };

    return (
        <div className="main-column">
            <form onSubmit={handleSubmit} className="panel">
                <input
                    placeholder="Paste ICS URL here"
                    value={icsUrl}
                    onChange={(e) => setIcsUrl(e.target.value)}
                />

                <select value={method} onChange={(e) => setMethod(e.target.value)}>
                    <option value="dictionary">Dictionary</option>
                    <option value="embedding - all-MiniLM-L6-v2">
                        Embedding - all-MiniLM-L6-v2
                    </option>
                    <option value="embedding - all-MiniLM-L12-v2">
                        Embedding - all-MiniLM-L12-v2
                    </option>
                    <option value="embedding - balanced">
                        Embedding - balanced
                    </option>
                    <option value="embedding - multilingual">
                        Embedding - multilingual
                    </option>
                    <option value="embedding - bge">
                        Embedding - bge
                    </option>
                </select>

                <button>Transform</button>
            </form>

            {error && (
                <div style={{ marginTop: "12px", color: "red" }}>
                    {error}
                </div>
            )}
        </div>
    );
}

export default TransformForm;