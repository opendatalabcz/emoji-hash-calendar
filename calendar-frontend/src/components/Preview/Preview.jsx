import "./Preview.css";

function Preview({ preview, loading }) {

    if (loading) {
        return (
            <div className="preview-loading">
                <div className="preview-spinner"></div>
                <p>Transforming events...</p>
            </div>
        );
    }

    if (!preview || preview.length === 0) {
        return null;
    }

    return (
        <div className="preview-section">

            <div className="preview-header">
                <h3>
                    Preview
                </h3>

                <p>
                    {preview.length} transformed events
                </p>
            </div>

            <div className="preview-grid">

                {preview.map((e, i) => (
                    <div
                        key={i}
                        className="preview-card"
                        style={{
                            animationDelay: `${i * 70}ms`
                        }}
                    >

                        <span className="preview-original">
                            {e.title_original}
                        </span>

                        <span className="preview-arrow">
                            →
                        </span>

                        <span className="preview-transformed">
                            {e.title_transformed === "?" || !e.title_transformed
                                ? <span className="preview-no-match">no match</span>
                                : e.title_transformed
                            }
                        </span>

                    </div>
                ))}

            </div>

        </div>
    );
}

export default Preview;