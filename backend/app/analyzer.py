from typing import Dict
import re


from .rules.catalog import RULES, Rule
#
# -------------------------
# Document Type Detection
# -------------------------

CONTRACT_KEYWORDS = [
    "agreement", "this agreement", "terms and conditions", "governing law",
    "liability", "indemnification", "termination", "whereas", "party", "parties"
]

NON_CONTRACT_KEYWORDS = [
    "resume", "curriculum vitae", "experience", "education",
    "skills", "projects", "certifications", "summary"
]

def detect_document_type(document_text: str) -> dict:
    text = _normalize(document_text)

    contract_score = sum(2 for kw in CONTRACT_KEYWORDS if kw in text)
    non_contract_score = sum(2 for kw in NON_CONTRACT_KEYWORDS if kw in text)

    # Bonus if agreement appears early
    first_chunk = text[: max(200, int(len(text) * 0.2))]
    if "agreement" in first_chunk:
        contract_score += 5

    confidence = 0.0
    doc_type = "contract"

    if non_contract_score > contract_score or contract_score < 6:
        doc_type = "non_contract"
        confidence = round(min(1.0, non_contract_score / max(1, non_contract_score + contract_score)), 2)
    else:
        confidence = round(min(1.0, contract_score / max(1, non_contract_score + contract_score)), 2)

    return {
        "document_type": doc_type,
        "confidence": confidence,
        "reason": (
            "This document appears to be a resume or non-contract document."
            if doc_type == "non_contract"
            else "This document appears to be a legal contract."
        ),
    }


OBLIGATION_CONTEXTS = {
    "termination": ["terminate", "termination", "end this agreement"],
    "payment": ["pay", "payment", "invoice", "late", "late fee", "interest"],
    "reporting": ["report", "notify", "inform", "notice"],
    "cure": ["cure", "fix", "remedy"],
    "return": ["return", "surrender", "vacate"],
    "insurance": ["insurance", "claim", "coverage"],
}



# -------------------------
# Clause-level Evidence Helpers
# -------------------------

def _extract_matched_keywords(rule: Rule, text: str) -> list[str]:
    matched = []
    norm_text = _normalize(text)
    for kw in getattr(rule, "keywords", []):
        if _normalize(kw) in norm_text:
            matched.append(kw)
    for ph in getattr(rule, "phrases", []):
        if _normalize(ph) in norm_text:
            matched.append(ph)
    return list(dict.fromkeys(matched))


def _extract_matching_sentence(text: str, keywords: list[str]) -> str | None:
    if not keywords:
        return None
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for sentence in sentences:
        s_norm = sentence.lower()
        for kw in keywords:
            if kw.lower() in s_norm:
                return sentence.strip()
    return None


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


def _classify_obligation(text: str) -> str | None:
    t = text.lower()
    for label, keywords in OBLIGATION_CONTEXTS.items():
        if any(k in t for k in keywords):
            return label
    return None

# Human-readable obligation explanation helper
def explain_obligation(obligation: str | None) -> str | None:
    return {
        "payment": "You must pay invoices within the specified time",
        "termination": "You must follow termination notice requirements",
        "cure": "You must fix the breach within the allowed cure period",
        "reporting": "You must report or notify within the required time",
        "return": "You must return property or assets as required",
        "insurance": "You must maintain required insurance coverage",
    }.get(obligation)





# -------------------------
# Time Extraction Helpers
# -------------------------

# Patterns for numbers written as digits or words (up to 99)
NUM_WORDS = {
    "one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9,
    "ten":10, "eleven":11, "twelve":12, "thirteen":13, "fourteen":14, "fifteen":15,
    "sixteen":16, "seventeen":17, "eighteen":18, "nineteen":19, "twenty":20,
    "thirty":30, "forty":40, "fifty":50, "sixty":60, "seventy":70, "eighty":80, "ninety":90
}

def _word_to_num(word: str) -> int | None:
    word = word.lower()
    if word.isdigit():
        return int(word)
    if word in NUM_WORDS:
        return NUM_WORDS[word]
    # Handle compound words like twenty-one
    if '-' in word:
        parts = word.split('-')
        total = 0
        for part in parts:
            if part in NUM_WORDS:
                total += NUM_WORDS[part]
            else:
                return None
        return total if total > 0 else None
    return None

# Regex to capture time expressions like "3 years", "three (3) years", "90-day cure period", "within 48 hrs"
TIME_UNITS = {
    "years": r"years?|yrs?|y",
    "months": r"months?|mos?|mth",
    "weeks": r"weeks?|wks?|w",
    "days": r"days?|d",
    "hours": r"hours?|hrs?|h",
}

# Build a combined regex pattern to match numbers and units
# Capture number (word or digit), optional parenthetical number, then unit
TIME_PATTERN = re.compile(
    r"\b(?P<num_word>\w+)?\s*(\(?\s*(?P<num_digit>\d+)\s*\))?\s*(?P<unit>" +
    "|".join(TIME_UNITS.values()) +
    r")\b",
    re.IGNORECASE
)

def _extract_time_values(text: str) -> list[dict]:
    results = []
    for match in TIME_PATTERN.finditer(text):
        num_word = match.group("num_word")
        num_digit = match.group("num_digit")
        unit_raw = match.group("unit").lower()
        # Normalize unit to singular form used in output
        unit = None
        for key, pattern in TIME_UNITS.items():
            if re.fullmatch(pattern, unit_raw, re.IGNORECASE):
                unit = key
                break
        if not unit:
            continue
        # Determine value: prefer digit if present, else parse word
        value = None
        if num_digit:
            value = int(num_digit)
        elif num_word:
            value = _word_to_num(num_word)
        if value is None:
            continue
        raw_text = match.group(0).strip()
        results.append({
            "value": value,
            "unit": unit,
            "raw_text": raw_text,
            "applies_to": None,
            "trigger": None,
        })
    return results


# -------------------------
# Percentage & Money Extraction Helpers
# -------------------------

PERCENT_PATTERN = re.compile(
    r"(?P<value>\d+(?:\.\d+)?)\s*%"
)

NUMBER_PATTERN = re.compile(r"\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b")

MONEY_CONTEXT_WORDS = {
    "fee", "fees", "penalty", "fine",
    "liability", "damages", "amount", "cost", "charge"
}

TIME_UNITS_SIMPLE = ["day", "days", "month", "months", "year", "years", "hrs", "hours"]

def _extract_percentages(text: str) -> list[dict]:
    results = []

    for m in PERCENT_PATTERN.finditer(text):
        value = float(m.group("value"))
        raw = m.group(0)

        # Window-based context detection
        window_start = max(0, m.start() - 40)
        window_end = min(len(text), m.end() + 40)
        window = text[window_start:window_end].lower()

        context = None
        if "interest" in window:
            context = "interest"
        elif "penalty" in window or "fine" in window:
            context = "penalty"
        elif "late" in window:
            context = "late_payment"

        # Frequency detection
        frequency = None
        if "per month" in window:
            frequency = "per month"
        elif "per year" in window or "annually" in window:
            frequency = "per year"

        # Human-readable explanation
        if context == "interest":
            explanation = f"Interest of {value}% applies if payment is late"
        elif context == "penalty":
            explanation = f"A penalty of {value}% applies if payment remains unpaid"
        else:
            explanation = f"A rate of {value}% applies"

        results.append({
            "type": "percentage",
            "value": value,
            "unit": "percent",
            "raw_text": raw,
            "context": context,
            "frequency": frequency,
            "applies_to": context,
            "trigger": "Late payment" if context in ("interest", "penalty", "late_payment") else None,
            "explanation": explanation,
        })

    return results

# -------------------------
# Percentage Normalization and Deadline Classification Helpers
# -------------------------

def normalize_percentage(percent: dict) -> dict:
    raw = percent.get("raw_text", "").lower()
    value = percent.get("value")

    normalized = percent.copy()

    if "per month" in raw:
        normalized["annual_equivalent"] = round(value * 12, 2)
        normalized["normalized_unit"] = "per_year"
    elif "per week" in raw:
        normalized["annual_equivalent"] = round(value * 52, 2)
        normalized["normalized_unit"] = "per_year"
    elif "per year" in raw or "annually" in raw:
        normalized["annual_equivalent"] = value
        normalized["normalized_unit"] = "per_year"

    return normalized

def classify_deadline(value: int, unit: str) -> str:
    if unit == "hours" or value <= 3:
        return "urgent"
    if unit == "days" and value <= 7:
        return "short"
    if unit == "days" and value <= 30:
        return "normal"
    return "long"

def _extract_money(text: str) -> list[dict]:
    results = []
    for match in NUMBER_PATTERN.finditer(text):
        raw = match.group(0)
        # Strengthen: skip if number is part of a percentage match
        if PERCENT_PATTERN.search(text[max(0, match.start()-1):match.end()+1]):
            continue
        # Skip if number is immediately followed by '%'
        if match.end() < len(text) and text[match.end()] == '%':
            continue
        # Skip if nearby text (±5 chars) contains time units like day, days, month, months, year, years, hrs, hours
        start_context = max(0, match.start() - 5)
        end_context = min(len(text), match.end() + 5)
        context_snippet = text[start_context:end_context].lower()
        if any(unit in context_snippet for unit in TIME_UNITS_SIMPLE):
            continue
        try:
            value = float(raw.replace(",", ""))
        except ValueError:
            continue

        # Tighten rules:
        # Only treat as money if: (a) currency symbol/word exists in same sentence, OR (b) money context word AND currency symbol/word exist
        # Remove 'interest' from context words (already done above)
        # Explicitly skip numbers that are part of a percentage match (already above)
        # Find the sentence containing the number
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentence_found = None
        match_start = match.start()
        match_end = match.end()
        char_count = 0
        for sent in sentences:
            sent_len = len(sent)
            if char_count <= match_start < char_count + sent_len:
                sentence_found = sent
                break
            char_count += sent_len + 1  # +1 for the split char
        window = sentence_found.lower() if sentence_found else text[max(0, match.start()-50):match.end()+50].lower()
        has_currency = any(sym in window for sym in ("$", "usd", "dollar"))
        has_money_context = any(word in window for word in MONEY_CONTEXT_WORDS)
        # Rule (a): currency symbol/word in same sentence
        if has_currency:
            results.append({
                "type": "money",
                "value": value,
                "currency": "$",
                "raw_text": raw,
            })
            continue
        # Rule (b): money context word AND currency symbol/word exist
        if has_money_context and has_currency:
            results.append({
                "type": "money",
                "value": value,
                "currency": "$",
                "raw_text": raw,
            })
            continue
        # Otherwise, do not treat as money
        continue

    return results


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

        matched_keywords = _extract_matched_keywords(rule, clause_text)
        candidates.append({
            "rule": rule,
            "confidence": confidence,
            "matched_keywords": matched_keywords,
        })

    # Replace time_constraints and percentages extraction with normalized versions
    time_constraints = []
    for t in _extract_time_values(clause_text):
        t["severity"] = classify_deadline(t["value"], t["unit"])
        time_constraints.append(t)
    # Infer context for time_constraints based on obligation type
    obligation = _classify_obligation(clause_text)
    for t in time_constraints:
        if obligation == "termination":
            t["applies_to"] = "termination notice"
            t["trigger"] = "Agreement termination"
        elif obligation == "payment":
            t["applies_to"] = "payment deadline"
            t["trigger"] = "Invoice payment"
        elif obligation == "cure":
            t["applies_to"] = "cure period"
            t["trigger"] = "Breach of agreement"

    for t in time_constraints:
        if t.get("applies_to") is None:
            t["applies_to"] = "contractual reference period"
            t["trigger"] = "Contractual limitation or reference"

    percentages = [normalize_percentage(p) for p in _extract_percentages(clause_text)]
    money_values = _extract_money(clause_text)

    obligation = _classify_obligation(clause_text)
    user_must_know = {
        "obligation": obligation,
        "obligation_explanation": explain_obligation(obligation),
        "deadlines": time_constraints,
        "percentages": percentages,
        "money": money_values,
    }

    # Add “important but not risky” extraction (D3)
    important_info = []
    for t in time_constraints:
        important_info.append(
            f"{t['value']} {t['unit']} requirement ({t.get('severity')})"
        )

    for p in percentages:
        important_info.append(
            f"{p['value']}% {p.get('context', 'rate')}"
        )

    if not candidates:
        # Ensure percentages always appear in both analysis and user_must_know
        user_must_know["percentages"] = percentages
        return {
            "clause_type": "General",
            "risk_level": "Low",
            "confidence": 0,
            "explanation": "No legal risk detected, but important obligations may apply.",
            "suggestion": None,
            "triggered_keywords": [],
            "matched_sentence": None,
            "time_constraints": time_constraints,
            "percentages": percentages,
            "money": money_values,
            "user_must_know": user_must_know,
            "obligation_type": obligation,
            "important_but_not_risky": important_info,
        }

    risk_rank = {"High": 3, "Medium": 2, "Low": 1}
    candidates.sort(
        key=lambda x: (risk_rank[x["rule"].risk_level], x["confidence"]),
        reverse=True,
    )

    rule = candidates[0]["rule"]
    matched_keywords = _extract_matched_keywords(rule, clause_text)
    # time_constraints and percentages already set above
    user_must_know["percentages"] = percentages
    return {
        "clause_type": rule.title,
        "risk_level": rule.risk_level,
        "explanation": rule.description,
        "suggestion": rule.suggestion,
        "confidence": candidates[0]["confidence"],
        "triggered_keywords": matched_keywords,
        "matched_sentence": _extract_matching_sentence(clause_text, matched_keywords),
        "time_constraints": time_constraints if time_constraints else [],
        "user_must_know": user_must_know,
        "percentages": percentages,
        "money": money_values,
        "obligation_type": obligation,
        "important_but_not_risky": important_info,
    }


# -------------------------
# Document Analysis
# -------------------------

def analyze_document(document_text: str) -> Dict:
    doc_type_info = detect_document_type(document_text)
    if doc_type_info["document_type"] == "non_contract":
        return {
            "document_type": "non_contract",
            "confidence": doc_type_info["confidence"],
            "reason": doc_type_info["reason"],
            "message": "Please upload a legal contract such as a lease, employment agreement, NDA, or service contract.",
        }
    normalized = _normalize(document_text)
    findings = []
    time_obligations = []

    # Keywords to infer context around time obligations
    CONTEXT_KEYWORDS = {"termination", "cure", "notice", "report", "payment"}

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

    # ---- Deduplicate findings by rule ID (keep highest confidence) ----
    deduped = {}
    for f in findings:
        existing = deduped.get(f["id"])
        if not existing or f["confidence"] > existing["confidence"]:
            deduped[f["id"]] = f
    findings = list(deduped.values())

    # Extract time obligations and percentages from document text
    extracted_times = _extract_time_values(document_text)
    doc_percents = [normalize_percentage(p) for p in _extract_percentages(document_text)]
    doc_money = _extract_money(document_text)
    # For each time found, try to find context word near it (within 10 words)
    doc_tokens = _tokenize(document_text)
    for time_entry in extracted_times:
        # Find position(s) of raw_text in tokens to get context
        raw_text = time_entry["raw_text"].lower()
        raw_words = _normalize(raw_text).split()
        positions = []
        for i in range(len(doc_tokens) - len(raw_words) + 1):
            if doc_tokens[i:i+len(raw_words)] == raw_words:
                positions.append(i)
        context_found = None
        for pos in positions:
            # Look +/- 10 tokens for context keywords
            start = max(0, pos - 10)
            end = min(len(doc_tokens), pos + len(raw_words) + 10)
            window = doc_tokens[start:end]
            for kw in CONTEXT_KEYWORDS:
                if kw in window:
                    context_found = kw
                    break
            if context_found:
                break
        obligation = None
        applies_to = None
        trigger = None

        # Termination takes priority over payment if both appear
        if context_found in ("termination", "notice"):
            obligation = "termination"
            applies_to = "termination notice"
            trigger = "Agreement termination"
        elif context_found == "cure":
            obligation = "cure"
            applies_to = "cure period"
            trigger = "Breach of agreement"
        elif context_found == "payment":
            obligation = "payment"
            applies_to = "payment deadline"
            trigger = "Invoice payment"

        if obligation is None:
            obligation = "reference"
            applies_to = "contractual reference period"
            trigger = "Contractual limitation or reference"

        time_obligations.append({
            "value": time_entry["value"],
            "unit": time_entry["unit"],
            "context": obligation,
            "applies_to": applies_to,
            "trigger": trigger,
            "severity": classify_deadline(time_entry["value"], time_entry["unit"]),
        })

    # Deduplicate time_obligations
    unique = {}
    for t in time_obligations:
        key = (t["value"], t["unit"], t.get("applies_to"))
        unique[key] = t
    time_obligations = list(unique.values())

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
        "time_obligations": time_obligations,
        "user_must_know": {
            "deadlines": time_obligations,
            "percentages": doc_percents,
            "money": doc_money,
        },
    }