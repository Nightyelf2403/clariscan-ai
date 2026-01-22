from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import SessionLocal
from . import models, crud
from .pdf_utils import extract_text_from_pdf
from .clause_utils import split_into_clauses
from .analyzer import analyze_clause, analyze_document

# -------------------------
# App initialization
# -------------------------

app = FastAPI(
    title="ClariScan AI",
    description="Deterministic contract risk analysis engine",
    version="1.0.0"
)

# -------------------------
# CORS configuration
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://nightyelf2403.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Database dependency
# -------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# Health check
# -------------------------

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "ClariScan AI",
        "engine": "deterministic-rule-engine"
    }

# -------------------------
# Analyze contract endpoint
# -------------------------

@app.post("/analyze")
def analyze_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Extract full text from PDF
    document_text = extract_text_from_pdf(file.file)

    # 2. Run document-level intelligence engine
    document_summary = analyze_document(document_text)

    # 3. Split into clauses (for UI drill-down)
    clauses = split_into_clauses(document_text)

    # 4. Persist document metadata (safe even without DB migrations)
    document = crud.create_document(
        db=db,
        filename=file.filename
    )

    # 5. Clause-level results
    clause_results = [
        {
            "clause_text": clause,
            "analysis": analyze_clause(clause)
        }
        for clause in clauses
    ]

    # 6. Final response (frontend-first)
    return {
        "document_id": document.id,
        "filename": file.filename,
        "total_clauses": len(clause_results),
        "document_summary": document_summary,
        "clauses": clause_results
    }
