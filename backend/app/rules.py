# backend/app/rules.py

from dataclasses import dataclass
from typing import List


@dataclass
class Rule:
    id: str
    category: str
    severity: str
    patterns: List[str]
    summary: str
    recommendation: str


RULES: List[Rule] = [

# =========================
# 🔴 CRITICAL ALERTS (1–20)
# =========================

Rule("ONE_SIDED_TERMINATION", "critical_alert", "high",
     ["may terminate at any time", "without cause", "sole discretion"],
     "Other party can terminate the agreement without reason.",
     "Seek mutual termination rights or notice period."),

Rule("IMMEDIATE_TERMINATION", "critical_alert", "high",
     ["immediate termination", "terminate immediately"],
     "Agreement can be terminated immediately without warning.",
     "Negotiate advance notice."),

Rule("AUTO_TERMINATION", "critical_alert", "high",
     ["automatically terminates", "shall automatically terminate"],
     "Agreement ends automatically under certain conditions.",
     "Clarify triggers and consequences."),

Rule("UNILATERAL_MODIFICATION", "critical_alert", "high",
     ["may modify at any time", "change terms without notice"],
     "Terms can be changed unilaterally.",
     "Require notice and consent."),

Rule("SERVICE_SUSPENSION", "critical_alert", "high",
     ["suspend services", "suspend access"],
     "Service can be suspended at any time.",
     "Ask for notice and remediation period."),

Rule("ACCOUNT_TERMINATION", "critical_alert", "high",
     ["terminate your account", "close your account"],
     "Account can be closed unilaterally.",
     "Confirm refund or data export rights."),

Rule("NO_REFUNDS", "critical_alert", "high",
     ["no refunds", "non-refundable"],
     "Payments are non-refundable.",
     "Evaluate financial risk carefully."),

Rule("LIABILITY_EXCLUSION", "critical_alert", "high",
     ["not liable", "no liability"],
     "Other party disclaims liability entirely.",
     "Negotiate reasonable liability caps."),

Rule("INDEMNIFICATION", "critical_alert", "high",
     ["indemnify", "hold harmless"],
     "You must cover losses caused by claims.",
     "Understand financial exposure."),

Rule("ARBITRATION_MANDATORY", "critical_alert", "high",
     ["binding arbitration"],
     "Disputes must go through arbitration.",
     "Understand limits of arbitration."),

Rule("CLASS_ACTION_WAIVER", "critical_alert", "high",
     ["class action waiver"],
     "You waive class action rights.",
     "Assess impact on legal rights."),

Rule("WAIVE_JURY_TRIAL", "critical_alert", "high",
     ["waive jury trial"],
     "You waive the right to jury trial.",
     "Understand dispute resolution impact."),

Rule("NO_APPEAL", "critical_alert", "high",
     ["no right to appeal"],
     "Decisions may be final with no appeal.",
     "Confirm fairness of resolution process."),

Rule("GOVERNING_LAW_REMOTE", "critical_alert", "high",
     ["governed by the laws of"],
     "Agreement governed by potentially unfavorable jurisdiction.",
     "Check jurisdiction fairness."),

Rule("UNILATERAL_ASSIGNMENT", "critical_alert", "high",
     ["assign without consent"],
     "Contract can be transferred without your approval.",
     "Request consent requirement."),

Rule("DATA_OWNERSHIP_TRANSFER", "critical_alert", "high",
     ["own your data", "perpetual license"],
     "You grant ownership or unlimited rights to your data.",
     "Limit scope and duration."),

Rule("SURVIVAL_CLAUSES", "critical_alert", "high",
     ["survive termination"],
     "Obligations continue after termination.",
     "Understand long-term impact."),

Rule("FORCE_MAJEURE_ABUSE", "critical_alert", "high",
     ["force majeure"],
     "Broad force majeure may excuse performance.",
     "Limit scope of force majeure."),

Rule("NO_SERVICE_GUARANTEE", "critical_alert", "high",
     ["as is", "no warranty"],
     "Service is provided without guarantees.",
     "Assess reliability risk."),

Rule("UNLIMITED_MONITORING", "critical_alert", "high",
     ["monitor all activity"],
     "Your activity may be continuously monitored.",
     "Review privacy implications."),

# =========================
# 🟠 REVIEW REQUIRED (21–45)
# =========================

Rule("AUTO_RENEWAL", "review_required", "medium",
     ["automatically renew", "auto-renewal"],
     "Agreement renews automatically.",
     "Check cancellation timing."),

Rule("NOTICE_PERIOD", "review_required", "medium",
     ["written notice", "notice period"],
     "Formal notice is required for actions.",
     "Track deadlines carefully."),

Rule("LATE_FEES", "review_required", "medium",
     ["late fee", "penalty"],
     "Late payments incur penalties.",
     "Confirm fee reasonableness."),

Rule("INTEREST_CHARGES", "review_required", "medium",
     ["interest per month", "annual percentage"],
     "Interest applies to unpaid balances.",
     "Calculate long-term cost."),

Rule("PAYMENT_CHANGES", "review_required", "medium",
     ["change pricing", "revise fees"],
     "Pricing may change.",
     "Request notice clause."),

Rule("LIMITED_SUPPORT", "review_required", "medium",
     ["no obligation to support"],
     "Support may be limited or unavailable.",
     "Clarify support expectations."),

Rule("USAGE_LIMITS", "review_required", "medium",
     ["usage limits", "fair use"],
     "Usage is restricted.",
     "Confirm limits meet needs."),

Rule("DATA_RETENTION", "review_required", "medium",
     ["retain data", "store data"],
     "Data retention policies apply.",
     "Confirm deletion rights."),

Rule("CONFIDENTIALITY_SCOPE", "review_required", "medium",
     ["confidential information"],
     "Broad confidentiality obligations.",
     "Ensure mutual obligations."),

Rule("AUDIT_RIGHTS", "review_required", "medium",
     ["audit", "inspect records"],
     "Other party may audit records.",
     "Limit scope and frequency."),

Rule("SUBCONTRACTING", "review_required", "medium",
     ["subcontract", "third parties"],
     "Work may be subcontracted.",
     "Confirm accountability."),

Rule("SERVICE_CHANGES", "review_required", "medium",
     ["change service features"],
     "Features may change.",
     "Confirm core functionality protection."),

Rule("TERMINATION_FEES", "review_required", "medium",
     ["early termination fee"],
     "Ending early incurs fees.",
     "Calculate exit cost."),

Rule("DATA_EXPORT_LIMITS", "review_required", "medium",
     ["export data"],
     "Data export may be limited.",
     "Confirm portability."),

Rule("REPUTATION_CLAUSE", "review_required", "medium",
     ["non-disparagement"],
     "Restrictions on public statements.",
     "Understand speech limits."),

Rule("INSURANCE_REQUIREMENT", "review_required", "medium",
     ["insurance required"],
     "You must maintain insurance.",
     "Verify coverage cost."),

Rule("CHANGE_CONTROL", "review_required", "medium",
     ["change control"],
     "Changes require approval process.",
     "Understand flexibility."),

Rule("ESCALATION_PROCESS", "review_required", "medium",
     ["escalation"],
     "Disputes must follow escalation path.",
     "Confirm timelines."),

Rule("EXPORT_CONTROLS", "review_required", "medium",
     ["export control laws"],
     "Export regulations apply.",
     "Confirm compliance obligations."),

Rule("BACKGROUND_CHECKS", "review_required", "medium",
     ["background check"],
     "Background checks may be required.",
     "Understand privacy impact."),

# =========================
# 🟢 GENERAL NOTES (46–90)
# =========================

Rule("GOVERNING_LAW", "general_note", "low",
     ["governing law"],
     "Specifies applicable law.",
     "Note jurisdiction."),

Rule("ENTIRE_AGREEMENT", "general_note", "low",
     ["entire agreement"],
     "Document represents entire agreement.",
     "No side agreements allowed."),

Rule("SEVERABILITY", "general_note", "low",
     ["severable"],
     "Invalid clauses won't void entire agreement.",
     "Standard clause."),

Rule("HEADINGS", "general_note", "low",
     ["headings are for convenience"],
     "Headings do not affect interpretation.",
     "Standard legal wording."),

Rule("COUNTERPARTS", "general_note", "low",
     ["counterparts"],
     "Agreement may be signed in parts.",
     "Administrative detail."),

Rule("ELECTRONIC_SIGNATURES", "general_note", "low",
     ["electronic signatures"],
     "Electronic signatures are valid.",
     "Standard clause."),

Rule("NO_WAIVER", "general_note", "low",
     ["no waiver"],
     "Failure to enforce is not a waiver.",
     "Standard protection."),

Rule("AMENDMENTS_IN_WRITING", "general_note", "low",
     ["in writing"],
     "Changes must be written.",
     "Standard clause."),

Rule("NOTICES", "general_note", "low",
     ["notices shall be sent"],
     "Specifies notice method.",
     "Track contact details."),

Rule("RELATIONSHIP", "general_note", "low",
     ["independent contractor"],
     "Defines relationship.",
     "Clarifies legal status."),

Rule("COMPLIANCE_WITH_LAW", "general_note", "low",
     ["comply with laws"],
     "Requires legal compliance.",
     "Standard obligation."),

Rule("SURVIVAL", "general_note", "low",
     ["shall survive"],
     "Some clauses survive termination.",
     "Note ongoing obligations."),

Rule("FORCE_MAJEURE", "general_note", "low",
     ["force majeure"],
     "Excuses performance under extreme events.",
     "Standard clause."),

Rule("ASSIGNMENT", "general_note", "low",
     ["assignment"],
     "Defines assignment rights.",
     "Review transfer conditions."),

Rule("SUCCESSORS", "general_note", "low",
     ["successors and assigns"],
     "Applies to future entities.",
     "Standard clause."),

Rule("WAIVER_DELAY", "general_note", "low",
     ["delay in enforcement"],
     "Delays do not waive rights.",
     "Standard wording."),

Rule("TIME_OF_ESSENCE", "general_note", "low",
     ["time is of the essence"],
     "Deadlines are strict.",
     "Watch timelines carefully."),

Rule("COUNTERCLAIMS", "general_note", "low",
     ["counterclaims"],
     "Limits counterclaims.",
     "Procedural note."),

Rule("CUMULATIVE_REMEDIES", "general_note", "low",
     ["cumulative remedies"],
     "Remedies are cumulative.",
     "Legal standard."),

Rule("INTERPRETATION", "general_note", "low",
     ["interpretation"],
     "Rules for interpreting terms.",
     "Standard clause."),
]