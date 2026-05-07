import { useState } from "react";
import { transformCalendar, generateCalendarLink } from "../../api/calendar.js";
import { buildUserMapping } from "../../utils/mapping.js";

import "./ActionButtons.css";

function ActionButtons({
                           icsUrl,
                           method,
                           userMappings,
                           setPreview,
                           setResult,
                           result,
                           setIsTransforming,
                           onTransformDone
                       }) {

    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [feedUrl, setFeedUrl] = useState(null);
    const [copied, setCopied] = useState(false);

    const handleTransform = async () => {
        try {
            setLoading(true);
            setIsTransforming(true);
            setSuccess(false);
            setPreview([]);
            setResult(null);
            setFeedUrl(null);

            const data = await transformCalendar({
                ics_url: icsUrl,
                method,
                dictionary_id: 1,
                user_mapping: buildUserMapping(userMappings),
            });

            setResult(data.ics_base64);
            setPreview(data.preview || []);
            setSuccess(true);
            onTransformDone?.();

            setTimeout(() => setSuccess(false), 2000);
        } catch (err) {
            alert(err.message || "Backend error");
        } finally {
            setLoading(false);
            setIsTransforming(false);
        }
    };

    const handleGetFeedLink = async () => {
        try {
            const data = await generateCalendarLink({
                base_url: `${import.meta.env.VITE_API_URL}/api/calendars`,
                ics_url: icsUrl,
                method,
                dictionary_id: 1,
                user_mapping: buildUserMapping(userMappings),
            });
            setFeedUrl(data.url);
            await navigator.clipboard.writeText(data.url);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        } catch (err) {
            alert(err.message || "Failed to generate link");
        }
    };

    const downloadFile = () => {
        if (!result) return;

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
        <div className="action-buttons">

            <button
                className={`
                    transform-btn
                    ${loading ? "loading" : ""}
                    ${success ? "success" : ""}
                `}
                onClick={handleTransform}
                disabled={loading}
            >

                {loading ? (
                    <span className="spinner"></span>
                ) : success ? (
                    <>
                        <span className="checkmark">✓</span>
                        Transformed
                    </>
                ) : (
                    "Transform Calendar"
                )}

            </button>

            {result && (
                <div className="result-actions fade-in">

                    <button className="secondary-btn" onClick={downloadFile}>
                        ⬇ Download .ics
                    </button>
                    <button className="secondary-btn" onClick={handleGetFeedLink}>
                        {copied ? "✓ Copied!" : "🔗 Copy Feed Link"}
                    </button>

                </div>
            )}
            {feedUrl && (
                <div className="feed-url fade-in">
                    <input readOnly value={feedUrl} onClick={e => e.target.select()} />
                    <p className="feed-url-hint">
                        Paste this URL into Google Calendar → "Other calendars" → "From URL"
                    </p>
                </div>
            )}

        </div>
    );
}

export default ActionButtons;