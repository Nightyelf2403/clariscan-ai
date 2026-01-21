def analyze_clause(clause_text: str) -> dict:
    text = clause_text.lower()

    if "terminate" in text or "termination" in text:
        return {
            "clause_type": "Termination",
            "risk_level": "High",
            "explanation": "This clause allows one party to terminate the agreement, which may create uncertainty.",
            "suggestion": "Consider adding mutual termination rights and a longer notice period."
        }

    if "liability" in text or "liable" in text:
        return {
            "clause_type": "Liability",
            "risk_level": "High",
            "explanation": "This clause limits or assigns liability, which could expose one party to significant risk.",
            "suggestion": "Review liability caps and exclusions carefully."
        }

    if "payment" in text or "$" in text:
        return {
            "clause_type": "Payment",
            "risk_level": "Medium",
            "explanation": "This clause defines payment obligations that may impact cash flow.",
            "suggestion": "Ensure payment terms and penalties are reasonable."
        }

    if "confidential" in text:
        return {
            "clause_type": "Confidentiality",
            "risk_level": "Low",
            "explanation": "This clause governs confidential information and is generally standard.",
            "suggestion": None
        }

    return {
        "clause_type": "General",
        "risk_level": "Low",
        "explanation": "This clause appears informational or standard.",
        "suggestion": None
    }
