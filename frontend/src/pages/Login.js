import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";
import "./Login.css";

function getAuthPayload(data) {
	const token = data?.token || data?.access_token || data?.jwt || null;
	const user = data?.user || null;
	return { token, user };
}

export default function Login() {
	const navigate = useNavigate();

	const [formData, setFormData] = useState({ email: "", password: "" });
	const [error, setError] = useState("");
	const [isSubmitting, setIsSubmitting] = useState(false);

	const handleChange = (event) => {
		const { name, value } = event.target;
		setFormData((prev) => ({ ...prev, [name]: value }));
	};

	const handleSubmit = async (event) => {
		event.preventDefault();
		setError("");
		setIsSubmitting(true);

		try {
			const response = await api.post("/api/auth/login", formData);
			const { token, user } = getAuthPayload(response.data);

			if (!token) {
				throw new Error("Login response did not include a token.");
			}

			localStorage.setItem("token", token);
			if (user) {
				localStorage.setItem("user", JSON.stringify(user));
			}
			navigate("/dashboard", { replace: true });
		} catch (err) {
			const message =
				err.response?.data?.message ||
				err.response?.data?.error ||
				err.message ||
				"Login failed. Please try again.";
			setError(message);
		} finally {
			setIsSubmitting(false);
		}
	};

	return (
		<main className="login-page">
			<section className="login-card" aria-label="Login form">
				<h1 className="login-title">Welcome Back</h1>
				<p className="login-subtitle">Sign in to continue to your dashboard.</p>

				<form className="login-form" onSubmit={handleSubmit}>
					<label htmlFor="email" className="login-label">
						Email
					</label>
					<input
						id="email"
						name="email"
						type="email"
						autoComplete="email"
						value={formData.email}
						onChange={handleChange}
						required
						className="login-input"
					/>

					<label htmlFor="password" className="login-label">
						Password
					</label>
					<input
						id="password"
						name="password"
						type="password"
						autoComplete="current-password"
						value={formData.password}
						onChange={handleChange}
						required
						className="login-input"
					/>

					{error ? (
						<p className="login-error" role="alert">
							{error}
						</p>
					) : null}

					<button type="submit" className="login-button" disabled={isSubmitting}>
						{isSubmitting ? "Signing in..." : "Sign In"}
					</button>
				</form>

				<p className="login-register-text">
					Do not have an account? <Link to="/register">Create one</Link>
				</p>
			</section>
		</main>
	);
}
