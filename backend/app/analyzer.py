"""
Analyzer module

ClariScan – Deterministic Document Intelligence Engine

This layer converts raw rule matches into:
- Human-readable insights
- Actionable checklists
- Prioritized review sections
"""

from .rules.catalog import RULES, Rule
from typing import Dict, List
from collections import defaultdict
from .rules.engine import analyze_document_with_rules


SEVERITY_WEIGHT = {
    "High": 3,
    "Medium": 2,
    "Low": 1,
}


def analyze_document(document_text: str) -> Dict:
    """
    Analyze a full document and return structured, human-first intelligence.
    """
    try:
        raw = analyze_document_with_rules(document_text)
    except Exception as e:
        return {
            "risk_overview": {
                "overall_risk": "Unknown",
                "risk_score": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
            },
            "review_now": [],
            "review_soon": [],
            "deadlines": [],
            "payments_and_fees": [],
            "your_obligations": [],
            "rights_you_lose": [],
            "termination_and_exit": [],
            "liability_exposure": [],
            "data_and_privacy": [],
            "action_checklist": [],
            "category_breakdown": {},
            "plain_english_summary": "Analysis failed due to an internal error.",
            "disclaimer": (
                "This analysis is for informational purposes only and "
                "does not constitute legal advice."
            ),
            "error": str(e),
        }

    high = raw.get("high_risk_items", [])
    medium = raw.get("medium_risk_items", [])
    low = raw.get("low_risk_items", [])

    # -------------------------
    # Rank & normalize
    # -------------------------
    all_items = []

    for item in high + medium + low:
        all_items.append({
            "severity": item.get("risk_level", "Low"),
            "category": item.get("category", "General"),
            "summary": item.get("summary", ""),
            "recommendation": item.get("recommendation"),
        })

    all_items.sort(
        key=lambda x: (
            -SEVERITY_WEIGHT.get(x["severity"], 1),
            x["category"],
            x["summary"]
        )
    )

    # -------------------------
    # Buckets people understand
    # -------------------------
    deadlines = []
    payments = []
    obligations = []
    rights_lost = []
    exit_risks = []
    liability = []
    data_privacy = []

    for item in all_items:
        text = item["summary"].lower()

        if any(k in text for k in ["within", "no later than", "by", "before", "after", "days", "months", "years"]):
            deadlines.append(item)

        if any(k in text for k in ["fee", "payment", "penalty", "interest", "charge", "cost"]):
            payments.append(item)

        if any(k in text for k in ["must", "required", "shall", "responsible", "obligated"]):
            obligations.append(item)

        if any(k in text for k in ["waive", "arbitration", "class action", "jury trial", "rights"]):
            rights_lost.append(item)

        if any(k in text for k in ["terminate", "termination", "cancel", "suspend"]):
            exit_risks.append(item)

        if any(k in text for k in ["liability", "indemnify", "damages", "hold harmless"]):
            liability.append(item)

        if any(k in text for k in ["data", "privacy", "personal information", "tracking"]):
            data_privacy.append(item)

    # -------------------------
    # Risk scoring
    # -------------------------
    risk_score = (
        len(high) * 5 +
        len(medium) * 3 +
        len(low) * 1
    )

    if risk_score >= 50:
        overall_risk = "High"
    elif risk_score >= 25:
        overall_risk = "Medium"
    else:
        overall_risk = "Low"

    # -------------------------
    # Category distribution
    # -------------------------
    category_counts = defaultdict(int)
    for item in all_items:
        category_counts[item["category"]] += 1

    # -------------------------
    # Action checklist (MOST IMPORTANT)
    # -------------------------
    checklist = []
    # Only include recommendations from High and Medium risk items, preserve order
    for item in high + medium:
        rec = item.get("recommendation")
        if rec and rec not in checklist:
            checklist.append(rec)
            if len(checklist) >= 20:
                break

    # -------------------------
    # Plain-English summary
    # -------------------------
    summary = (
        f"This document carries an overall {overall_risk.lower()} level of risk. "
        f"It contains {len(high)} high-risk clauses, "
        f"{len(medium)} important obligations, "
        f"and {len(low)} standard terms. "
    )

    if deadlines:
        summary += f"There are {len(deadlines)} time-sensitive requirements. "

    if payments:
        summary += f"Several clauses may result in fees or financial penalties. "

    if rights_lost:
        summary += f"You may be giving up important legal rights in some sections. "

    summary += "Review the highlighted items carefully before agreeing."

    return {
        # Executive overview
        "risk_overview": {
            "overall_risk": overall_risk,
            "risk_score": risk_score,
            "high": len(high),
            "medium": len(medium),
            "low": len(low),
        },

        # What to review first
        "review_now": high[:10],
        "review_soon": medium[:15],

        # Human sections
        "deadlines": deadlines,
        "payments_and_fees": payments,
        "your_obligations": obligations,
        "rights_you_lose": rights_lost,
        "termination_and_exit": exit_risks,
        "liability_exposure": liability,
        "data_and_privacy": data_privacy,

        # Actionable output
        "action_checklist": checklist,

        # Analytics
        "category_breakdown": dict(category_counts),

        # Summary
        "plain_english_summary": summary,

        "disclaimer": (
            "This analysis is for informational purposes only and "
            "does not constitute legal advice."
        ),
    }