import { useState } from "react";
import axios from "axios";

type Percentage = {
  value: number;
  raw_text: string;
  context: string;
};

type Deadline = {
  value: number;
  unit: string;
  raw_text: string;
};

type UserMustKnow = {
  deadlines: Deadline[];
  percentages: Percentage[];
  consequences: string[];
  what_happens_if_you_dont_comply?: string[];
};

type ClauseAnalysis = {
  clause_type: string;
  risk_level: "Low" | "Medium" | "High";
  explanation: string;
  suggestion?: string;
  user_must_know?: UserMustKnow;
};

type Clause = {
  clause_text: string;
  analysis: ClauseAnalysis;
};

type ApiResponse = {
  document_summary: {
    user_must_know: UserMustKnow;
  };
  clauses: Clause[];
};

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!file) {
      alert("Please upload a contract file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setData(null);

    try {
      const res = await axios.post(
        "https://clariscan-ai.onrender.com/analyze",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      setData(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to analyze document");
    } finally {
      setLoading(false);
    }
  };

  const riskColor = (risk: string) => {
    if (risk === "High") return "#fee2e2";
    if (risk === "Medium") return "#fef3c7";
    return "#dcfce7";
  };

  const mustKnow = data?.document_summary?.user_must_know ?? {
    deadlines: [],
    percentages: [],
    consequences: [],
    what_happens_if_you_dont_comply: [],
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
      <div className="glass-card" style={{ maxWidth: 1000, width: "100%", padding: 36 }}>
        <h1 style={{ fontSize: 30 }}>ClariScan AI</h1>

        <p style={{ marginTop: 10, color: "#4b5563" }}>
          Upload a contract to instantly understand risks, deadlines, penalties,
          and consequences.
        </p>

        <div style={{ marginTop: 28, display: "flex", gap: 14 }}>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
          <button
            onClick={handleAnalyze}
            disabled={loading}
            style={{
              padding: "10px 18px",
              backgroundColor: "#2563eb",
              color: "white",
              borderRadius: 8,
              fontWeight: 600,
              opacity: loading ? 0.7 : 1,
            }}
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>

        {/* USER MUST KNOW */}
        {data && (
          <div style={{ marginTop: 40 }}>
            <h2 style={{ fontSize: 22 }}>What You Must Know</h2>

            {mustKnow.deadlines.length > 0 && (
              <div>
                <strong>Deadlines</strong>
                <ul>
                  {mustKnow.deadlines.map((d, i) => (
                    <li key={i}>{d.raw_text}</li>
                  ))}
                </ul>
              </div>
            )}

            {mustKnow.percentages.length > 0 && (
              <div>
                <strong>Percentages</strong>
                <ul>
                  {mustKnow.percentages.map((p, i) => (
                    <li key={i}>
                      {p.raw_text} ({p.context})
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {mustKnow.consequences.length > 0 && (
              <div>
                <strong>Consequences</strong>
                <ul>
                  {mustKnow.consequences.map((c, i) => (
                    <li key={i}>{c}</li>
                  ))}
                </ul>
              </div>
            )}

            {mustKnow.what_happens_if_you_dont_comply &&
              mustKnow.what_happens_if_you_dont_comply.length > 0 && (
                <div>
                  <strong>If You Don’t Comply</strong>
                  <ul>
                    {mustKnow.what_happens_if_you_dont_comply.map((w, i) => (
                      <li key={i}>{w}</li>
                    ))}
                  </ul>
                </div>
              )}
          </div>
        )}

        {/* CLAUSES */}
        {data?.clauses && data.clauses.length > 0 && (
          <div style={{ marginTop: 40 }}>
            <h2 style={{ fontSize: 22 }}>Clause Analysis</h2>

            {data.clauses.map((c, i) => (
              <div
                key={i}
                style={{
                  backgroundColor: riskColor(c.analysis.risk_level),
                  padding: 18,
                  borderRadius: 12,
                  marginTop: 18,
                }}
              >
                <strong>
                  {c.analysis.clause_type} — {c.analysis.risk_level}
                </strong>

                <p style={{ marginTop: 8 }}>{c.clause_text}</p>

                <p style={{ marginTop: 8 }}>
                  <strong>Explanation:</strong> {c.analysis.explanation}
                </p>

                {c.analysis.suggestion && (
                  <p style={{ marginTop: 6 }}>
                    <strong>Suggestion:</strong> {c.analysis.suggestion}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
