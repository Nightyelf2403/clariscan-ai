import { useState } from "react";
import axios from "axios";

type Percentage = {
  value: number;
  raw_text: string;
  context: string;
  frequency?: string;
  trigger?: string;
};

type Deadline = {
  value: number;
  unit: string;
  raw_text: string;
  applies_to?: string;
  trigger?: string;
};

type UserMustKnow = {
  deadlines: Deadline[];
  percentages: Percentage[];
  consequence_chain?: { if: string; then: string; obligation_type?: string }[];
};

type ClauseAnalysis = {
  clause_type: string;
  risk_level: "Low" | "Medium" | "High";
  explanation: string;
  suggestion?: string;
  user_must_know?: UserMustKnow;
  obligation?: string;
  obligation_explanation?: string;
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

            {/* Consequence Chain */}
            {mustKnow.consequence_chain?.length > 0 && (
              <div
                style={{
                  backgroundColor: "#f9fafb",
                  borderRadius: 12,
                  padding: 16,
                  marginBottom: 24,
                  border: "1px solid #e5e7eb",
                }}
              >
                <strong style={{ display: "block", marginBottom: 8 }}>
                  Consequences If Obligations Are Not Met
                </strong>
                <ul style={{ margin: 0, paddingLeft: 20 }}>
                  {mustKnow.consequence_chain.map((c, i) => (
                    <li key={i} style={{ marginBottom: 6 }}>
                      <strong>{c.if}</strong> → {c.then}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Deadlines */}
            {mustKnow.deadlines?.length > 0 && (
              <div
                style={{
                  backgroundColor: "#f9fafb",
                  borderRadius: 12,
                  padding: 16,
                  marginBottom: 24,
                  border: "1px solid #e5e7eb",
                }}
              >
                <strong>Deadlines</strong>
                <ul style={{ marginTop: 8 }}>
                  {mustKnow.deadlines.map((d, i) => (
                    <li key={i} style={{ marginBottom: 6 }}>
                      {d.applies_to
                        ? `You must comply with the ${d.applies_to} within ${d.raw_text}.`
                        : d.trigger
                        ? `You must act within ${d.raw_text} when ${d.trigger}.`
                        : `Important time period: ${d.raw_text} as defined in the contract.`}
                      <div style={{ fontSize: 12, color: "#6b7280", marginTop: 2 }}>
                        Missing this may result in penalties, suspension, or termination.
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Percentages */}
            {mustKnow.percentages?.length > 0 && (
              <div
                style={{
                  backgroundColor: "#f9fafb",
                  borderRadius: 12,
                  padding: 16,
                  marginBottom: 24,
                  border: "1px solid #e5e7eb",
                }}
              >
                <strong>Percentages</strong>
                <ul style={{ marginTop: 8 }}>
                  {mustKnow.percentages.map((p, i) => (
                    <li key={i} style={{ marginBottom: 6 }}>
                      <strong>{p.raw_text}</strong> {p.context.toLowerCase()}
                      {p.frequency ? ` (${p.frequency})` : ""} will apply because of {p.trigger || "a missed obligation"}.
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* CLAUSES */}
        {data?.clauses?.length > 0 && (
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

                {c.analysis.obligation_explanation && (
                  <p style={{ marginTop: 8 }}>
                    <strong>Obligation:</strong> {c.analysis.obligation_explanation}
                  </p>
                )}

                <p style={{ marginTop: 8 }}>
                  <strong>Explanation:</strong> {c.analysis.explanation}
                </p>

                {c.analysis.suggestion && (
                  <p style={{ marginTop: 6 }}>
                    <strong>Suggestion:</strong> {c.analysis.suggestion}
                  </p>
                )}

                {c.analysis.user_must_know?.consequence_chain?.length > 0 && (
                  <div style={{ marginTop: 10 }}>
                    <strong>If you don’t comply:</strong>
                    <ul style={{ marginTop: 6 }}>
                      {c.analysis.user_must_know.consequence_chain.map((cc, idx) => (
                        <li key={idx}>
                          {cc.then}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
