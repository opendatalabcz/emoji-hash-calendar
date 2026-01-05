import { useState } from "react";
import './App.css';
import emojis from "emoji.json";

function App() {
    const [icsUrl, setIcsUrl] = useState("");
    const [method, setMethod] = useState("dictionary");
    const [result, setResult] = useState(null);
    const [error, setError] = useState("");
    const [preview, setPreview] = useState([]);
    const [userMappings, setUserMappings] = useState([]);
    const EMOJIS = emojis.slice(0, 5000).map(e => e.char);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setResult(null);
        setPreview([]);

        try {
            const response = await fetch("http://127.0.0.1:5000/calendar/transformation", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    ics_url: icsUrl,
                    method: method,
                    user_mapping: buildUserMapping()
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                setError(data.error || "Something went wrong");
                return;
            }

            setResult(data.ics_base64);
            setPreview(data.preview || []);
        } catch (err) {
            setError("Backend connection failed");
        }
    };

    const downloadFile = () => {
        const binary = atob(result);
        const bytes = new Uint8Array(binary.length);

        for (let i = 0; i < binary.length; i++) {
            bytes[i] = binary.charCodeAt(i);
        }

        const blob = new Blob([bytes], { type: "text/calendar" });
        const url = URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = "transformed.ics";
        a.click();
    };

    const buildUserMapping = () => {
        const mapping = {};
        userMappings.forEach(({ keyword, emoji }) => {
            if (keyword && emoji) {
                mapping[keyword.toLowerCase()] = emoji;
            }
        });
        return mapping;
    };

    return (
        <div className="app-container">
            <h1 className="app-title">Calendar Transformer</h1>

            <div className="app-layout">
                {/* SIDEBAR */}
                <div className="sidebar">
                    <h3>User-defined rules</h3>
                    <hr />

                    {userMappings.map((m, i) => (
                        <div key={i} className="rule-row">
                            <input
                                className="rule-keyword"
                                placeholder="keyword"
                                value={m.keyword}
                                onChange={(e) => {
                                    const copy = [...userMappings];
                                    copy[i].keyword = e.target.value;
                                    setUserMappings(copy);
                                }}
                            />

                            <select
                                className="rule-emoji"
                                value={m.emoji}
                                onChange={(e) => {
                                    const copy = [...userMappings];
                                    copy[i].emoji = e.target.value;
                                    setUserMappings(copy);
                                }}
                            >
                                <option value="">😀</option>
                                {EMOJIS.map((emoji) => (
                                    <option key={emoji} value={emoji}>
                                        {emoji}
                                    </option>
                                ))}
                            </select>

                            <button onClick={() =>
                                setUserMappings(userMappings.filter((_, idx) => idx !== i))
                            }>
                                ✕
                            </button>
                        </div>
                    ))}

                    <button onClick={() =>
                        setUserMappings([...userMappings, { keyword: "", emoji: "" }])
                    }>
                        ➕ Add rule
                    </button>
                </div>

                {/* MAIN */}
                <div className="main-column">
                    <form onSubmit={handleSubmit} className="panel">
                        <input
                            placeholder="Paste ICS URL here"
                            value={icsUrl}
                            onChange={(e) => setIcsUrl(e.target.value)}
                        />

                        <select value={method} onChange={(e) => setMethod(e.target.value)}>
                            <option value="dictionary">Dictionary</option>
                            <option value="embedding">Embedding</option>
                        </select>

                        <button>Transform</button>
                    </form>

                    {result && (
                        <button
                            onClick={downloadFile}
                            style={{ marginTop: "12px" }}
                        >
                            ⬇ Download .ics
                        </button>
                    )}

                    {preview.length > 0 && (
                        <div style={{ marginTop: "30px" }}>
                            <h3>Preview (first {preview.length} events)</h3>

                            <div className="preview-grid">
                                {preview.map((e, i) => (
                                    <div key={i} className="preview-card">
                                        <span className="preview-original">{e.title_original}</span>
                                        <span className="preview-arrow">→</span>
                                        <span className="preview-transformed">
                                            {e.title_transformed}
                                        </span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default App;
