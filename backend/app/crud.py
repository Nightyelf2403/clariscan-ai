from sqlalchemy.orm import Session
from . import models


def create_document(db: Session, filename: str):
    document = models.Document(filename=filename)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document
