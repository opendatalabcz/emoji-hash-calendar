import { useState } from "react";
import { transformText } from "../api/calendar";
import { buildUserMapping } from "../utils/mapping";

function Tester({ userMappings }) {
    const [testerInput, setTesterInput] = useState("");
    const [testerMethod, setTesterMethod] = useState("dictionary");
    const [testerResult, setTesterResult] = useState("");

    const handleTesterSubmit = async (e) => {
        e.preventDefault();
        setTesterResult("");

        try {
            const data = await transformText({
                text: testerInput,
                method: testerMethod,
                dictionary_id: 1,
                user_mapping: buildUserMapping(userMappings),
            });

            setTesterResult(data.emoji || "");
        } catch (err) {
            setTesterResult(err.message || "Backend connection failed");
        }
    };

    return (
        <div className="tester-column">
            <h3>Text → Emoji Tester</h3>
            <hr />

            <form onSubmit={handleTesterSubmit} className="panel">
                <input
                    placeholder="Type some text..."
                    value={testerInput}
                    onChange={(e) => setTesterInput(e.target.value)}
                />

                <select
                    value={testerMethod}
                    onChange={(e) => setTesterMethod(e.target.value)}
                >
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

            {testerResult && (
                <div style={{ marginTop: "12px", fontSize: "24px" }}>
                    Result: {testerResult}
                </div>
            )}
        </div>
    );
}

export default Tester;