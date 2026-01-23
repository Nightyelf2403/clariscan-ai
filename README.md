# ClariScan AI ⚖️

ClariScan AI is a lightweight web application that helps users **understand legal contracts faster** by extracting **key risks, obligations, penalties, and important clauses** from uploaded documents.

The goal is simple:  
👉 **Show users what actually matters before they sign a contract.**

This project focuses on **clarity, explainability, and usability**, not legal jargon.

---

## 🚀 Live Demo
Frontend:  
https://nightyelf2403.github.io/clariscan-ai

Backend API:  
https://clariscan-ai.onrender.com

---

## 🧠 Why This Project Exists

Most people sign contracts without fully understanding:
- Hidden risks
- Termination clauses
- Late payment penalties
- Liability limits
- One-sided obligations

ClariScan AI **summarizes only the most important points**, so users can quickly decide:
- Is this contract risky?
- What should I be careful about?
- What happens if I miss a payment or deadline?

---

## ❗ Important Note About AI Usage

### ❌ No paid AI / LLMs were used
This project **does NOT use OpenAI, GPT, Claude, Gemini, or any paid AI services**.

**Reason:**  
Paid AI APIs are expensive and not feasible for this project’s budget.

---

## ✅ How “AI-like” Analysis Is Achieved Without Paid AI

Instead of using large language models, ClariScan AI uses:

- **Rule-based legal pattern detection**
- **Keyword + phrase matching**
- **Structured clause classification**
- **Heuristic scoring**
- **Deterministic logic**

This makes the system:
- Predictable
- Explainable
- Cost-free
- Fast

While it is not generative AI, the output is **very similar to AI summaries**, because contracts follow repeatable legal patterns.

---

## 🛠️ Tech Stack

### Frontend
- **React (TypeScript)**
- **Vite**
- **Framer Motion** (animations & micro-interactions)
- **CSS / Tailwind-style utilities**
- **Axios** (API calls)
- **GitHub Pages** (deployment)

### Backend
- **FastAPI**
- **Python**
- **PyPDF** (PDF text extraction)
- **Rule Engine** (custom legal analysis logic)
- **Uvicorn**
- **Render** (backend hosting)

---

## 📄 What the App Can Do

### ✔ Detect if a document is a contract
- Rejects resumes, general documents, etc.

### ✔ Extract key clauses
- Termination
- Payments
- Liability
- Intellectual Property
- Service suspension
- Refunds
- Compliance obligations

### ✔ Risk classification
- High / Medium / Low risk tagging
- Clear explanations (plain English)

### ✔ “What You Must Know” Summary
Only shows:
- Critical risks
- Important penalties
- Major obligations
- Financial consequences

No unnecessary legal noise.

---

## 🧩 Example Output
- “Late payments incur 2.5% monthly interest.”
- “Services may be suspended if payment is overdue.”
- “Liability is capped to fees paid in the last 6 months.”
- “Termination can occur with short notice.”

---

## 🎨 UX & Design Principles
- Mobile-friendly
- Minimal UI
- Clear hierarchy
- Smooth animations
- Focus on **understanding**, not legal overwhelm

---

## ⚠️ Disclaimer
ClariScan AI provides **AI-assisted summaries only**.  
It does **NOT** provide legal advice.

Always consult a qualified legal professional before making legal decisions.

---

## 📌 Future Improvements
- Optional LLM integration (when budget allows)
- Clause comparison
- Exportable summaries
- Contract risk scoring trends
- Multi-language support

---

## 👤 Author
**Nightyelf2403**

GitHub: https://github.com/Nightyelf2403

---

⭐ If you find this project useful, feel free to star the repo!
