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

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [results, setResults] = useState<AnalysisResult[]>([]);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!file) {
      alert("Please upload a PDF contract.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setResults([]);

    try {
      const res = await axios.post(
        "https://clariscan-ai.onrender.com/analyze",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      setResults(res.data.results);
    } catch (error) {
      console.error(error);
      alert("Failed to analyze contract");
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
        background:
          "radial-gradient(circle at top, #eef2ff 0%, #f3f4f6 55%)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "32px",
      }}
    >
      <div className="glow-border">
        <div
          className="glass-card"
          style={{
            padding: "36px",
            width: "100%",
            maxWidth: "900px",
          }}
        >
          {/* Header */}
          <h1 style={{ fontSize: "30px" }}>ClariScan AI</h1>

          <p style={{ marginTop: "10px", color: "#4b5563" }}>
            ClariScan AI helps you understand legal contracts before you sign
            them. Upload a PDF contract to break it into clauses, identify
            potential risks, and receive clear explanations in plain English.
          </p>

          <p className="disclaimer">
            This tool provides informational insights only and does not replace
            professional legal advice.
          </p>

          {/* Upload */}
          <div
            style={{
              marginTop: "28px",
              display: "flex",
              gap: "14px",
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
              className="analyze-btn"
              style={{
                padding: "10px 18px",
                backgroundColor: "#2563eb",
                color: "white",
                border: "none",
                borderRadius: "8px",
                cursor: "pointer",
                fontWeight: 600,
                opacity: loading ? 0.7 : 1,
              }}
            >
              {loading ? "Analyzing..." : "Analyze"}
            </button>
          </div>

          {/* Results */}
          {results.length > 0 && (
            <div style={{ marginTop: "44px" }}>
              <h2 style={{ fontSize: "22px", marginBottom: "20px" }}>
                Analysis Results
              </h2>

              {results.map((item, index) => (
                <div
                  key={index}
                  className="result-card"
                  style={{
                    backgroundColor: riskColor(item.analysis.risk_level),
                    padding: "18px",
                    borderRadius: "12px",
                    marginBottom: "18px",
                  }}
                >
                  <strong>
                    {item.analysis.clause_type} —{" "}
                    {item.analysis.risk_level} Risk
                  </strong>

                  <p style={{ marginTop: "10px" }}>
                    {item.clause_text}
                  </p>

                  <p style={{ marginTop: "10px" }}>
                    <strong>Explanation:</strong>{" "}
                    {item.analysis.explanation}
                  </p>

                  {item.analysis.suggestion && (
                    <p style={{ marginTop: "8px" }}>
                      <strong>Suggestion:</strong>{" "}
                      {item.analysis.suggestion}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
