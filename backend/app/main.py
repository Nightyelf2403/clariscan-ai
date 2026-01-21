from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session

from .database import engine, SessionLocal
from . import models, crud
from .pdf_utils import extract_text_from_pdf
from .clause_utils import split_into_clauses

# ---------------------------------
# Create database tables on startup
# ---------------------------------
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ClariScan AI")


# ---------------------------------
# Database Dependency
# ---------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------
# Health Check
# ---------------------------------
@app.get("/")
def health_check():
    return {"status": "ok"}


# ---------------------------------
# Upload + PDF Parsing + Clause Split
# ---------------------------------
@app.post("/upload")
def upload_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Extract raw text from PDF
    extracted_text = extract_text_from_pdf(file.file)

    # 2. Split text into logical clauses
    clauses = split_into_clauses(extracted_text)

    # 3. Store document metadata
    document = crud.create_document(
        db=db,
        filename=file.filename
    )

    # 4. Return validation response (temporary)
    return {
        "document_id": document.id,
        "filename": document.filename,
        "total_clauses": len(clauses),
        "sample_clauses": clauses[:3]
    }
