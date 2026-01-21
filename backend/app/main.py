from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import engine, SessionLocal
from . import models, crud
from .pdf_utils import extract_text_from_pdf
from .clause_utils import split_into_clauses
from .analyzer import analyze_clause

# -------------------------
# App initialization
# -------------------------

app = FastAPI(title="ClariScan AI")

# -------------------------
# CORS configuration
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",                 # local frontend
        "https://nightyelf2403.github.io",        # GitHub Pages
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
# Startup event (SAFE for cloud)
# -------------------------

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)

# -------------------------
# Health check
# -------------------------

@app.get("/")
def health_check():
    return {"status": "ok"}

# -------------------------
# Analyze contract endpoint
# -------------------------

@app.post("/analyze")
def analyze_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Extract text from PDF
    text = extract_text_from_pdf(file.file)

    # Split into clauses
    clauses = split_into_clauses(text)

    # Save document metadata
    document = crud.create_document(
        db=db,
        filename=file.filename
    )

    results = []

    for clause in clauses:
        results.append({
            "clause_text": clause,
            "analysis": analyze_clause(clause)
        })

    return {
        "document_id": document.id,
        "total_clauses": len(results),
        "results": results
    }
