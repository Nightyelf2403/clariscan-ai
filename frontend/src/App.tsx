import { useState } from "react";
import axios from "axios";

type AnalysisResult = {
  clause_text: string;
  analysis: {
    clause_type: string;
    risk_level: "Low" | "Medium" | "High";
    explanation: string;
    suggestion: string | null;
  };
};

const API_URL = "https://clariscan-ai.onrender.com/analyze";

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [results, setResults] = useState<AnalysisResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please select a PDF file.");
      return;
    }

    setError(null);
    setResults([]);
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(API_URL, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setResults(response.data.results || []);
    } catch (err) {
      console.error(err);
      setError("Failed to analyze contract. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const riskColor = (risk: string) => {
    if (risk === "High") return "#fee2e2";
    if (risk === "Medium") return "#fef3c7";
    return "#dcfce7";
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#f3f4f6",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "24px",
        fontFamily: "Inter, system-ui, sans-serif",
      }}
    >
      <div
        style={{
          backgroundColor: "#ffffff",
          borderRadius: "12px",
          padding: "32px",
          width: "100%",
          maxWidth: "900px",
          boxShadow: "0 10px 25px rgba(0,0,0,0.1)",
        }}
      >
        <h1 style={{ fontSize: "28px", fontWeight: 700 }}>
          ClariScan AI
        </h1>

        <p style={{ color: "#555", marginTop: "8px" }}>
          Upload a contract PDF to identify potential legal risks.
        </p>

        {/* Upload section */}
        <div
          style={{
            marginTop: "24px",
            display: "flex",
            gap: "12px",
            alignItems: "center",
          }}
        >
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />

          <button
            onClick={handleAnalyze}
            disabled={loading}
            style={{
              padding: "8px 16px",
              backgroundColor: "#2563eb",
              color: "white",
              border: "none",
              borderRadius: "6px",
              cursor: "pointer",
              opacity: loading ? 0.6 : 1,
            }}
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>

        {/* Error */}
        {error && (
          <p style={{ color: "red", marginTop: "12px" }}>
            {error}
          </p>
        )}

        {/* Results */}
        {results.length > 0 && (
          <div style={{ marginTop: "40px" }}>
            <h2 style={{ fontSize: "20px", marginBottom: "16px" }}>
              Analysis Results
            </h2>

            {results.map((item, index) => (
              <div
                key={index}
                style={{
                  backgroundColor: riskColor(item.analysis.risk_level),
                  padding: "16px",
                  borderRadius: "8px",
                  marginBottom: "16px",
                }}
              >
                <strong>
                  {item.analysis.clause_type} —{" "}
                  {item.analysis.risk_level} Risk
                </strong>

                <p style={{ marginTop: "8px" }}>
                  {item.clause_text}
                </p>

                <p style={{ marginTop: "8px" }}>
                  <strong>Explanation:</strong>{" "}
                  {item.analysis.explanation}
                </p>

                {item.analysis.suggestion && (
                  <p style={{ marginTop: "6px" }}>
                    <strong>Suggestion:</strong>{" "}
                    {item.analysis.suggestion}
                  </p>
                )}
              </div>
            ))}

            <p style={{ fontSize: "12px", color: "#666" }}>
              ⚠️ This tool is for informational purposes only and does not
              constitute legal advice.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
