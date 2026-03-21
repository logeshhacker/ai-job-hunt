import { createContext, useContext, useMemo, useState } from "react";
import api from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
	const [user, setUser] = useState(null);
	const [token, setToken] = useState(localStorage.getItem("token") || null);

	const login = (authToken, userData) => {
		localStorage.setItem("token", authToken);
		setToken(authToken);
		setUser(userData);
	};

	const logout = () => {
		localStorage.removeItem("token");
		setToken(null);
		setUser(null);
	};

	const register = async (payload) => {
		const response = await api.post("/api/auth/register", payload);
		return response.data;
	};

	const value = useMemo(
		() => ({
			user,
			token,
			login,
			logout,
			register,
		}),
		[user, token]
	);

	return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
	const context = useContext(AuthContext);

	if (!context) {
		throw new Error("useAuth must be used within an AuthProvider");
	}

	return context;
}
