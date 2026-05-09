import "./Header.css";
import {useState} from "react";

function Header({ isLoggedIn, logout, setModal, user, isAdmin, onToggleAdmin }) {
    const [adminOpen, setAdminOpen] = useState(false);

    const toggleAdmin = () => {
        const next = !adminOpen;
        setAdminOpen(next);
        onToggleAdmin(next);
    };

    return (
        <header>
            <div className="header-content">
                <div className="header-left">
                    <h1 className="app-title">
                        Calendar Emoji Transformer
                    </h1>
                    <p>
                        Transform calendar event titles into emojis 🙂
                    </p>
                </div>

                <div className="auth-actions">
                    {!isLoggedIn ? (
                        <>
                            <span className="auth-hint">Sign in to save optional mapping</span>
                            <button className="btn-ghost" onClick={() => setModal("login")}>
                                Login
                            </button>

                            <button className="btn-primary" onClick={() => setModal("signup")}>
                                Sign up
                            </button>
                        </>
                    ) : (
                        <>
                            <div className="auth-user-block">
                                <span className="auth-username">
                                    👤 {user?.username}
                                </span>
                                {isAdmin && (
                                    <span className="admin-badge">
                                    👑 Admin
                                </span>
                                )}
                            </div>
                            {isAdmin && (
                                <button className="btn-ghost admin-tools-btn" onClick={toggleAdmin}>
                                    Admin Tools ▾
                                </button>
                            )}
                            <button className="btn-ghost danger" onClick={logout}>
                                Logout
                            </button>
                        </>
                    )}
                </div>
            </div>
        </header>
    );
}

export default Header;