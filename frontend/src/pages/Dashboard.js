import { useEffect, useMemo, useState } from "react";
import { Link, Navigate, useLocation } from "react-router-dom";
import api from "../services/api";
import "./Dashboard.css";

const NAV_LINKS = [
	{ to: "/dashboard", label: "Dashboard" },
	{ to: "/jobs", label: "Job Tracker" },
	{ to: "/resume", label: "Resume Generator" },
	{ to: "/cover-letter", label: "Cover Letter" },
	{ to: "/analytics", label: "Analytics" },
];

function toNumber(value) {
	const parsed = Number(value);
	return Number.isFinite(parsed) ? parsed : 0;
}

export default function Dashboard() {
	const location = useLocation();
	const token = localStorage.getItem("token");

	const [stats, setStats] = useState({
		total_jobs: 0,
		applied: 0,
		interviews: 0,
		offers: 0,
	});
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState("");

	useEffect(() => {
		let isMounted = true;

		async function fetchSummary() {
			setLoading(true);
			setError("");

			try {
				const response = await api.get("/api/analytics/summary");
				if (!isMounted) {
					return;
				}

				const data = response.data || {};
				setStats({
					total_jobs: toNumber(data.total_jobs ?? data.totalJobs),
					applied: toNumber(data.applied),
					interviews: toNumber(data.interviews),
					offers: toNumber(data.offers),
				});
			} catch (err) {
				if (!isMounted) {
					return;
				}

				const message =
					err.response?.data?.message ||
					err.response?.data?.error ||
					"Unable to load dashboard stats right now.";
				setError(message);
			} finally {
				if (isMounted) {
					setLoading(false);
				}
			}
		}

		fetchSummary();

		return () => {
			isMounted = false;
		};
	}, []);

	const cards = useMemo(
		() => [
			{ label: "Total Jobs", value: stats.total_jobs },
			{ label: "Applied", value: stats.applied },
			{ label: "Interviews", value: stats.interviews },
			{ label: "Offers", value: stats.offers },
		],
		[stats]
	);

	if (!token) {
		return <Navigate to="/login" replace state={{ from: location }} />;
	}

	return (
		<div className="dashboard-page">
			<nav className="dashboard-nav" aria-label="Main navigation">
				<div className="dashboard-brand">AI Job Hunt</div>
				<div className="dashboard-links">
					{NAV_LINKS.map((link) => (
						<Link key={link.to} to={link.to} className="dashboard-link">
							{link.label}
						</Link>
					))}
				</div>
			</nav>

			<main className="dashboard-main">
				<header className="dashboard-header">
					<h1>Dashboard</h1>
					<p>Track your job search progress at a glance.</p>
				</header>

				{loading ? <p className="dashboard-status">Loading stats...</p> : null}
				{error ? (
					<p className="dashboard-error" role="alert">
						{error}
					</p>
				) : null}

				{!loading && !error ? (
					<section className="dashboard-grid" aria-label="Job stats">
						{cards.map((card) => (
							<article key={card.label} className="stat-card">
								<p className="stat-label">{card.label}</p>
								<p className="stat-value">{card.value}</p>
							</article>
						))}
					</section>
				) : null}
			</main>
		</div>
	);
}
