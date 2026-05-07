import "./MethodSelect.css";

function MethodSelect({ method, setMethod }) {
    return (
        <div className="method-select">
            <div className="method-header">
                <h3>Transformation Method</h3>

                <p>
                    Choose how your calendar event titles
                    will be converted into emojis.
                </p>
            </div>

            <select
                value={method}
                onChange={(e) => setMethod(e.target.value)}
            >
                <option value="dictionary">Dictionary</option>
                <option value="embedding - all-MiniLM-L6-v2">MiniLM-L6</option>
                <option value="embedding - all-MiniLM-L12-v2">MiniLM-L12</option>
                <option value="embedding - balanced">Balanced</option>
                <option value="embedding - multilingual">Multilingual</option>
                <option value="embedding - bge">BGE</option>
            </select>
        </div>
    );
}

export default MethodSelect;