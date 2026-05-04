import "./Preview.css";

function Preview({ preview }) {
    if (!preview || preview.length === 0) {
        return null;
    }

    return (
        <div style={{ marginTop: "30px" }}>
            <h3>Preview (first {preview.length} events)</h3>

            <div className="preview-grid">
                {preview.map((e, i) => (
                    <div key={i} className="preview-card">
            <span className="preview-original">
              {e.title_original}
            </span>

                        <span className="preview-arrow">
              →
            </span>

                        <span className="preview-transformed">
              {e.title_transformed}
            </span>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Preview;