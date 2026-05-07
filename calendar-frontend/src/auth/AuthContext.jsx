import { createContext, useState, useEffect, useCallback } from "react";
import { getToken, setToken as saveToken, logout as clearToken } from "./auth";

const API_URL = import.meta.env.VITE_API_URL;
export const AuthContext = createContext();

function isTokenExpired(token) {
    try {
        const payload = JSON.parse(atob(token.split(".")[1]));
        return payload.exp * 1000 < Date.now();
    } catch {
        return true;
    }
}

export function AuthProvider({ children }) {
    const [token, setTokenState] = useState(null);
    const [user, setUser] = useState(null);
    const [sessionExpired, setSessionExpired] = useState(false);

    const logout = useCallback((expired = false) => {
        clearToken();
        setTokenState(null);
        setUser(null);
        if (expired) setSessionExpired(true);
    }, []);

    const fetchUser = useCallback(async (token) => {
        const res = await fetch(`${API_URL}/api/users/me`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        if (res.status === 401) {
            logout(true);
            return;
        }
        if (!res.ok) return;
        const data = await res.json();
        setUser(data);
    }, [logout]);

    useEffect(() => {
        const storedToken = getToken();
        if (!storedToken) return;

        if (isTokenExpired(storedToken)) {
            logout(true);
            return;
        }

        setTokenState(storedToken);
        fetchUser(storedToken);
    }, []);

    useEffect(() => {
        const interval = setInterval(() => {
            const currentToken = getToken();
            if (currentToken && isTokenExpired(currentToken)) {
                logout(true);
            }
        }, 60 * 1000);

        return () => clearInterval(interval);
    }, [logout]);

    const login = async (newToken) => {
        saveToken(newToken);
        setTokenState(newToken);
        setSessionExpired(false);
        await fetchUser(newToken);
    };

    return (
        <AuthContext.Provider value={{ token, user, login, logout, isLoggedIn: !!token, sessionExpired, setSessionExpired }}>
            {sessionExpired && (
                <div className="session-expired-banner">
                    Your session has expired. Please{" "}
                    <button onClick={() => {
                        setSessionExpired(false);
                    }}>
                        Log in again
                    </button>
                    <button onClick={() => setSessionExpired(false)}>✕</button>
                </div>
            )}
            {children}
        </AuthContext.Provider>
    );
}