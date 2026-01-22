from typing import Dict
import re

from .rules.catalog import RULES, Rule


# -------------------------
# Utilities
# -------------------------

NEGATIONS = {"not", "no", "without", "never", "none"}


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _tokenize(text: str):
    return _normalize(text).split()


def _is_negated(keyword: str, tokens: list[str], idx: int) -> bool:
    start = max(0, idx - 3)
    return any(tok in NEGATIONS for tok in tokens[start:idx])


def _count_keyword_hits(rule: Rule, text: str) -> int:
    tokens = _tokenize(text)
    hits = 0
    for kw in getattr(rule, "keywords", []):
        kw_norm = _normalize(kw)
        kw_tokens = kw_norm.split()
        if len(kw_tokens) == 1:
            for i, tok in enumerate(tokens):
                if tok == kw_tokens[0]:
                    hits += 0 if _is_negated(kw_tokens[0], tokens, i) else 1
        else:
            phrase = " ".join(kw_tokens)
            if phrase in " ".join(tokens):
                hits += 1
    return hits


def _phrase_hits(rule: Rule, text: str) -> int:
    phrases = getattr(rule, "phrases", [])
    if not phrases:
        return 0
    t = _normalize(text)
    return sum(1 for p in phrases if _normalize(p) in t)


def _proximity_bonus(rule: Rule, text: str) -> int:
    tokens = _tokenize(text)
    kws = [t for k in getattr(rule, "keywords", []) for t in _normalize(k).split()]
    positions = []
    for i, tok in enumerate(tokens):
        if tok in kws:
            positions.append(i)
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            if abs(positions[i] - positions[j]) <= 6:
                return 1
    return 0


def _confidence_score(hits: int, total_keywords: int) -> int:
    if total_keywords <= 0:
        return 0
    return min(100, int((hits / total_keywords) * 100))


# -------------------------
# Clause Analysis
# -------------------------

def analyze_clause(clause_text: str) -> Dict:
    normalized = _normalize(clause_text)
    candidates = []

    for rule in RULES:
        kw_hits = _count_keyword_hits(rule, normalized)
        ph_hits = _phrase_hits(rule, normalized)
        prox = _proximity_bonus(rule, normalized)
        effective_hits = max(0, kw_hits + ph_hits + prox)

        if effective_hits < rule.min_hits:
            continue

        confidence = _confidence_score(
            effective_hits,
            max(1, len(getattr(rule, "keywords", [])))
        )

        candidates.append({
            "rule": rule,
            "confidence": confidence,
        })

    if not candidates:
        return {
            "clause_type": "General",
            "risk_level": "Low",
            "explanation": "No specific risk indicators detected.",
            "suggestion": None,
            "confidence": 0,
        }

    risk_rank = {"High": 3, "Medium": 2, "Low": 1}
    candidates.sort(
        key=lambda x: (risk_rank[x["rule"].risk_level], x["confidence"]),
        reverse=True,
    )

    rule = candidates[0]["rule"]
    return {
        "clause_type": rule.title,
        "risk_level": rule.risk_level,
        "explanation": rule.description,
        "suggestion": rule.suggestion,
        "confidence": candidates[0]["confidence"],
    }


# -------------------------
# Document Analysis
# -------------------------

def analyze_document(document_text: str) -> Dict:
    normalized = _normalize(document_text)
    findings = []

    for rule in RULES:
        kw_hits = _count_keyword_hits(rule, normalized)
        ph_hits = _phrase_hits(rule, normalized)
        prox = _proximity_bonus(rule, normalized)
        effective_hits = max(0, kw_hits + ph_hits + prox)

        if effective_hits < rule.min_hits:
            continue

        confidence = _confidence_score(
            effective_hits,
            max(1, len(getattr(rule, "keywords", [])))
        )

        findings.append({
            "id": rule.id,
            "title": rule.title,
            "risk_level": rule.risk_level,
            "description": rule.description,
            "suggestion": rule.suggestion,
            "matched_keywords": effective_hits,
            "confidence": confidence,
        })

    weights = {"High": 3, "Medium": 2, "Low": 1}
    if findings:
        total_weight = sum(weights[f["risk_level"]] * f["confidence"] for f in findings)
        max_weight = sum(weights[f["risk_level"]] * 100 for f in findings)
        document_risk_score = int((total_weight / max_weight) * 100) if max_weight else 0
    else:
        document_risk_score = 0

    high = [f for f in findings if f["risk_level"] == "High"]
    medium = [f for f in findings if f["risk_level"] == "Medium"]
    low = [f for f in findings if f["risk_level"] == "Low"]

    for group in (high, medium, low):
        group.sort(key=lambda x: x["confidence"], reverse=True)

    return {
        "total_findings": len(findings),
        "document_risk_score": document_risk_score,
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low,
        "all_findings": findings,
    }