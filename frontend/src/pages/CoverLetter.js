import { useMemo, useState } from "react";
import api from "../services/api";
import "./CoverLetter.css";

function extractCoverLetter(data) {
  if (!data) {
    return "";
  }

  if (typeof data === "string") {
    return data;
  }

  return data.cover_letter || data.generated_cover_letter || data.result || "";
}

export default function CoverLetter() {
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [generatedCoverLetter, setGeneratedCoverLetter] = useState("");
  const [error, setError] = useState("");
  const [copyStatus, setCopyStatus] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const canSubmit = useMemo(
    () =>
      resumeText.trim() &&
      jobDescription.trim() &&
      companyName.trim() &&
      !isSubmitting,
    [resumeText, jobDescription, companyName, isSubmitting]
  );

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setCopyStatus("");
    setIsSubmitting(true);

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        throw new Error("You must be logged in to generate a cover letter.");
      }

      const response = await api.post(
        "/api/cover-letter/generate",
        {
          resume_text: resumeText,
          job_description: jobDescription,
          company_name: companyName,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const generated = extractCoverLetter(response.data);
      if (!generated) {
        throw new Error("No cover letter content was returned by the server.");
      }

      setGeneratedCoverLetter(generated);
    } catch (err) {
      const message =
        err.response?.data?.message ||
        err.response?.data?.error ||
        err.message ||
        "Failed to generate cover letter. Please try again.";
      setError(message);
      setGeneratedCoverLetter("");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCopy = async () => {
    if (!generatedCoverLetter) {
      return;
    }

    try {
      await navigator.clipboard.writeText(generatedCoverLetter);
      setCopyStatus("Copied to clipboard.");
    } catch (err) {
      setCopyStatus("Copy failed. Please copy manually.");
    }
  };

  return (
    <main className="cover-letter-page">
      <section className="cover-letter-card">
        <h1>Cover Letter Generator</h1>
        <p className="cover-letter-subtitle">
          Generate a tailored cover letter from your resume and target role details.
        </p>

        <form className="cover-letter-form" onSubmit={handleSubmit}>
          <label htmlFor="company-name">Company Name</label>
          <input
            id="company-name"
            type="text"
            value={companyName}
            onChange={(event) => setCompanyName(event.target.value)}
            placeholder="Enter company name"
            required
          />

          <label htmlFor="resume-text">Resume Text</label>
          <textarea
            id="resume-text"
            value={resumeText}
            onChange={(event) => setResumeText(event.target.value)}
            placeholder="Paste your resume text here"
            rows={8}
            required
          />

          <label htmlFor="job-description">Job Description</label>
          <textarea
            id="job-description"
            value={jobDescription}
            onChange={(event) => setJobDescription(event.target.value)}
            placeholder="Paste the job description here"
            rows={8}
            required
          />

          {error ? (
            <p className="cover-letter-error" role="alert">
              {error}
            </p>
          ) : null}

          <button type="submit" disabled={!canSubmit}>
            {isSubmitting ? "Generating..." : "Generate Cover Letter"}
          </button>
        </form>

        <section className="cover-letter-result" aria-label="Generated cover letter">
          <div className="cover-letter-result-header">
            <h2>Generated Cover Letter</h2>
            <button
              type="button"
              className="cover-letter-copy"
              onClick={handleCopy}
              disabled={!generatedCoverLetter}
            >
              Copy to Clipboard
            </button>
          </div>

          <pre className="cover-letter-result-box">
            {generatedCoverLetter || "Your generated cover letter will appear here."}
          </pre>
          {copyStatus ? (
            <p className="cover-letter-copy-status">{copyStatus}</p>
          ) : null}
        </section>
      </section>
    </main>
  );
}
