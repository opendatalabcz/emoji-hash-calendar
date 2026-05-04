import {useContext, useState} from "react";
import RuleSidebar from "./components/RuleSidebar";
import Tester from "./components/Tester";
import Preview from "./components/Preview";
import TransformForm from "./components/TransformForm.jsx";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import { AuthContext } from "./auth/AuthContext";
import './App.css';

function App() {
    const { isLoggedIn, logout } = useContext(AuthContext);

    const [result, setResult] = useState(null);
    const [preview, setPreview] = useState([]);
    const [userMappings, setUserMappings] = useState([]);

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
            <h1 className="app-title">Calendar Transformer</h1>

            <div className="app-layout">
                {/* SIDEBAR */}
                <RuleSidebar
                    userMappings={userMappings}
                    setUserMappings={setUserMappings}
                />
                {/* MAIN */}
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


                {/* Text → Emoji Tester */}
                <Tester userMappings={userMappings} />
            </div>
        </div>
    );
}

export default App;
