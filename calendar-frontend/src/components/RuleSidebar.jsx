import emojis from "emoji.json";

function RuleSidebar({ userMappings, setUserMappings }) {
    const EMOJIS = emojis.slice(0, 5000).map(e => e.char);

    const updateKeyword = (index, value) => {
        const copy = [...userMappings];
        copy[index].keyword = value;
        setUserMappings(copy);
    };

    const updateEmoji = (index, value) => {
        const copy = [...userMappings];
        copy[index].emoji = value;
        setUserMappings(copy);
    };

    const removeRule = (index) => {
        setUserMappings(userMappings.filter((_, i) => i !== index));
    };

    const addRule = () => {
        setUserMappings([...userMappings, { keyword: "", emoji: "" }]);
    };

    return (
        <div className="sidebar">
            <h3>User-defined rules</h3>
            <hr />

            {userMappings.map((m, i) => (
                <div key={i} className="rule-row">
                    <input
                        className="rule-keyword"
                        placeholder="keyword"
                        value={m.keyword}
                        onChange={(e) => updateKeyword(i, e.target.value)}
                    />

                    <select
                        className="rule-emoji"
                        value={m.emoji}
                        onChange={(e) => updateEmoji(i, e.target.value)}
                    >
                        <option value="">?</option>
                        {EMOJIS.map((emoji) => (
                            <option key={emoji} value={emoji}>
                                {emoji}
                            </option>
                        ))}
                    </select>

                    <button onClick={() => removeRule(i)}>
                        ❌
                    </button>
                </div>
            ))}

            <button onClick={addRule}>
                ➕ Add rule
            </button>
        </div>
    );
}

export default RuleSidebar;