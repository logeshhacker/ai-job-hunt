import { useEffect, useMemo, useState } from "react";
import api from "../services/api";
import "./JobTracker.css";

export default function JobTracker() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [addError, setAddError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [formData, setFormData] = useState({
    title: "",
    company: "",
    link: "",
    location: "",
    description: "",
  });

  const canSubmit = useMemo(
    () =>
      formData.title.trim() &&
      formData.company.trim() &&
      formData.location.trim() &&
      !isSubmitting,
    [formData, isSubmitting]
  );

  useEffect(() => {
    let isMounted = true;

    async function fetchJobs() {
      setLoading(true);
      setError("");

      try {
        const response = await api.get("/api/jobs/list");
        if (!isMounted) {
          return;
        }

        const jobList = Array.isArray(response.data) ? response.data : response.data.jobs || [];
        setJobs(jobList);
      } catch (err) {
        if (!isMounted) {
          return;
        }

        const message =
          err.response?.data?.message ||
          err.response?.data?.error ||
          "Unable to load jobs right now.";
        setError(message);
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }

    fetchJobs();

    return () => {
      isMounted = false;
    };
  }, []);

  const handleFormChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleAddJob = async (event) => {
    event.preventDefault();
    setAddError("");
    setIsSubmitting(true);

    try {
      const response = await api.post("/api/jobs/add", formData);

      if (response.data) {
        setJobs((prev) => [...prev, response.data]);
      }

      setFormData({
        title: "",
        company: "",
        link: "",
        location: "",
        description: "",
      });
    } catch (err) {
      const message =
        err.response?.data?.message ||
        err.response?.data?.error ||
        "Failed to add job. Please try again.";
      setAddError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleMarkApplied = async (jobId) => {
    try {
      await api.post(`/api/jobs/${jobId}/apply`);

      setJobs((prev) =>
        prev.map((job) =>
          job.id === jobId ? { ...job, applied: true } : job
        )
      );
    } catch (err) {
      console.error("Failed to mark job as applied:", err);
    }
  };

  return (
    <main className="job-tracker-page">
      <div className="job-tracker-container">
        <header className="job-tracker-header">
          <h1>Job Tracker</h1>
          <p>Track and manage your job applications</p>
        </header>

        <div className="job-tracker-sections">
          <section className="job-add-form-card">
            <h2>Add New Job</h2>
            <form className="job-add-form" onSubmit={handleAddJob}>
              <div>
                <label htmlFor="title">Job Title</label>
                <input
                  id="title"
                  name="title"
                  type="text"
                  value={formData.title}
                  onChange={handleFormChange}
                  placeholder="e.g., Senior Software Engineer"
                  required
                />
              </div>

              <div>
                <label htmlFor="company">Company</label>
                <input
                  id="company"
                  name="company"
                  type="text"
                  value={formData.company}
                  onChange={handleFormChange}
                  placeholder="e.g., Acme Corp"
                  required
                />
              </div>

              <div>
                <label htmlFor="link">Job Link</label>
                <input
                  id="link"
                  name="link"
                  type="url"
                  value={formData.link}
                  onChange={handleFormChange}
                  placeholder="https://example.com/job"
                />
              </div>

              <div>
                <label htmlFor="location">Location</label>
                <input
                  id="location"
                  name="location"
                  type="text"
                  value={formData.location}
                  onChange={handleFormChange}
                  placeholder="e.g., San Francisco, CA"
                  required
                />
              </div>

              <div className="job-add-form-full">
                <label htmlFor="description">Description</label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleFormChange}
                  placeholder="Job description and requirements"
                  rows={5}
                />
              </div>

              {addError ? (
                <p className="job-add-error" role="alert">
                  {addError}
                </p>
              ) : null}

              <button type="submit" disabled={!canSubmit}>
                {isSubmitting ? "Adding..." : "Add Job"}
              </button>
            </form>
          </section>

          <section className="job-list-card">
            <h2>All Jobs</h2>

            {loading ? (
              <p style={{ color: "#475569" }}>Loading jobs...</p>
            ) : error ? (
              <p style={{ color: "#b91c1c" }} role="alert">
                {error}
              </p>
            ) : jobs.length === 0 ? (
              <p className="job-list-empty">No jobs added yet. Add one to get started.</p>
            ) : (
              <div style={{ display: "grid", gap: "8px" }}>
                {jobs.map((job) => (
                  <article key={job.id} className="job-item">
                    <div className="job-item-header">
                      <h3 className="job-item-title">{job.title}</h3>
                      <div style={{ display: "flex", gap: "8px" }}>
                        <span className="job-item-company">{job.company}</span>
                        <span
                          className={`job-item-status ${
                            job.applied ? "applied" : "not-applied"
                          }`}
                        >
                          {job.applied ? "Applied" : "Not Applied"}
                        </span>
                      </div>
                    </div>

                    <div className="job-item-details">
                      <div className="job-item-detail">
                        <span className="job-detail-label">Location:</span>{" "}
                        {job.location}
                      </div>
                      {job.link ? (
                        <div className="job-item-detail">
                          <span className="job-detail-label">Link:</span>{" "}
                          <a href={job.link} target="_blank" rel="noopener noreferrer">
                            {job.link}
                          </a>
                        </div>
                      ) : null}
                    </div>

                    {job.description ? (
                      <div className="job-item-description">{job.description}</div>
                    ) : null}

                    <div className="job-item-actions">
                      {!job.applied ? (
                        <button
                          className="job-apply-button"
                          onClick={() => handleMarkApplied(job.id)}
                        >
                          Mark as Applied
                        </button>
                      ) : (
                        <span style={{ fontSize: "0.85rem", color: "#166534" }}>
                          ✓ Applied
                        </span>
                      )}
                    </div>
                  </article>
                ))}
              </div>
            )}
          </section>
        </div>
      </div>
    </main>
  );
}
