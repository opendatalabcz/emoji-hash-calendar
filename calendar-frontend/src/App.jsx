import { useContext, useState, useEffect } from "react";
import RuleSidebar from "./components/RuleSidebar/RuleSidebar.jsx";
import Tester from "./components/Tester/Tester.jsx";
import Preview from "./components/Preview/Preview.jsx";
import TransformForm from "./components/TransformForm/TransformForm.jsx";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import { AuthContext } from "./auth/AuthContext";

import {
    getMappingSets,
    createMappingSet,
    getMappings,
    updateMappingSet   // ✅ IMPORTANT
} from "./api/mappings";

import "./App.css";

function App() {
    const { isLoggedIn, logout, token } = useContext(AuthContext);

    const [modal, setModal] = useState(null);
    const [result, setResult] = useState(null);
    const [preview, setPreview] = useState([]);
    const [userMappings, setUserMappings] = useState([]);
    const [mappingSets, setMappingSets] = useState([]);
    const [selectedSetId, setSelectedSetId] = useState(null);

    useEffect(() => {
        if (!isLoggedIn || !token) {
            setMappingSets([]);
            setSelectedSetId(null);
            setUserMappings([]);
            return;
        }

        getMappingSets(token)
            .then(setMappingSets)
            .catch(console.error);
    }, [isLoggedIn, token]);

    const handleSelectSet = (id) => {
        setSelectedSetId(id ? Number(id) : null);
    };

    const loadSet = async (setId) => {
        if (!setId || !token) return;

        const data = await getMappings(token, setId);

        setUserMappings(
            data.map(m => ({
                keyword: m.word,
                emoji: m.emoji,
            }))
        );

        setSelectedSetId(setId);
        return data; // ✅ important for sidebar
    };

    const createSet = async (name) => {
        if (!token) return;

        const newSet = await createMappingSet(token, name);

        setMappingSets(prev => [...prev, newSet]);
        setSelectedSetId(newSet.id);

        return newSet; // ✅ FIX
    };

    const saveSet = async (setId, payload) => {
        if (!token) return;
        await updateMappingSet(token, setId, payload);
    };

    const downloadFile = () => {
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
        <div className="app-container">
            <div className="auth-bar">
                <h1 className="app-title">Calendar Transformer</h1>

                <div className="auth-actions">
                    {!isLoggedIn ? (
                        <>
                            <button onClick={() => setModal("login")}>Login</button>
                            <button onClick={() => setModal("signup")}>Sign up</button>
                        </>
                    ) : (
                        <>
                            <span>Logged in</span>
                            <button onClick={logout}>Logout</button>
                        </>
                    )}
                </div>
            </div>

            {modal && (
                <div className="modal-layer">
                    {modal === "login" && <Login onClose={() => setModal(null)} />}
                    {modal === "signup" && <Signup onClose={() => setModal(null)} />}
                </div>
            )}

            <div className={`app-layout ${modal ? "dimmed" : ""}`}>
                <RuleSidebar
                    userMappings={userMappings}
                    setUserMappings={setUserMappings}
                    mappingSets={mappingSets}
                    selectedSetId={selectedSetId}
                    setSelectedSetId={handleSelectSet}
                    loadSet={loadSet}
                    createSet={createSet}
                    saveSet={saveSet}
                    isLoggedIn={isLoggedIn}
                />

                <div>
                    <TransformForm
                        userMappings={userMappings}
                        setPreview={setPreview}
                        setResult={setResult}
                    />

                    <Preview preview={preview} />

                    {result && (
                        <button onClick={downloadFile}>
                            Download .ics
                        </button>
                    )}
                </div>

                <Tester userMappings={userMappings} />
            </div>
        </div>
    );
}

export default App;