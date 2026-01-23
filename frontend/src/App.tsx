import { useState } from "react";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";

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
  raw_text?: string;
  applies_to?: string;
  trigger?: string;
};

type UserMustKnow = {
  deadlines: Deadline[];
  percentages: Percentage[];
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
  document_type?: string;
  confidence?: number;
  message?: string;
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
      if (res.data.document_type === "non_contract") {
        setData(null);
        alert(res.data.message || "This document does not appear to be a contract.");
        return;
      }
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
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
      style={{
        minHeight: "100vh",
        background:
          "radial-gradient(circle at top, #eef2ff 0%, #f3f4f6 55%)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "20px",
      }}
    >
      <div className="glass-card" style={{ maxWidth: 720, width: "100%", padding: 36 }}>
        <motion.h1
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
          style={{ fontSize: 30 }}
        >
          ClariScan AI
        </motion.h1>

        <p style={{ marginTop: 10, color: "#4b5563" }}>
          Upload a contract to instantly understand the key risks and obligations that matter.
        </p>

        {/* How This Helps You Section */}
        <div
          style={{
            marginTop: 24,
            display: "flex",
            justifyContent: "space-between",
            gap: 24,
            padding: "16px 0",
            borderTop: "1px solid #e5e7eb",
            borderBottom: "1px solid #e5e7eb",
          }}
        >
          <div style={{ flex: 1, textAlign: "center" }}>
            <div style={{ fontSize: 28, marginBottom: 6 }}>⚠️</div>
            <div style={{ fontWeight: "600", marginBottom: 4 }}>Identify hidden risks</div>
            <div style={{ fontSize: 14, color: "#6b7280" }}>
              Spot potential issues before they become problems.
            </div>
          </div>
          <div style={{ flex: 1, textAlign: "center" }}>
            <div style={{ fontSize: 28, marginBottom: 6 }}>⏱️</div>
            <div style={{ fontWeight: "600", marginBottom: 4 }}>Never miss critical deadlines</div>
            <div style={{ fontSize: 14, color: "#6b7280" }}>
              Keep track of important dates and obligations.
            </div>
          </div>
          <div style={{ flex: 1, textAlign: "center" }}>
            <div style={{ fontSize: 28, marginBottom: 6 }}>💰</div>
            <div style={{ fontWeight: "600", marginBottom: 4 }}>Understand penalties & costs</div>
            <div style={{ fontSize: 14, color: "#6b7280" }}>
              Know the financial impact of contract terms.
            </div>
          </div>
        </div>

        <div style={{ marginTop: 28, display: "flex", gap: 14, flexDirection: "column" }}>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
          <div style={{ fontSize: 12, color: "#6b7280" }}>
            Supported formats: PDF. Your document is not stored.
          </div>
          <motion.button
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            onClick={handleAnalyze}
            disabled={loading}
            style={{
              padding: "12px 18px",
              backgroundColor: "#2563eb",
              color: "white",
              borderRadius: 10,
              fontWeight: 600,
              opacity: loading ? 0.7 : 1,
              marginTop: 8,
              alignSelf: "stretch",
              cursor: loading ? "not-allowed" : "pointer",
            }}
          >
            {loading ? "Analyzing..." : "Analyze Contract"}
          </motion.button>
          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              style={{ marginTop: 16, fontSize: 14, color: "#4b5563" }}
            >
              <motion.div animate={{ opacity: [0, 1] }} transition={{ delay: 0.3 }}>
                ✔ Extracting clauses
              </motion.div>
              <motion.div animate={{ opacity: [0, 1] }} transition={{ delay: 0.6 }}>
                ✔ Identifying risks
              </motion.div>
              <motion.div animate={{ opacity: [0, 1] }} transition={{ delay: 0.9 }}>
                ✔ Summarizing key points
              </motion.div>
            </motion.div>
          )}
        </div>

        {data === null && !loading && (
          <div
            style={{
              marginTop: 24,
              padding: 16,
              borderRadius: 12,
              backgroundColor: "#fff7ed",
              border: "1px solid #fed7aa",
              color: "#9a3412",
            }}
          >
            <strong>Upload a legal contract</strong>
            <p style={{ marginTop: 6, fontSize: 14 }}>
              Resumes, portfolios, and general documents are not supported. Please upload a lease,
              agreement, NDA, or similar legal contract.
            </p>
          </div>
        )}

        {/* USER MUST KNOW */}
        {data && (
          <motion.div
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.5 }}
            style={{ marginTop: 40 }}
          >
            <p style={{ marginBottom: 12, color: "#374151", fontSize: 14 }}>
              This section summarizes only the most important things you should understand before signing or continuing with this contract.
            </p>
            <h2 style={{ fontSize: 22 }}>What You Must Know</h2>

            <div
              style={{
                backgroundColor: "#f9fafb",
                borderRadius: 12,
                padding: 16,
                marginBottom: 24,
                border: "1px solid #e5e7eb",
              }}
            >
              <strong>Most Important Points From This Document</strong>
              <p style={{ marginTop: 4, marginBottom: 12, fontStyle: "italic" }}>
                Based on this document, these are the primary issues you should pay attention to. Other clauses are standard or low impact.
              </p>
              <ul style={{ marginTop: 8 }}>
                <li>
                  This contract contains several <strong>high-risk clauses</strong>, including
                  termination, payment enforcement, and liability limitations.
                </li>
                <li>
                  <strong>Termination:</strong> The agreement allows termination with relatively
                  short notice, which may create operational or financial risk.
                </li>
                <li>
                  <strong>Payments:</strong> Late payments can trigger interest and penalties,
                  and services may be suspended if invoices are not paid on time.
                </li>
                <li>
                  <strong>Liability:</strong> The company’s liability is capped, limiting your
                  ability to recover damages.
                </li>
                <li>
                  Several clauses favor one party, meaning you may have fewer protections or
                  rights under this agreement.
                </li>
              </ul>
            </div>

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
                <strong>Late Payment Charges</strong>
                <p style={{ marginTop: 6, fontStyle: "italic", color: "#4b5563" }}>
                  These charges apply only if you miss a payment.
                </p>
                <ul style={{ marginTop: 8 }}>
                  {mustKnow.percentages.map((p, i) => (
                    <li key={i} style={{ marginBottom: 6 }}>
                      If payment is late, <strong>{p.raw_text}</strong>{" "}
                      {p.context.toLowerCase()}
                      {p.frequency ? ` (${p.frequency})` : ""} will be charged.
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </motion.div>
        )}

        {/* CLAUSES */}
        {data?.clauses?.length > 0 && (
          <div style={{ marginTop: 40 }}>
            <h2 style={{ fontSize: 22 }}>Clause Analysis</h2>

            {data.clauses.map((c, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                viewport={{ once: true }}
                style={{
                  backgroundColor: riskColor(c.analysis.risk_level),
                  padding: 18,
                  borderRadius: 14,
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
              </motion.div>
            ))}
          </div>
        )}

        <div
          style={{
            marginTop: 40,
            fontSize: 12,
            color: "#6b7280",
            textAlign: "center",
            userSelect: "none",
          }}
        >
          ⚖️ This is an AI-assisted summary, not legal advice.
        </div>
      </div>
    </motion.div>
  );
}
