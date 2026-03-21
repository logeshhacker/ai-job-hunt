import { useMemo, useState } from "react";
import api from "../services/api";
import "./ResumeGenerator.css";

function normalizeGeneratedResume(data) {
	if (!data) {
		return "";
	}

	if (typeof data === "string") {
		return data;
	}

	return (
		data.ats_resume ||
		data.generated_resume ||
		data.resume ||
		data.result ||
		""
	);
}

export default function ResumeGenerator() {
	const [resumeText, setResumeText] = useState("");
	const [jobDescription, setJobDescription] = useState("");
	const [generatedResume, setGeneratedResume] = useState("");
	const [error, setError] = useState("");
	const [isSubmitting, setIsSubmitting] = useState(false);
	const [copyStatus, setCopyStatus] = useState("");

	const canSubmit = useMemo(
		() => resumeText.trim() && jobDescription.trim() && !isSubmitting,
		[resumeText, jobDescription, isSubmitting]
	);

	const handleSubmit = async (event) => {
		event.preventDefault();
		setError("");
		setCopyStatus("");
		setIsSubmitting(true);

		try {
			const token = localStorage.getItem("token");
			if (!token) {
				throw new Error("You must be logged in to generate an ATS resume.");
			}

			const response = await api.post(
				"/api/resume/generate-ats",
				{
					resume_text: resumeText,
					job_description: jobDescription,
				},
				{
					headers: {
						Authorization: `Bearer ${token}`,
					},
				}
			);

			const content = normalizeGeneratedResume(response.data);
			if (!content) {
				throw new Error("No generated resume was returned by the server.");
			}

			setGeneratedResume(content);
		} catch (err) {
			const message =
				err.response?.data?.message ||
				err.response?.data?.error ||
				err.message ||
				"Failed to generate resume. Please try again.";
			setError(message);
			setGeneratedResume("");
		} finally {
			setIsSubmitting(false);
		}
	};

	const handleCopy = async () => {
		if (!generatedResume) {
			return;
		}

		try {
			await navigator.clipboard.writeText(generatedResume);
			setCopyStatus("Copied to clipboard.");
		} catch (err) {
			setCopyStatus("Copy failed. Please copy manually.");
		}
	};

	return (
		<main className="resume-generator-page">
			<section className="resume-generator-card">
				<h1>ATS Resume Generator</h1>
				<p className="resume-generator-subtitle">
					Paste your current resume and the job description to generate an ATS-
					optimized version.
				</p>

				<form className="resume-generator-form" onSubmit={handleSubmit}>
					<label htmlFor="resume-text">Resume Text</label>
					<textarea
						id="resume-text"
						value={resumeText}
						onChange={(event) => setResumeText(event.target.value)}
						placeholder="Paste your resume text here"
						rows={9}
						required
					/>

					<label htmlFor="job-description">Job Description</label>
					<textarea
						id="job-description"
						value={jobDescription}
						onChange={(event) => setJobDescription(event.target.value)}
						placeholder="Paste the target job description here"
						rows={9}
						required
					/>

					{error ? (
						<p className="resume-generator-error" role="alert">
							{error}
						</p>
					) : null}

					<button type="submit" disabled={!canSubmit}>
						{isSubmitting ? "Generating..." : "Generate ATS Resume"}
					</button>
				</form>

				<section className="resume-result-section" aria-label="Generated ATS resume">
					<div className="resume-result-header">
						<h2>Generated ATS Resume</h2>
						<button
							type="button"
							onClick={handleCopy}
							disabled={!generatedResume}
							className="copy-button"
						>
							Copy to Clipboard
						</button>
					</div>

					<pre className="resume-result-box">{generatedResume || "Your generated resume will appear here."}</pre>
					{copyStatus ? <p className="copy-status">{copyStatus}</p> : null}
				</section>
			</section>
		</main>
	);
}
