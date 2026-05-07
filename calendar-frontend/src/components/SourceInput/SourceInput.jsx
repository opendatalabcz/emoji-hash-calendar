import "./SourceInput.css";

function SourceInput({ icsUrl, setIcsUrl }) {
    return (
        <div className="panel">
            <h3>Paste source ICS URL here</h3>
            <input
                placeholder="Paste ICS URL here"
                value={icsUrl}
                onChange={(e) => setIcsUrl(e.target.value)}
            />
        </div>
    );
}

export default SourceInput;