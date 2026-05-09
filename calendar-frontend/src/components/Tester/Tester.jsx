import { useState } from "react";
import { transformText } from "../../api/calendar.js";
import { buildUserMapping } from "../../utils/mapping.js";
import "./Tester.css";

function Tester({ userMappings, method, dictionaryId }) {
    const [testerInput, setTesterInput] = useState("");
    const [testerResult, setTesterResult] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleTesterSubmit = async (e) => {
        e.preventDefault();

        if (!testerInput.trim()) {
            setError("Text cannot be empty");
            return;
        }

        setError("");
        setTesterResult("");
        setLoading(true);

        try {
            const data = await transformText({
                text: testerInput,
                method,
                dictionary_id: dictionaryId,
                user_mapping: buildUserMapping(userMappings),
            });

            setTesterResult(data.emoji || "");
        } catch (err) {
            setTesterResult(err.message || "Backend connection failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="tester-column">
            <form onSubmit={handleTesterSubmit} className="panel">
                <h3>Text → Emoji Tester</h3>
                <input
                    placeholder="Type some text..."
                    value={testerInput}
                    onChange={(e) => setTesterInput(e.target.value)}
                />
                {error && <p className="tester-error">{error}</p>}
                <button disabled={loading}>
                    Test
                </button>
            </form>

            {loading && (
                <div className="tester-result loading">
                    Processing…
                </div>
            )}

            {!loading && testerResult && (
                <div className="tester-result">
                    Result: {testerResult}
                </div>
            )}
        </div>
    );
}

export default Tester;