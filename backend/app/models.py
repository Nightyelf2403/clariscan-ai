from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    clauses = relationship(
        "Clause",
        back_populates="document",
        cascade="all, delete"
    )


class Clause(Base):
    __tablename__ = "clauses"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))

    clause_text = Column(Text, nullable=False)
    risk_level = Column(String)
    explanation = Column(Text)
    suggestion = Column(Text)

    document = relationship("Document", back_populates="clauses")
