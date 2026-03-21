import { useEffect, useMemo, useState } from "react";
import { Bar } from "react-chartjs-2";
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Title,
  Tooltip,
} from "chart.js";
import api from "../services/api";
import "./Analytics.css";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function toNumber(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

export default function Analytics() {
  const [summary, setSummary] = useState({
    total_jobs: 0,
    applied: 0,
    interviews: 0,
    offers: 0,
  });

  const [dailyData, setDailyData] = useState([]);
  const [loadingStats, setLoadingStats] = useState(true);
  const [loadingChart, setLoadingChart] = useState(true);
  const [statsError, setStatsError] = useState("");
  const [chartError, setChartError] = useState("");
  const [isExporting, setIsExporting] = useState(false);
  const [exportError, setExportError] = useState("");

  useEffect(() => {
    let isMounted = true;

    async function fetchSummary() {
      setLoadingStats(true);
      setStatsError("");

      try {
        const response = await api.get("/api/analytics/summary");
        if (!isMounted) {
          return;
        }

        const data = response.data || {};
        setSummary({
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
          "Unable to load summary stats.";
        setStatsError(message);
      } finally {
        if (isMounted) {
          setLoadingStats(false);
        }
      }
    }

    fetchSummary();
    return () => {
      isMounted = false;
    };
  }, []);

  useEffect(() => {
    let isMounted = true;

    async function fetchDaily() {
      setLoadingChart(true);
      setChartError("");

      try {
        const response = await api.get("/api/analytics/daily");
        if (!isMounted) {
          return;
        }

        const data = Array.isArray(response.data) ? response.data : response.data.data || [];
        setDailyData(data);
      } catch (err) {
        if (!isMounted) {
          return;
        }

        const message =
          err.response?.data?.message ||
          err.response?.data?.error ||
          "Unable to load daily data.";
        setChartError(message);
      } finally {
        if (isMounted) {
          setLoadingChart(false);
        }
      }
    }

    fetchDaily();
    return () => {
      isMounted = false;
    };
  }, []);

  const chartData = useMemo(() => {
    if (!dailyData || dailyData.length === 0) {
      return {
        labels: [],
        datasets: [
          {
            label: "Daily Applications",
            data: [],
            backgroundColor: "#0284c7",
            borderColor: "#0369a1",
            borderWidth: 1,
          },
        ],
      };
    }

    const labels = dailyData.map((item) => item.date || item.day || "");
    const counts = dailyData.map((item) => toNumber(item.count ?? item.applications));

    return {
      labels,
      datasets: [
        {
          label: "Daily Applications",
          data: counts,
          backgroundColor: "#0284c7",
          borderColor: "#0369a1",
          borderWidth: 1,
          borderRadius: 4,
        },
      ],
    };
  }, [dailyData]);

  const chartOptions = useMemo(
    () => ({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        title: {
          display: false,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1,
          },
        },
      },
    }),
    []
  );

  const handleExportExcel = async () => {
    setExportError("");
    setIsExporting(true);

    try {
      const response = await api.get("/api/analytics/export-excel", {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "analytics.xlsx");
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      const message =
        err.response?.data?.message ||
        err.response?.data?.error ||
        "Failed to export data. Please try again.";
      setExportError(message);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <main className="analytics-page">
      <div className="analytics-container">
        <header className="analytics-header">
          <h1>Analytics</h1>
          <p>View your job search analytics and trends</p>
        </header>

        <div className="analytics-export-section">
          <button
            className="export-button"
            onClick={handleExportExcel}
            disabled={isExporting}
          >
            {isExporting ? "Exporting..." : "Export to Excel"}
          </button>
        </div>

        {exportError ? (
          <p
            style={{
              color: "#b91c1c",
              marginBottom: "16px",
              fontWeight: "500",
            }}
            role="alert"
          >
            {exportError}
          </p>
        ) : null}

        <div className="analytics-content">
          {loadingStats ? (
            <p className="analytics-loading">Loading summary stats...</p>
          ) : statsError ? (
            <p className="analytics-error" role="alert">
              {statsError}
            </p>
          ) : (
            <div className="analytics-stats">
              <article className="analytics-stat-card">
                <p className="analytics-stat-label">Total Jobs</p>
                <p className="analytics-stat-value">{summary.total_jobs}</p>
              </article>

              <article className="analytics-stat-card">
                <p className="analytics-stat-label">Applied</p>
                <p className="analytics-stat-value">{summary.applied}</p>
              </article>

              <article className="analytics-stat-card">
                <p className="analytics-stat-label">Interviews</p>
                <p className="analytics-stat-value">{summary.interviews}</p>
              </article>

              <article className="analytics-stat-card">
                <p className="analytics-stat-label">Offers</p>
                <p className="analytics-stat-value">{summary.offers}</p>
              </article>
            </div>
          )}

          <article className="analytics-chart-card">
            <h2>Daily Applications (Last 30 Days)</h2>

            {loadingChart ? (
              <p className="analytics-loading">Loading chart data...</p>
            ) : chartError ? (
              <p className="analytics-error" role="alert">
                {chartError}
              </p>
            ) : (
              <div className="chart-container">
                <Bar data={chartData} options={chartOptions} />
              </div>
            )}
          </article>
        </div>
      </div>
    </main>
  );
}
