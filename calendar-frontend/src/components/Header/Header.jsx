import "./Header.css";

function Header({ isLoggedIn, logout, setModal, user }) {
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
                            <span className="auth-hint">Sign in to save mapping sets</span>
                            <button className="btn-ghost" onClick={() => setModal("login")}>
                                Login
                            </button>

                            <button className="btn-primary" onClick={() => setModal("signup")}>
                                Sign up
                            </button>
                        </>
                    ) : (
                        <>
                            <span className="auth-username">
                                👤 {user?.username}
                            </span>

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