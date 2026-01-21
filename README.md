# ClariScan AI 🧠📄  
**AI-assisted Contract Risk Analyzer**

ClariScan AI is a full-stack web application that helps users understand legal contracts by breaking them into readable clauses and highlighting potential legal risks with clear explanations and suggestions.

This project demonstrates how AI-assisted document analysis can be built using a modern, production-style web stack.

---

## 🚨 Why ClariScan AI Exists (The Problem)

Legal contracts are everywhere — employment offers, rental agreements, service contracts, NDAs — yet most people sign them without fully understanding the risks.

Common problems include:
- Legal language is complex and intimidating
- Important clauses are buried deep in long documents
- One-sided termination rights go unnoticed
- Hidden liability limitations and penalties are missed
- Hiring a lawyer for every document is expensive and unrealistic

As a result, people often discover problems **after** they are legally bound.

---

## 💡 How ClariScan AI Helps

ClariScan AI acts as a **first-pass contract risk assistant**.

It:
- Extracts text from uploaded PDF contracts
- Splits documents into individual clauses
- Classifies each clause by type (e.g., Termination, Payment, Liability)
- Assigns a **risk level** (Low / Medium / High)
- Explains risks in **plain English**
- Suggests what users should review or question

⚠️ ClariScan AI does **not replace lawyers** — it helps users become informed **before signing**.

---

## 🎯 What This Project Demonstrates

This project is designed as a **real-world engineering demo**, not a toy example.

It demonstrates:
- Full-stack development (React + FastAPI)
- PDF text extraction and processing
- Clause segmentation and rule-based analysis
- Clean API design and data flow
- Frontend ↔ backend integration
- Deployment on GitHub Pages and Render
- Responsible AI design with clear disclaimers

---

## ✨ Key Features

- Upload PDF contracts
- Automatic clause extraction
- Clause classification
- Risk levels: Low / Medium / High
- Plain-English explanations
- Improvement suggestions
- Clean, user-friendly UI
- Fully deployed frontend and backend

---

## 🌐 Live Demo

- **Frontend (GitHub Pages)**  
  👉 https://nightyelf2403.github.io/clariscan-ai/

- **Backend API (Render)**  
  👉 https://clariscan-ai.onrender.com/

- **API Documentation (Swagger)**  
  👉 https://clariscan-ai.onrender.com/docs

---

## 🛠 Tech Stack

### Frontend
- React
- TypeScript
- Vite
- Axios
- Tailwind CSS
- GitHub Pages (deployment)

### Backend
- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL (configurable)
- PyPDF (PDF text extraction)
- Render (deployment)

---

## 🧠 Analysis Logic

Currently, ClariScan AI uses a **rule-based analysis engine** to:
- Identify clause types
- Assign risk levels
- Generate explanations and suggestions

The architecture is intentionally designed so it can be **upgraded to LLM-based analysis** (OpenAI / Claude / Gemini) in the future without major refactoring.

---

## 🗂 Project Structure

```
clariscan-ai/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── analyzer.py
│   │   ├── clause_utils.py
│   │   ├── pdf_utils.py
│   │   ├── database.py
│   │   └── models.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── index.html
│   └── vite.config.ts
│
├── render.yaml
└── README.md

```
⸻

▶️ Running Locally

Backend

cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Backend runs at:
👉 http://127.0.0.1:8000
👉 http://127.0.0.1:8000/docs

Frontend

cd frontend
npm install
npm run dev

Frontend runs at:
👉 http://localhost:5173

⸻

⚠️ Important Disclaimer

ClariScan AI provides informational insights only.
It does not provide legal advice and should not be used as a substitute for a qualified legal professional.
Currently focuses on high-confidence risk patterns. Some contextual or implicit risks (such as IP ownership balance or missing clauses) are intentionally conservative and flagged in future iterations.

⸻

🔮 Future Improvements
	•	Integrate LLMs for deeper legal reasoning
	•	Clause comparison across jurisdictions
	•	Highlight unusual or non-standard clauses
	•	Export annotated contracts
	•	User accounts and history
	•	Advanced visualizations and summaries

⸻

👤 Author

Lalith Aditya
	•	GitHub: https://github.com/nightyelf2403
	•	LinkedIn: https://www.linkedin.com/in/lalithaditya/

