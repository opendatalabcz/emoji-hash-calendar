import { useState } from "react";
import './App.css';

function App() {
    const [icsUrl, setIcsUrl] = useState("");
    const [method, setMethod] = useState("dictionary");
    const [result, setResult] = useState(null);
    const [error, setError] = useState("");
    const [preview, setPreview] = useState([]);
    const [userMappings, setUserMappings] = useState([]);

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
        <div style={{ padding: "40px", fontFamily: "Arial" }}>
            <h1 style={{ textAlign: "center", marginBottom: "30px" }}>
                Calendar Transformer
            </h1>

            <div className="app-layout">

                {/* LEFT SIDEBAR */}
                <div className="sidebar">
                    <h3>User-defined rules</h3>
                    <hr style={{ opacity: 0.3, marginBottom: "12px" }} />

                    {userMappings.map((m, i) => (
                        <div
                            key={i}
                            style={{
                                display: "flex",
                                gap: "8px",
                                marginBottom: "8px",
                                alignItems: "center"
                            }}
                        >
                            <input
                                type="text"
                                placeholder="keyword"
                                value={m.keyword}
                                onChange={(e) => {
                                    const copy = [...userMappings];
                                    copy[i].keyword = e.target.value;
                                    setUserMappings(copy);
                                }}
                                style={{ flex: 1, padding: "6px" }}
                            />

                            <input
                                type="text"
                                placeholder="😀"
                                value={m.emoji}
                                onChange={(e) => {
                                    const copy = [...userMappings];
                                    copy[i].emoji = e.target.value;
                                    setUserMappings(copy);
                                }}
                                style={{ width: "60px", padding: "6px", textAlign: "center" }}
                            />

                            <button
                                type="button"
                                onClick={() =>
                                    setUserMappings(userMappings.filter((_, idx) => idx !== i))
                                }
                            >
                                ✕
                            </button>
                        </div>
                    ))}

                    <button
                        type="button"
                        onClick={() =>
                            setUserMappings([...userMappings, { keyword: "", emoji: "" }])
                        }
                        style={{ marginTop: "8px" }}
                    >
                        ➕ Add rule
                    </button>
                </div>

                {/* MAIN CONTENT */}
                <div className="main-column">
                    <form onSubmit={handleSubmit} className="panel">
                        <input
                            type="text"
                            placeholder="Paste ICS URL here"
                            value={icsUrl}
                            onChange={(e) => setIcsUrl(e.target.value)}
                            style={{ width: "100%", marginBottom: "12px" }}
                        />

                        <select
                            value={method}
                            onChange={(e) => setMethod(e.target.value)}
                            style={{ width: "100%", marginBottom: "20px" }}
                        >
                            <option value="dictionary">Dictionary</option>
                            <option value="embedding">Embedding</option>
                        </select>

                        <button>Transform</button>
                    </form>

                    {/* Preview BELOW the form */}
                    {preview.length > 0 && (
                        <div style={{ marginTop: "30px" }}>
                            <h3>Preview (first {preview.length} events)</h3>

                            <div style={{ display: "grid", gap: "12px", maxWidth: "700px" }}>
                                {preview.map((e, i) => (
                                    <div
                                        key={i}
                                        style={{
                                            padding: "12px 16px",
                                            borderRadius: "8px",
                                            border: "1px solid #e0e0e0",
                                            backgroundColor: "#fafafa",
                                            boxShadow: "0 1px 2px rgba(0,0,0,0.04)"
                                        }}
                                    >
                                        {/* Titles */}
                                        <div style={{ marginBottom: "6px" }}>
                                            <span style={{ opacity: 0.6 }}>{e.title_original}</span>
                                            <span style={{ margin: "0 8px", opacity: 0.5 }}>→</span>
                                            <strong style={{ fontSize: "1.05em" }}>
                                                {e.title_transformed}
                                            </strong>
                                        </div>
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
