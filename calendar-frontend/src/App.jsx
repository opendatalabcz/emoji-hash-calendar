import { useState } from "react";
import './App.css';

function App() {
    const [icsUrl, setIcsUrl] = useState("");
    const [method, setMethod] = useState("dictionary");
    const [result, setResult] = useState(null);
    const [error, setError] = useState("");
    const [preview, setPreview] = useState([]);

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

    return (
        <div style={{ padding: "40px", fontFamily: "Arial" }}>
            <h1>Calendar Transformer</h1>

            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Paste ICS URL here"
                    value={icsUrl}
                    onChange={(e) => setIcsUrl(e.target.value)}
                    style={{ width: "400px", padding: "10px" }}
                />

                <div style={{ marginTop: "10px" }}>
                    <select value={method} onChange={(e) => setMethod(e.target.value)}>
                        <option value="dictionary">Dictionary</option>
                        <option value="embedding">Embedding</option>
                    </select>
                </div>

                <button style={{ marginTop: "20px", padding: "10px 20px" }}>
                    Transform
                </button>
            </form>

            {error && <p style={{ color: "red" }}>{error}</p>}

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

            {result && preview.length > 0 && (
                <button style={{ marginTop: "20px" }} onClick={downloadFile}>
                    Download .ics
                </button>
            )}
        </div>
    );
}

export default App;
