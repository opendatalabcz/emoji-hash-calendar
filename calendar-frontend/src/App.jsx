import { useContext, useState, useEffect } from "react";
import Header from "./components/Header/Header.jsx"
import RuleSidebar from "./components/RuleSidebar/RuleSidebar.jsx";
import Tester from "./components/Tester/Tester.jsx";
import Preview from "./components/Preview/Preview.jsx";
import Login from "./components/Login/Login.jsx";
import Signup from "./components/Signup/Signup.jsx";
import Footer from "./components/Footer/Footer.jsx"
import { AuthContext } from "./auth/AuthContext";

import {
    getMappingSets,
    createMappingSet,
    getMappings,
    updateMappingSet
} from "./api/mappings";

import "./App.css";
import SourceInput from "./components/SourceInput/SourceInput.jsx";
import ActionButtons from "./components/ActionButtons/ActionButtons.jsx";
import MethodSelect from "./components/MethodSelect/MethodSelect.jsx";
import DictionarySelect from "./components/DictionarySelect/DictionarySelect.jsx";
import AdminDictionaryPanel from "./components/AdminDictionaryPanel/AdminDictionaryPanel.jsx";
import AdminUserPanel from "./components/AdminUserPanel/AdminUserPanel.jsx";

function App() {
    const { isLoggedIn, logout, token, user, sessionExpired, setSessionExpired } = useContext(AuthContext);
    const isAdmin = user?.is_admin === true;

    const [modal, setModal] = useState(null);
    const [result, setResult] = useState(null);
    const [preview, setPreview] = useState([]);
    const [userMappings, setUserMappings] = useState([]);
    const [mappingSets, setMappingSets] = useState([]);
    const [selectedSetId, setSelectedSetId] = useState(null);
    const [icsUrl, setIcsUrl] = useState("");
    const [method, setMethod] = useState("dictionary");
    const [isTransforming, setIsTransforming] = useState(false);
    const [isMobile, setIsMobile] = useState(window.innerWidth <= 1100);
    const [showPreviewModal, setShowPreviewModal] = useState(false);
    const [dictionaryId, setDictionaryId] = useState(null);
    const [adminOpen, setAdminOpen] = useState(false);
    const [dictionaryRefresh, setDictionaryRefresh] = useState(0);
    const [sourceMode, setSourceMode] = useState("url");
    const [icsFile, setIcsFile] = useState(null);


    useEffect(() => {
        const handler = () => setIsMobile(window.innerWidth <= 1100);
        window.addEventListener("resize", handler);
        return () => window.removeEventListener("resize", handler);
    }, []);

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

    useEffect(() => {
        if (sessionExpired && isLoggedIn) {
            setModal("login");
        }
    }, [sessionExpired, isLoggedIn]);

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
        return data;
    };

    const createSet = async (name) => {
        if (!token) return;

        const newSet = await createMappingSet(token, name);

        setMappingSets(prev => [...prev, newSet]);
        setSelectedSetId(newSet.id);

        return newSet;
    };

    const saveSet = async (setId, payload) => {
        if (!token) return;
        await updateMappingSet(token, setId, payload);
    };

    return (
        <div className="page">
            <Header
                isLoggedIn={isLoggedIn}
                logout={logout}
                setModal={setModal}
                user={user}
                isAdmin={isAdmin}
                onToggleAdmin={setAdminOpen}
            />
            {isAdmin && adminOpen && (
                <div className="admin-dropdown admin-flex">
                    <AdminUserPanel />
                    <AdminDictionaryPanel onRefresh={() => setDictionaryRefresh(r => r + 1)} />
                </div>
            )}
            <section className="page-intro">
                <p>
                    Paste your calendar's ICS URL, pick a transformation method, and hit{" "}
                    <strong>Transform Calendar</strong>. Download the result or get a subscription
                    link to keep your calendar in sync automatically.
                </p>
                <p>
                    <strong>Exact Matches</strong> matches exact keywords in event titles.
                    The embedding models find the closest emojis by meaning — better for varied or unpredictable titles.
                </p>
            </section>
            <div className="app-container">
                {modal && (
                    <div className="modal-layer">
                        {modal === "login" && <Login onClose={() => setModal(null)} />}
                        {modal === "signup" && <Signup onClose={() => setModal(null)} />}
                    </div>
                )}

                <div className={`app-layout ${modal ? "dimmed" : ""}`}>
                    <div className="layout-left column-left">
                        <SourceInput
                            icsUrl={icsUrl}
                            setIcsUrl={setIcsUrl}
                            icsFile={icsFile}
                            setIcsFile={setIcsFile}
                            sourceMode={sourceMode}
                            setSourceMode={setSourceMode}
                        />
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
                    </div>

                    <div className="layout-center column-center">
                        <MethodSelect
                            method={method}
                            setMethod={setMethod}
                        />
                        <DictionarySelect
                            dictionaryId={dictionaryId}
                            setDictionaryId={setDictionaryId}
                            refresh={dictionaryRefresh}
                        />
                        <ActionButtons
                            icsUrl={icsUrl}
                            icsFile={icsFile}
                            sourceMode={sourceMode}
                            method={method}
                            setMethod={setMethod}
                            userMappings={userMappings}
                            dictionaryId={dictionaryId}
                            setPreview={setPreview}
                            setResult={setResult}
                            result={result}
                            setIsTransforming={setIsTransforming}
                            onTransformDone={() => isMobile && setShowPreviewModal(true)}
                        />
                        {isMobile && preview.length > 0 && (
                            <button
                                className="show-preview-btn"
                                onClick={() => setShowPreviewModal(true)}
                            >
                                Show Preview ({preview.length} events)
                            </button>
                        )}
                    </div>
                    <div className="layout-right column-right">
                        {!isMobile && (
                            <>
                                <Tester
                                    userMappings={userMappings}
                                    method={method}
                                    dictionaryId={dictionaryId}
                                />
                                <Preview
                                    preview={preview}
                                    loading={isTransforming}
                                />
                            </>
                        )}
                    </div>
                </div>
            </div>

            {isMobile && showPreviewModal && (
                <div className="preview-modal-overlay" onClick={() => setShowPreviewModal(false)}>
                    <div className="preview-modal" onClick={e => e.stopPropagation()}>
                        <div className="preview-modal-header">
                            <h3>Preview</h3>
                            <button
                                className="preview-modal-close"
                                onClick={() => setShowPreviewModal(false)}
                            >
                                ✕
                            </button>
                        </div>
                        <Preview preview={preview} loading={isTransforming} />
                    </div>
                </div>
            )}
            <Footer
            />
        </div>
    );
}

export default App;