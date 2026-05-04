import { createContext, useState, useEffect } from "react";
import { getToken, setToken as saveToken, logout as clearToken } from "./auth";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [token, setTokenState] = useState(null);

    // Load token on app start (important for refresh persistence)
    useEffect(() => {
        const storedToken = getToken();
        if (storedToken) {
            setTokenState(storedToken);
        }
    }, []);

    const login = (newToken) => {
        saveToken(newToken);      // localStorage
        setTokenState(newToken);  // React state
    };

    const logout = () => {
        clearToken();
        setTokenState(null);
    };

    const isLoggedIn = !!token;

    return (
        <AuthContext.Provider
            value={{
                token,
                login,
                logout,
                isLoggedIn,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}