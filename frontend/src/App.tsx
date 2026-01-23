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

  const consequenceMap: Record<string, string> = {
    penalty: "Financial penalty may be charged",
    termination: "The agreement may be terminated",
    service_suspension: "Your service may be suspended",
  };

  const mustKnow = data?.document_summary?.user_must_know ?? {
    deadlines: [],
    percentages: [],
    consequences: [],
    what_happens_if_you_dont_comply: [],
  };

  // Build consequence chain array
  const consequenceChainParts: string[] = [];

  // Deadlines part
  if (mustKnow.deadlines?.length) {
    mustKnow.deadlines.forEach((d) => {
      consequenceChainParts.push(`Miss ${d.raw_text}`);
    });
  }

  // Percentages part
  if (mustKnow.percentages?.length) {
    mustKnow.percentages.forEach((p) => {
      const contextLower = p.context.toLowerCase();
      // Use raw_text + context + "will be applied if you do not meet the obligation"
      consequenceChainParts.push(`${p.raw_text} ${contextLower} will be applied if you do not meet the obligation`);
    });
  }

  // Consequences part (map keys to human-readable)
  if (mustKnow.consequences?.length) {
    mustKnow.consequences.forEach((c) => {
      const mapped = consequenceMap[c] ?? c;
      consequenceChainParts.push(mapped);
    });
  }

  // what_happens_if_you_dont_comply part
  if (mustKnow.what_happens_if_you_dont_comply?.length) {
    mustKnow.what_happens_if_you_dont_comply.forEach((w) => {
      consequenceChainParts.push(w);
    });
  }

  // Join with arrows, but skip empty parts
  const consequenceChain = consequenceChainParts.filter(Boolean).join(" → ");

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
            {consequenceChain && (
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
                  What Happens If You Don’t Comply (Consequence Chain)
                </strong>
                <p style={{ margin: 0 }}>{consequenceChain}</p>
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
                      You must act within {d.raw_text} ({d.unit})
                      <div style={{ fontSize: 12, color: "#6b7280", marginTop: 2 }}>
                        Missing this deadline may trigger penalties or termination.
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
                      {p.raw_text} {p.context.toLowerCase()} will be applied if you fail to meet the related obligation (e.g. late payment)
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Consequences */}
            {mustKnow.consequences?.length > 0 && (
              <div
                style={{
                  backgroundColor: "#f9fafb",
                  borderRadius: 12,
                  padding: 16,
                  marginBottom: 24,
                  border: "1px solid #e5e7eb",
                }}
              >
                <strong>Consequences</strong>
                <ul style={{ marginTop: 8 }}>
                  {mustKnow.consequences.map((c, i) => (
                    <li key={i} style={{ marginBottom: 6 }}>
                      {consequenceMap[c] ?? c}
                    </li>
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
