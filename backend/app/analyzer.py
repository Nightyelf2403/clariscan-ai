from typing import Dict, List
import re

from .rules.catalog import RULES, Rule


# -------------------------
# Utilities
# -------------------------

def _normalize(text: str) -> str:
    """
    Normalize text for matching:
    - lowercase
    - remove punctuation
    - collapse whitespace
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _rule_matches(rule: Rule, text: str) -> int:
    """
    Returns number of keyword matches for a rule.
    We trigger a rule if at least ONE keyword matches.
    """
    hits = 0
    for kw in rule.keywords:
        kw_norm = _normalize(kw)
        if kw_norm in text:
            hits += 1
    return hits


# -------------------------
# Clause Analysis
# -------------------------

def analyze_clause(clause_text: str) -> Dict:
    """
    Analyze a single clause and return the highest-risk finding (if any).
    """
    normalized = _normalize(clause_text)

    triggered = []

    for rule in RULES:
        hits = _rule_matches(rule, normalized)
        if hits > 0:
            triggered.append((rule, hits))

    if not triggered:
        return {
            "clause_type": "General",
            "risk_level": "Low",
            "explanation": "No specific risk indicators detected.",
            "suggestion": None,
        }

    # Sort by:
    # 1. Risk severity
    # 2. Number of keyword hits
    risk_rank = {"High": 3, "Medium": 2, "Low": 1}
    triggered.sort(
        key=lambda x: (risk_rank[x[0].risk_level], x[1]),
        reverse=True,
    )

    top_rule, hits = triggered[0]

    return {
        "clause_type": top_rule.title,
        "risk_level": top_rule.risk_level,
        "explanation": top_rule.description,
        "suggestion": top_rule.suggestion,
    }


# -------------------------
# Document Analysis
# -------------------------

def analyze_document(document_text: str) -> Dict:
    """
    Analyze the entire document and return a structured summary.
    """
    normalized = _normalize(document_text)

    findings = []
    seen_rule_ids = set()

    for rule in RULES:
        hits = _rule_matches(rule, normalized)
        if hits > 0 and rule.id not in seen_rule_ids:
            seen_rule_ids.add(rule.id)
            findings.append({
                "id": rule.id,
                "title": rule.title,
                "risk_level": rule.risk_level,
                "description": rule.description,
                "suggestion": rule.suggestion,
                "matched_keywords": hits,
            })

    high = [f for f in findings if f["risk_level"] == "High"]
    medium = [f for f in findings if f["risk_level"] == "Medium"]
    low = [f for f in findings if f["risk_level"] == "Low"]

    return {
        "total_findings": len(findings),
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low,
        "all_findings": findings,
    }