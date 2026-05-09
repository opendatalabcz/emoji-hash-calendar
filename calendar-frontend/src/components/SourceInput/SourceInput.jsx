import "./SourceInput.css";

function SourceInput({ icsUrl, setIcsUrl, icsFile, setIcsFile, sourceMode, setSourceMode }) {
    return (
        <div className="panel source-panel">

            <div className="source-toggle">
                <button
                    className={sourceMode === "url" ? "active" : ""}
                    onClick={() => {
                        setSourceMode("url");
                        setIcsFile(null);
                    }}
                >
                    URL
                </button>

                <button
                    className={sourceMode === "file" ? "active" : ""}
                    onClick={() => {
                        setSourceMode("file");
                        setIcsUrl("");
                    }}
                >
                    File
                </button>
            </div>

            {sourceMode === "url" && (
                <>
                    <h3>Paste source ICS URL</h3>
                    <p className="source-description">
                        Enter a public or private ICS link from Google Calendar, Outlook, Apple Calendar, or any other provider.
                    </p>
                    <input
                        type="url"
                        placeholder="https://example.com/calendar.ics"
                        value={icsUrl}
                        onChange={(e) => setIcsUrl(e.target.value)}
                    />
                </>
            )}

            {sourceMode === "file" && (
                <>
                    <h3>Upload ICS File</h3>
                    <p className="source-description">
                        Upload a .ics file exported from your calendar app. We’ll transform it locally.
                    </p>
                    <input
                        type="file"
                        accept=".ics"
                        onChange={(e) => setIcsFile(e.target.files[0] || null)}
                    />
                </>
            )}
        </div>
    );
}

export default SourceInput;
