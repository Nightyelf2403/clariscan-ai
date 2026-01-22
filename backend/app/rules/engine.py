from typing import List, Dict
import re
from .catalog import RULES, Rule


def analyze_document_with_rules(text: str) -> List[Dict]:
    findings = []
    text = text.lower()

    for rule in RULES:
        for pattern in rule.patterns:
            if re.search(pattern, text):
                findings.append({
                    "rule_id": rule.id,
                    "category": rule.category,
                    "severity": rule.severity,
                    "summary": rule.summary,
                    "recommendation": rule.recommendation,
                })
                break

    return findings