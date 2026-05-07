import { useState } from "react";
import { transformText } from "../../api/calendar.js";
import { buildUserMapping } from "../../utils/mapping.js";
import "./Tester.css";

function Tester({ userMappings, method }) {
    const [testerInput, setTesterInput] = useState("");
    const [testerResult, setTesterResult] = useState("");

    const handleTesterSubmit = async (e) => {
        e.preventDefault();
        setTesterResult("");

        try {
            const data = await transformText({
                text: testerInput,
                method,
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
            <form onSubmit={handleTesterSubmit} className="panel">
                <h3>Text → Emoji Tester</h3>
                <input
                    placeholder="Type some text..."
                    value={testerInput}
                    onChange={(e) => setTesterInput(e.target.value)}
                />

                <button>Test</button>
            </form>

            {testerResult && (
                <div className="tester-result">
                    Result: {testerResult}
                </div>
            )}
        </div>
    );
}

export default Tester;