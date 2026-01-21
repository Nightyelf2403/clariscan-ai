from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session

from .database import engine, SessionLocal
from . import models, crud
from .pdf_utils import extract_text_from_pdf
from .clause_utils import split_into_clauses
from .analyzer import analyze_clause

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ClariScan AI")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/analyze")
def analyze_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    text = extract_text_from_pdf(file.file)
    clauses = split_into_clauses(text)

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
