import re
from collections import defaultdict
from dataclasses import dataclass
from typing import List

"""
Deterministic rule catalog for ClariScan AI.

This file contains the full set of contract, policy, and legal risk rules
used for static document analysis across multiple domains
(leases, employment, finance, consumer, government, SaaS, etc.).
"""

@dataclass(frozen=True)
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

# =========================
# 🔴 FINANCIAL & PAYMENT RISKS (91–120)
# =========================

Rule("CREDIT_RISK", "financial_risk", "high",
     ["credit risk", "creditworthiness", "credit check"],
     "Risk related to creditworthiness of parties.",
     "Assess credit risk and require guarantees."),

Rule("DEFAULT_INTEREST", "financial_risk", "high",
     ["default interest", "interest on overdue"],
     "High interest charged on overdue payments.",
     "Negotiate reasonable default interest rates."),

Rule("CURRENCY_RISK", "financial_risk", "medium",
     ["currency fluctuation", "exchange rate risk"],
     "Payments exposed to currency exchange fluctuations.",
     "Consider hedging or fixed currency terms."),

Rule("FINANCIAL_STATEMENTS", "financial_risk", "medium",
     ["financial statements", "audited accounts"],
     "Requirement to provide financial reports.",
     "Confirm confidentiality and frequency."),

Rule("SECURITY_INTEREST", "financial_risk", "high",
     ["security interest", "collateral", "pledge assets"],
     "Assets may be used as collateral.",
     "Understand scope and enforcement rights."),

Rule("LATE_PAYMENT_PENALTY", "financial_risk", "medium",
     ["late payment penalty", "penalty interest"],
     "Penalties apply for late payments.",
     "Clarify penalty amounts and grace periods."),

Rule("DEBT_ACCELERATION", "financial_risk", "high",
     ["debt acceleration", "immediate repayment"],
     "Debt may become due immediately upon default.",
     "Negotiate cure periods and limits."),

Rule("NON_PAYMENT_TERMINATION", "financial_risk", "high",
     ["terminate for non-payment", "suspend for non-payment"],
     "Contract can be terminated for non-payment.",
     "Seek notice and cure rights."),

Rule("REFUND_RESTRICTIONS", "financial_risk", "medium",
     ["no refunds", "non-refundable fees"],
     "Payments may be non-refundable.",
     "Confirm refund policies carefully."),

Rule("ESCROW_REQUIREMENT", "financial_risk", "medium",
     ["escrow account", "funds held in escrow"],
     "Funds to be held in escrow.",
     "Confirm terms and release conditions."),

Rule("BILLING_DISPUTE", "financial_risk", "medium",
     ["billing dispute", "invoice challenge"],
     "Dispute resolution for billing issues.",
     "Ensure fair dispute process."),

Rule("TAX_RESPONSIBILITY", "financial_risk", "medium",
     ["tax responsibility", "tax indemnity"],
     "Taxes may be allocated to one party.",
     "Clarify tax obligations and liabilities."),

Rule("PRICE_ADJUSTMENT", "financial_risk", "medium",
     ["price adjustment", "price change clause"],
     "Prices may be adjusted during contract.",
     "Require advance notice and limits."),

Rule("CREDIT_LIMIT", "financial_risk", "medium",
     ["credit limit", "maximum credit"],
     "Limits on credit extended.",
     "Confirm limits and consequences."),

Rule("INVOICE_TIMING", "financial_risk", "low",
     ["invoice timing", "billing cycle"],
     "Defines when invoices are issued.",
     "Track billing dates carefully."),

# =========================
# 🟠 EMPLOYMENT & JOB CONTRACT RISKS (121–150)
# =========================

Rule("NON_COMPETE", "employment_contract", "high",
     ["non-compete", "restrict competition"],
     "Restricts employee's future employment.",
     "Evaluate scope and duration carefully."),

Rule("AT_WILL_TERMINATION", "employment_contract", "high",
     ["at-will employment", "terminate at will"],
     "Employment can be ended without cause.",
     "Seek severance or notice provisions."),

Rule("CONFIDENTIALITY_EMPLOYEE", "employment_contract", "medium",
     ["employee confidentiality", "non-disclosure agreement"],
     "Employee must keep information confidential.",
     "Clarify scope and duration."),

Rule("INTELLECTUAL_PROPERTY_ASSIGNMENT", "employment_contract", "high",
     ["assign inventions", "work product ownership"],
     "Employer owns employee inventions.",
     "Confirm scope and fairness."),

Rule("NON_SOLICITATION", "employment_contract", "medium",
     ["non-solicitation", "no solicitation"],
     "Restricts employee from soliciting clients or staff.",
     "Check duration and geographic scope."),

Rule("COMPENSATION_CHANGES", "employment_contract", "medium",
     ["change compensation", "salary adjustment"],
     "Employer can change pay terms.",
     "Seek notice and agreement."),

Rule("BENEFITS_TERMINATION", "employment_contract", "medium",
     ["terminate benefits", "end health coverage"],
     "Benefits may be terminated unexpectedly.",
     "Confirm continuation rights."),

Rule("DISCIPLINARY_ACTIONS", "employment_contract", "medium",
     ["disciplinary procedures", "progressive discipline"],
     "Defines how discipline is handled.",
     "Ensure fair process."),

Rule("ARBITRATION_EMPLOYMENT", "employment_contract", "high",
     ["employment arbitration", "binding arbitration"],
     "Employment disputes must go to arbitration.",
     "Assess impact on employee rights."),

Rule("WORK_HOURS", "employment_contract", "low",
     ["work hours", "overtime"],
     "Defines working hours and overtime rules.",
     "Track hours and compensation."),

Rule("LEAVE_POLICIES", "employment_contract", "low",
     ["leave entitlement", "vacation policy"],
     "Specifies employee leave rights.",
     "Confirm compliance with law."),

Rule("JOB_DESCRIPTION", "employment_contract", "low",
     ["job duties", "position description"],
     "Defines employee responsibilities.",
     "Clarify scope to avoid disputes."),

Rule("PROBATION_PERIOD", "employment_contract", "medium",
     ["probation period", "trial period"],
     "Initial employment evaluation period.",
     "Confirm rights and termination during probation."),

Rule("SEVERANCE_PAY", "employment_contract", "high",
     ["severance pay", "termination compensation"],
     "Compensation upon termination.",
     "Negotiate terms clearly."),

Rule("INTELLECTUAL_PROPERTY_RETURN", "employment_contract", "medium",
     ["return company property", "intellectual property return"],
     "Employee must return IP and property on termination.",
     "Define scope and timing."),

# =========================
# 🟠 HOUSING / LEASE RISKS (151–175)
# =========================

Rule("RENT_INCREASE", "lease_housing", "medium",
     ["rent increase", "rent adjustment"],
     "Landlord can increase rent.",
     "Confirm limits and notice periods."),

Rule("SECURITY_DEPOSIT", "lease_housing", "medium",
     ["security deposit", "damage deposit"],
     "Deposit held against damages or unpaid rent.",
     "Clarify refund conditions."),

Rule("EARLY_TERMINATION_LEASE", "lease_housing", "high",
     ["early termination", "break lease"],
     "Tenant may be liable for early termination fees.",
     "Seek flexible termination options."),

Rule("MAINTENANCE_RESPONSIBILITY", "lease_housing", "medium",
     ["maintenance responsibility", "repair obligations"],
     "Defines who maintains property.",
     "Clarify landlord and tenant duties."),

Rule("ACCESS_RIGHTS", "lease_housing", "medium",
     ["landlord access", "entry notice"],
     "Landlord's right to enter property.",
     "Confirm notice requirements."),

Rule("PETS_POLICY", "lease_housing", "low",
     ["pets allowed", "no pets"],
     "Rules regarding pets on premises.",
     "Confirm pet restrictions."),

Rule("LEASE_RENEWAL", "lease_housing", "medium",
     ["lease renewal", "renewal option"],
     "Options for lease renewal.",
     "Clarify terms and notice."),

Rule("UTILITIES_PAYMENT", "lease_housing", "low",
     ["utilities payment", "utility charges"],
     "Who pays for utilities.",
     "Confirm responsibilities."),

Rule("OCCUPANCY_LIMITS", "lease_housing", "low",
     ["occupancy limits", "maximum occupants"],
     "Limits on number of occupants.",
     "Confirm compliance."),

Rule("SUBLETTING", "lease_housing", "medium",
     ["subletting", "sublease"],
     "Restrictions on subletting property.",
     "Negotiate permissions."),

Rule("LEASE_ASSIGNMENT", "lease_housing", "medium",
     ["assign lease", "lease assignment"],
     "Rights to assign lease to another.",
     "Clarify consent requirements."),

Rule("DEFAULT_TERMS", "lease_housing", "high",
     ["default on rent", "rent arrears"],
     "Consequences of rent default.",
     "Seek cure periods and limits."),

Rule("PROPERTY_DAMAGE", "lease_housing", "high",
     ["property damage", "tenant liability"],
     "Tenant liable for damages.",
     "Clarify scope and process."),

Rule("INSURANCE_REQUIREMENTS_LEASE", "lease_housing", "medium",
     ["tenant insurance", "rental insurance"],
     "Insurance requirements for tenant.",
     "Confirm coverage and proof."),

Rule("TERMINATION_NOTICE", "lease_housing", "medium",
     ["termination notice", "notice to vacate"],
     "Notice requirements for ending lease.",
     "Track deadlines carefully."),

# =========================
# 🔴 PRIVACY & DATA RISKS (176–205)
# =========================

Rule("DATA_SHARING", "privacy_data", "high",
     ["share data with third parties", "data sharing"],
     "Data may be shared with others.",
     "Limit sharing and require consent."),

Rule("DATA_RETENTION_POLICY", "privacy_data", "medium",
     ["data retention", "store data for"],
     "Specifies how long data is kept.",
     "Confirm retention limits and deletion rights."),

Rule("DATA_BREACH_NOTIFICATION", "privacy_data", "high",
     ["data breach notification", "security incident"],
     "Requirements to notify on data breaches.",
     "Ensure timely and clear notification."),

Rule("PERSONAL_DATA_USAGE", "privacy_data", "high",
     ["use personal data", "process personal information"],
     "How personal data is used.",
     "Limit usage and require compliance."),

Rule("DATA_ENCRYPTION", "privacy_data", "medium",
     ["data encryption", "secure transmission"],
     "Requirements for data security.",
     "Confirm encryption standards."),

Rule("COOKIES_POLICY", "privacy_data", "low",
     ["cookies policy", "tracking cookies"],
     "Use of cookies and tracking technologies.",
     "Disclose usage and obtain consent."),

Rule("DATA_ACCESS_RIGHTS", "privacy_data", "medium",
     ["access personal data", "data subject rights"],
     "Rights to access and correct data.",
     "Ensure compliance with laws."),

Rule("DATA_TRANSFER_RESTRICTIONS", "privacy_data", "high",
     ["international data transfer", "cross-border data"],
     "Restrictions on data transfers across borders.",
     "Confirm legal basis and safeguards."),

Rule("ANONYMIZATION", "privacy_data", "low",
     ["data anonymization", "de-identified data"],
     "Use of anonymized data.",
     "Confirm effectiveness and limits."),

Rule("DATA_PROCESSOR_REQUIREMENTS", "privacy_data", "medium",
     ["data processor", "subprocessor"],
     "Obligations of data processors.",
     "Define responsibilities and audits."),

Rule("PRIVACY_POLICY_UPDATES", "privacy_data", "medium",
     ["privacy policy changes", "policy updates"],
     "Changes to privacy policies.",
     "Require notice and consent."),

Rule("USER_CONSENT", "privacy_data", "high",
     ["user consent", "opt-in consent"],
     "Requirement for user consent.",
     "Ensure valid and documented consent."),

Rule("DATA_MINIMIZATION", "privacy_data", "medium",
     ["data minimization", "limit data collection"],
     "Collect only necessary data.",
     "Confirm scope and compliance."),

Rule("DATA_PORTABILITY", "privacy_data", "medium",
     ["data portability", "data export"],
     "Rights to export personal data.",
     "Confirm process and format."),

Rule("PRIVACY_TRAINING", "privacy_data", "low",
     ["privacy training", "data protection training"],
     "Obligation for privacy training.",
     "Confirm frequency and content."),

# =========================
# 🟠 CONSUMER & USER TERMS (206–230)
# =========================

Rule("WARRANTY_LIMITATIONS", "consumer_terms", "high",
     ["limited warranty", "no warranty"],
     "Limits on product/service warranties.",
     "Clarify coverage and exclusions."),

Rule("RETURN_POLICY", "consumer_terms", "medium",
     ["return policy", "product returns"],
     "Conditions for returning products.",
     "Confirm timelines and conditions."),

Rule("USER_LICENSE", "consumer_terms", "medium",
     ["user license", "limited license"],
     "Scope of user license granted.",
     "Confirm permitted uses and restrictions."),

Rule("USER_CONDUCT", "consumer_terms", "medium",
     ["user conduct", "acceptable use"],
     "Rules for user behavior.",
     "Clarify prohibited actions."),

Rule("THIRD_PARTY_CONTENT", "consumer_terms", "medium",
     ["third-party content", "external links"],
     "Use of third-party materials.",
     "Limit liability and clarify rights."),

Rule("DISPUTE_RESOLUTION_CONSUMER", "consumer_terms", "high",
     ["consumer arbitration", "dispute resolution"],
     "Dispute processes for consumers.",
     "Confirm fairness and accessibility."),

Rule("LIMITATION_OF_DAMAGES", "consumer_terms", "high",
     ["limit damages", "exclusion of liability"],
     "Limits on damages recoverable.",
     "Assess reasonableness."),

Rule("AGE_RESTRICTIONS", "consumer_terms", "medium",
     ["minimum age", "age restriction"],
     "Limits on user age.",
     "Confirm compliance with laws."),

Rule("SUBSCRIPTION_CANCELLATION", "consumer_terms", "medium",
     ["subscription cancellation", "cancel subscription"],
     "Rules for cancelling subscriptions.",
     "Clarify process and penalties."),

Rule("CONTENT_OWNERSHIP", "consumer_terms", "medium",
     ["content ownership", "user-generated content"],
     "Ownership of user content.",
     "Define licenses and rights."),

Rule("ADVERTISING_POLICY", "consumer_terms", "low",
     ["advertising", "promotional content"],
     "Rules regarding advertising.",
     "Clarify restrictions and disclosures."),

Rule("FEEDBACK_LICENSE", "consumer_terms", "low",
     ["feedback license", "use of feedback"],
     "Rights to use user feedback.",
     "Confirm scope and compensation."),

Rule("SERVICE_AVAILABILITY", "consumer_terms", "medium",
     ["service availability", "uptime guarantee"],
     "Guarantees on service availability.",
     "Confirm SLAs and remedies."),

Rule("USER_ACCOUNT_TERMINATION", "consumer_terms", "high",
     ["terminate user account", "account suspension"],
     "Rights to suspend or terminate user accounts.",
     "Seek clear criteria and notice."),

Rule("CONTENT_MODERATION", "consumer_terms", "medium",
     ["content moderation", "remove content"],
     "Rights to moderate or remove content.",
     "Clarify process and appeal."),

# =========================
# 🟠 GOVERNMENT & LEGAL COMPLIANCE (231–255)
# =========================

Rule("ANTI_BRIBERY", "government_legal", "high",
     ["anti-bribery", "anti-corruption"],
     "Prohibits bribery and corruption.",
     "Ensure compliance and training."),

Rule("EXPORT_RESTRICTIONS", "government_legal", "high",
     ["export restrictions", "export control laws"],
     "Limits on exporting goods or technology.",
     "Confirm compliance with laws."),

Rule("SANCTIONS_COMPLIANCE", "government_legal", "high",
     ["economic sanctions", "trade embargo"],
     "Prohibits dealings with sanctioned entities.",
     "Conduct due diligence."),

Rule("ANTI_MONEY_LAUNDERING", "government_legal", "high",
     ["anti-money laundering", "AML compliance"],
     "Requires AML controls.",
     "Implement monitoring and reporting."),

Rule("DATA_PROTECTION_LAWS", "government_legal", "high",
     ["GDPR", "CCPA", "data protection laws"],
     "Compliance with data protection regulations.",
     "Ensure policies and controls."),

Rule("WHISTLEBLOWER_PROTECTIONS", "government_legal", "medium",
     ["whistleblower protection", "reporting misconduct"],
     "Protects whistleblowers.",
     "Confirm reporting channels and protections."),

Rule("GOVERNMENT_AUDITS", "government_legal", "medium",
     ["government audit", "regulatory inspection"],
     "Subject to government audits.",
     "Prepare documentation and compliance."),

Rule("COMPLIANCE_CERTIFICATIONS", "government_legal", "low",
     ["compliance certification", "ISO certification"],
     "Requirements for certifications.",
     "Confirm scope and maintenance."),

Rule("ETHICS_POLICY", "government_legal", "low",
     ["code of ethics", "ethical conduct"],
     "Standards for ethical behavior.",
     "Train and enforce policies."),

Rule("CONFLICT_OF_INTEREST", "government_legal", "medium",
     ["conflict of interest", "disclosure requirements"],
     "Requires disclosure of conflicts.",
     "Implement review processes."),

Rule("RECORD_RETENTION_LAW", "government_legal", "medium",
     ["record retention law", "document retention"],
     "Mandates retention of records.",
     "Confirm retention periods."),

Rule("PROCUREMENT_RULES", "government_legal", "medium",
     ["government procurement", "procurement rules"],
     "Rules for government contracts.",
     "Ensure compliance with procedures."),

Rule("EXPORT_LICENSE", "government_legal", "high",
     ["export license", "export authorization"],
     "Requires licenses for exports.",
     "Obtain and maintain licenses."),

Rule("ANTI_DISCRIMINATION_LAWS", "government_legal", "high",
     ["anti-discrimination", "equal opportunity"],
     "Prohibits discrimination.",
     "Ensure policies and training."),

Rule("FREEDOM_OF_INFORMATION", "government_legal", "medium",
     ["freedom of information", "FOIA requests"],
     "Subject to information disclosure laws.",
     "Prepare response procedures."),

# =========================
# 🔴 ARBITRATION & DISPUTE RESOLUTION RISKS (256–270)
# =========================

Rule("FORUM_SELECTION_CLAUSE", "arbitration_risk", "high",
     ["forum selection", "venue clause"],
     "Specifies venue for disputes.",
     "Confirm convenience and fairness."),

Rule("MANDATORY_ARBITRATION", "arbitration_risk", "high",
     ["mandatory arbitration", "arbitration clause"],
     "Requires arbitration for disputes.",
     "Assess impact on rights and costs."),

Rule("LIMITED_DISCOVERY", "arbitration_risk", "medium",
     ["limited discovery", "restricted evidence"],
     "Limits evidence allowed in disputes.",
     "Evaluate impact on case preparation."),

Rule("CONFIDENTIALITY_ARBITRATION", "arbitration_risk", "medium",
     ["confidential arbitration", "non-disclosure"],
     "Arbitration proceedings are confidential.",
     "Consider implications for transparency."),

Rule("COST_ALLOCATION", "arbitration_risk", "medium",
     ["arbitration costs", "cost allocation"],
     "Specifies who pays arbitration costs.",
     "Negotiate fair cost sharing."),

Rule("JUDGMENT_ENFORCEMENT", "arbitration_risk", "medium",
     ["enforcement of award", "final and binding"],
     "Arbitration awards are final.",
     "Confirm enforceability and appeal rights."),

Rule("MULTIPLE_PARTIES_ARBITRATION", "arbitration_risk", "medium",
     ["class arbitration waiver", "individual arbitration"],
     "Restricts class or collective arbitration.",
     "Assess impact on dispute resolution."),

Rule("ARBITRATOR_SELECTION", "arbitration_risk", "medium",
     ["arbitrator selection", "appoint arbitrator"],
     "Process for selecting arbitrators.",
     "Ensure neutrality and expertise."),

Rule("ARBITRATION_TIME_LIMITS", "arbitration_risk", "low",
     ["time limits arbitration", "statute of limitations"],
     "Deadlines for arbitration claims.",
     "Track and comply with timelines."),

Rule("ARBITRATION_LOCATION", "arbitration_risk", "low",
     ["arbitration location", "hearing venue"],
     "Location of arbitration hearings.",
     "Confirm accessibility and convenience."),
    # =========================
    # 🔴 BANKING & CREDIT CARD TERMS (271–310)
    # =========================

    Rule("CREDIT_LIMIT_CHANGE", "banking_credit", "high",
         ["change your credit limit", "reduce credit limit"],
         "Issuer can change your credit limit at any time.",
         "Monitor credit usage and avoid sudden utilization spikes."),

    Rule("INTEREST_RATE_CHANGE", "banking_credit", "high",
         ["variable interest rate", "interest rate may change"],
         "Interest rate can increase unexpectedly.",
         "Understand triggers for rate increases."),

    Rule("MINIMUM_PAYMENT_TRAP", "banking_credit", "high",
         ["minimum payment", "only minimum due"],
         "Paying minimum prolongs debt and increases interest.",
         "Pay more than minimum whenever possible."),

    Rule("BALANCE_TRANSFER_FEES", "banking_credit", "medium",
         ["balance transfer fee"],
         "Fees apply to balance transfers.",
         "Calculate true transfer cost."),

    Rule("CASH_ADVANCE_FEES", "banking_credit", "high",
         ["cash advance", "cash withdrawal fee"],
         "High fees and interest apply immediately.",
         "Avoid cash advances unless necessary."),

    Rule("FOREIGN_TRANSACTION_FEES", "banking_credit", "medium",
         ["foreign transaction fee"],
         "Extra charges for foreign purchases.",
         "Use cards with no foreign transaction fees."),

    Rule("REWARD_EXPIRATION", "banking_credit", "medium",
         ["reward points expire", "points expiration"],
         "Rewards may expire if unused.",
         "Track and redeem rewards early."),

    Rule("ACCOUNT_CLOSURE_BANK", "banking_credit", "high",
         ["close your account", "account termination"],
         "Bank may close account unilaterally.",
         "Maintain compliance with account terms."),

    Rule("OVERDRAFT_FEES", "banking_credit", "high",
         ["overdraft fee"],
         "High fees for overdrawing account.",
         "Enable alerts or overdraft protection."),

    Rule("CREDIT_REPORTING", "banking_credit", "high",
         ["report to credit bureau", "credit reporting"],
         "Negative activity may be reported to credit bureaus.",
         "Avoid late or missed payments."),

    # =========================
    # 🔴 CAR RENTAL & VEHICLE LEASE (311–345)
    # =========================

    Rule("DAMAGE_LIABILITY_RENTAL", "vehicle_rental", "high",
         ["responsible for all damage", "vehicle damage liability"],
         "Renter is liable for vehicle damage.",
         "Document vehicle condition before use."),

    Rule("INSURANCE_WAIVER_LIMITS", "vehicle_rental", "high",
         ["collision damage waiver", "cdw exclusions"],
         "Insurance waivers may have exclusions.",
         "Review what is not covered."),

    Rule("LATE_RETURN_FEES", "vehicle_rental", "medium",
         ["late return fee"],
         "Fees apply if vehicle is returned late.",
         "Plan return timing carefully."),

    Rule("MILEAGE_LIMITS", "vehicle_rental", "medium",
         ["mileage limit", "excess mileage"],
         "Charges apply for excess mileage.",
         "Estimate mileage needs upfront."),

    Rule("FUEL_CHARGES", "vehicle_rental", "medium",
         ["fuel service charge"],
         "Extra fees if fuel tank not refilled.",
         "Refuel before return."),

    Rule("TOWING_CHARGES", "vehicle_rental", "high",
         ["towing charge"],
         "Renter pays towing and recovery costs.",
         "Avoid prohibited driving areas."),

    Rule("TRAFFIC_VIOLATIONS", "vehicle_rental", "high",
         ["traffic violation", "parking fines"],
         "Renter responsible for violations.",
         "Follow traffic laws strictly."),

    Rule("VEHICLE_TRACKING", "vehicle_rental", "medium",
         ["gps tracking", "vehicle monitoring"],
         "Vehicle may be tracked.",
         "Understand privacy implications."),

    Rule("EARLY_RETURN_NO_REFUND", "vehicle_rental", "medium",
         ["no refund for early return"],
         "Returning early does not reduce cost.",
         "Confirm refund policy."),

    Rule("AUTHORIZED_DRIVERS", "vehicle_rental", "medium",
         ["authorized drivers only"],
         "Only approved drivers may operate vehicle.",
         "Add all drivers in advance."),

    # =========================
    # 🔴 ONLINE SUBSCRIPTIONS & DIGITAL SERVICES (346–380)
    # =========================

    Rule("AUTO_RENEW_SUBSCRIPTION", "digital_services", "high",
         ["subscription automatically renews"],
         "Subscription renews unless cancelled.",
         "Set cancellation reminders."),

    Rule("CANCELLATION_DIFFICULTY", "digital_services", "high",
         ["contact customer support to cancel"],
         "Cancellation process may be difficult.",
         "Document cancellation attempts."),

    Rule("PRICE_INCREASE_NOTICE", "digital_services", "medium",
         ["price increase notice"],
         "Prices may increase with notice.",
         "Review affordability regularly."),

    Rule("FEATURE_REMOVAL", "digital_services", "medium",
         ["remove features", "discontinue features"],
         "Features may be removed.",
         "Confirm core functionality protection."),

    Rule("ACCOUNT_SUSPENSION_DIGITAL", "digital_services", "high",
         ["suspend account", "disable access"],
         "Account access may be suspended.",
         "Understand suspension triggers."),

    Rule("DATA_LOSS", "digital_services", "high",
         ["not responsible for data loss"],
         "Provider disclaims responsibility for data loss.",
         "Maintain backups."),

    Rule("CONTENT_LICENSE_DIGITAL", "digital_services", "medium",
         ["license to use your content"],
         "Service may use uploaded content.",
         "Limit scope of content license."),

    Rule("ADS_INJECTION", "digital_services", "low",
         ["display advertisements"],
         "Service may show ads.",
         "Expect advertising content."),

    Rule("SERVICE_TERMINATION_NOTICE", "digital_services", "medium",
         ["terminate service with notice"],
         "Service may be discontinued.",
         "Export data before termination."),

    Rule("BETA_FEATURES", "digital_services", "low",
         ["beta features"],
         "Beta features may be unstable.",
         "Use cautiously."),

    # =========================
    # 🔴 GOVERNMENT FORMS & PUBLIC PROGRAMS (381–420)
    # =========================

    Rule("FALSE_STATEMENT_PENALTY", "government_forms", "high",
         ["false statement", "penalty of perjury"],
         "False information may lead to penalties.",
         "Ensure accuracy of all statements."),

    Rule("BENEFIT_REPAYMENT", "government_forms", "high",
         ["repay benefits", "overpayment recovery"],
         "Government may recover overpaid benefits.",
         "Report changes promptly."),

    Rule("AUDIT_GOVERNMENT", "government_forms", "medium",
         ["subject to audit"],
         "Application may be audited.",
         "Keep documentation."),

    Rule("ELIGIBILITY_REQUIREMENTS", "government_forms", "medium",
         ["eligibility requirements"],
         "Strict eligibility criteria apply.",
         "Confirm eligibility before applying."),

    Rule("DATA_SHARING_GOV", "government_forms", "high",
         ["share information with agencies"],
         "Information may be shared across agencies.",
         "Understand privacy implications."),

    Rule("CRIMINAL_LIABILITY", "government_forms", "high",
         ["criminal liability"],
         "Violations may result in criminal charges.",
         "Seek legal advice if unsure."),

    Rule("PROGRAM_TERMINATION", "government_forms", "medium",
         ["program termination"],
         "Program may end unexpectedly.",
         "Plan contingencies."),

    Rule("RECORD_KEEPING", "government_forms", "medium",
         ["retain records"],
         "Must retain records for specified period.",
         "Store documents securely."),

    Rule("REPORTING_OBLIGATIONS", "government_forms", "medium",
         ["report changes", "ongoing reporting"],
         "Ongoing reporting required.",
         "Track deadlines."),

    Rule("PENALTY_INTEREST", "government_forms", "high",
         ["penalty interest"],
         "Interest accrues on unpaid amounts.",
         "Pay amounts promptly."),

    # =========================
    # 🔴 COURT / LEGAL DOCUMENTS (421–460)
    # =========================

    Rule("DEFAULT_JUDGMENT", "court_documents", "high",
         ["default judgment"],
         "Failure to respond may result in default judgment.",
         "Respond within deadlines."),

    Rule("WAIVER_OF_RIGHTS", "court_documents", "high",
         ["waive rights"],
         "You waive certain legal rights.",
         "Understand rights being waived."),

    Rule("STATUTE_OF_LIMITATIONS", "court_documents", "medium",
         ["statute of limitations"],
         "Time limit applies to claims.",
         "Track limitation periods."),

    Rule("MANDATORY_APPEARANCE", "court_documents", "high",
         ["must appear", "mandatory appearance"],
         "Failure to appear may have consequences.",
         "Attend all required hearings."),

    Rule("FILING_FEES", "court_documents", "medium",
         ["filing fee"],
         "Fees required for filings.",
         "Budget for legal costs."),

    Rule("SERVICE_OF_PROCESS", "court_documents", "medium",
         ["service of process"],
         "Legal documents must be served properly.",
         "Confirm service compliance."),

    Rule("CONFIDENTIAL_FILINGS", "court_documents", "low",
         ["confidential filing"],
         "Some filings may be confidential.",
         "Follow court rules."),

    Rule("APPEAL_RIGHTS", "court_documents", "medium",
         ["right to appeal"],
         "Appeal rights may be limited.",
         "Confirm appeal deadlines."),

    Rule("SANCTIONS", "court_documents", "high",
         ["court sanctions"],
         "Violations may lead to sanctions.",
         "Comply with court orders."),


Rule("SETTLEMENT_TERMS", "court_documents", "medium",
     ["settlement agreement"],
     "Settlement terms are binding.",
     "Review obligations carefully."),

# =========================
# 🔴 SAAS / API & TECH TERMS (461–520)
# =========================

Rule("API_RATE_LIMITS", "saas_api", "medium",
     ["rate limit", "api throttling", "request limits"],
     "API usage is restricted by rate limits.",
     "Confirm limits align with expected usage."),

Rule("API_TERMINATION", "saas_api", "high",
     ["terminate api access", "revoke api key"],
     "API access may be revoked unilaterally.",
     "Ensure notice and remediation rights."),

Rule("SERVICE_LEVEL_EXCLUSIONS", "saas_api", "medium",
     ["sla exclusions", "no uptime guarantee"],
     "Service level guarantees may exclude many failures.",
     "Review SLA exclusions carefully."),

Rule("LOG_RETENTION_LIMITS", "saas_api", "medium",
     ["log retention", "logs retained for"],
     "Operational logs are retained for limited time.",
     "Export logs regularly if required."),

Rule("DATA_TRAINING_USAGE", "ai_data", "high",
     ["train models", "machine learning training"],
     "Your data may be used to train AI models.",
     "Opt out or restrict training rights."),

Rule("MODEL_OUTPUT_OWNERSHIP", "ai_data", "medium",
     ["ownership of outputs", "model outputs"],
     "Ownership of AI-generated outputs may be unclear.",
     "Clarify IP ownership of outputs."),

# =========================
# 🔴 INTELLECTUAL PROPERTY & LICENSING (521–580)
# =========================

Rule("LICENSE_SCOPE_BROAD", "intellectual_property", "high",
     ["perpetual license", "worldwide license"],
     "License grant is extremely broad.",
     "Limit duration, territory, and purpose."),

Rule("IRREVOCABLE_LICENSE", "intellectual_property", "high",
     ["irrevocable license"],
     "License cannot be revoked once granted.",
     "Avoid irrevocable grants where possible."),

Rule("DERIVATIVE_WORKS", "intellectual_property", "medium",
     ["derivative works"],
     "Other party may create derivatives of your IP.",
     "Restrict derivative rights."),

Rule("OPEN_SOURCE_CONTAMINATION", "intellectual_property", "high",
     ["open source", "copyleft"],
     "Open-source terms may impose disclosure obligations.",
     "Review OSS licenses carefully."),

Rule("PATENT_LICENSE", "intellectual_property", "medium",
     ["patent license"],
     "Patent rights are licensed or restricted.",
     "Consult IP counsel if patents involved."),

# =========================
# 🔴 E-COMMERCE & MARKETPLACE (581–640)
# =========================

Rule("SELLER_SUSPENSION", "ecommerce", "high",
     ["suspend seller account"],
     "Marketplace can suspend seller accounts.",
     "Understand appeal and reinstatement process."),

Rule("FUNDS_WITHHOLDING", "ecommerce", "high",
     ["withhold funds", "reserve balance"],
     "Marketplace may hold your funds.",
     "Confirm release conditions."),

Rule("CHARGEBACK_LIABILITY", "ecommerce", "high",
     ["chargeback", "dispute transaction"],
     "Seller bears chargeback liability.",
     "Implement fraud prevention."),

Rule("RETURN_FRAUD", "ecommerce", "medium",
     ["return abuse"],
     "Risk of fraudulent returns.",
     "Clarify seller protections."),

# =========================
# 🔴 INVESTMENTS & FINANCIAL PRODUCTS (641–700)
# =========================

Rule("NO_INVESTMENT_ADVICE", "investments", "high",
     ["not investment advice"],
     "Provider disclaims fiduciary responsibility.",
     "Do independent due diligence."),

Rule("MARKET_RISK_DISCLOSURE", "investments", "high",
     ["market risk", "loss of principal"],
     "Investments carry risk of loss.",
     "Assess risk tolerance."),

Rule("LOCKUP_PERIOD", "investments", "medium",
     ["lock-up period"],
     "Funds cannot be withdrawn for a period.",
     "Confirm liquidity needs."),

Rule("LIQUIDATION_PREFERENCE", "investments", "high",
     ["liquidation preference"],
     "Certain investors get paid first.",
     "Understand payout hierarchy."),

# =========================
# 🔴 BANKRUPTCY & INSOLVENCY (701–750)
# =========================

Rule("INSOLVENCY_TERMINATION", "bankruptcy", "high",
     ["terminate upon insolvency"],
     "Contract may terminate if a party becomes insolvent.",
     "Plan contingency arrangements."),

Rule("CREDITOR_PRIORITY", "bankruptcy", "medium",
     ["priority of creditors"],
     "Certain creditors have payment priority.",
     "Assess recovery risk."),

# =========================
# 🔴 SAFETY, HEALTH & ENVIRONMENT (751–800)
# =========================

Rule("SAFETY_COMPLIANCE", "safety_environment", "high",
     ["safety regulations", "osha"],
     "Strict safety compliance obligations.",
     "Ensure procedures and training."),

Rule("ENVIRONMENTAL_LIABILITY", "safety_environment", "high",
     ["environmental liability", "hazardous materials"],
     "Liability for environmental damage.",
     "Confirm insurance and controls."),

Rule("HEALTH_DATA", "healthcare", "high",
     ["hipaa", "protected health information"],
     "Handling of sensitive health data.",
     "Ensure HIPAA/GDPR compliance."),

# =========================
# 🔴 HEALTHCARE & INSURANCE (801–830)
# =========================

Rule("PRE_EXISTING_CONDITIONS", "healthcare", "high",
     ["pre-existing condition", "coverage exclusion"],
     "Insurance may exclude pre-existing conditions.",
     "Clarify what is covered and excluded."),

Rule("CLAIM_DENIAL", "healthcare", "high",
     ["deny claim", "claim denial"],
     "Insurer can deny claims under many circumstances.",
     "Understand appeal rights and documentation required."),

Rule("NETWORK_LIMITATIONS", "healthcare", "medium",
     ["in-network only", "network provider"],
     "Coverage may be limited to network providers.",
     "Check provider lists and out-of-network costs."),

Rule("PRIOR_AUTHORIZATION", "healthcare", "medium",
     ["prior authorization required", "pre-approval"],
     "Certain treatments require prior approval.",
     "Understand approval process and timelines."),

Rule("LIFETIME_MAXIMUMS", "healthcare", "medium",
     ["lifetime maximum", "benefit cap"],
     "Benefits may have lifetime caps.",
     "Confirm policy maximums and alternatives."),

# =========================
# 🔴 EDUCATION & STUDENT AGREEMENTS (831–860)
# =========================

Rule("ACADEMIC_INTEGRITY", "education", "high",
     ["academic integrity", "plagiarism policy"],
     "Strict rules on academic honesty and plagiarism.",
     "Understand penalties for violations."),

Rule("TUITION_INCREASE", "education", "medium",
     ["tuition increase", "fee adjustment"],
     "Tuition or fees may increase during enrollment.",
     "Budget for possible increases."),

Rule("DISCIPLINARY_ACTION_EDU", "education", "medium",
     ["disciplinary action", "student code of conduct"],
     "Violations may result in disciplinary action.",
     "Review conduct rules and appeal process."),

Rule("ENROLLMENT_TERMINATION", "education", "high",
     ["terminate enrollment", "expulsion"],
     "School may terminate enrollment for violations.",
     "Clarify grounds and notice requirements."),

Rule("INTELLECTUAL_PROPERTY_STUDENT", "education", "medium",
     ["student work ownership", "assign student IP"],
     "School may claim ownership of student work.",
     "Negotiate IP rights if needed."),

# =========================
# 🔴 TRAVEL & HOSPITALITY (861–890)
# =========================

Rule("CANCELLATION_FEES_TRAVEL", "travel_hospitality", "high",
     ["cancellation fee", "non-refundable booking"],
     "Bookings may be non-refundable or have cancellation fees.",
     "Check flexibility before booking."),

Rule("OVERBOOKING", "travel_hospitality", "medium",
     ["overbooking policy", "subject to availability"],
     "Provider may overbook and deny service.",
     "Confirm compensation and alternatives."),

Rule("BAGGAGE_LIMITS", "travel_hospitality", "medium",
     ["baggage allowance", "excess baggage fee"],
     "Strict baggage limits and fees may apply.",
     "Review limits before travel."),

Rule("DAMAGE_LIABILITY_HOTEL", "travel_hospitality", "medium",
     ["guest liable for damage", "room damage charge"],
     "Guests may be liable for property damage.",
     "Inspect room and report issues immediately."),

Rule("CHECKIN_CHECKOUT_TIMES", "travel_hospitality", "low",
     ["check-in time", "check-out time"],
     "Strict check-in and check-out times.",
     "Plan travel accordingly."),

# =========================
# 🔴 AI / DATA TRAINING USAGE (891–910)
# =========================

Rule("DATA_SHARING_FOR_TRAINING", "ai_data", "high",
     ["share data for training", "data provided for model improvement"],
     "Your data may be shared for third-party AI training.",
     "Request restrictions or opt-out options."),

Rule("MODEL_BIAS_DISCLOSURE", "ai_data", "medium",
     ["model bias", "algorithmic bias"],
     "AI models may have undisclosed biases.",
     "Request transparency and review processes."),

Rule("OUTPUT_REUSE", "ai_data", "medium",
     ["reuse of outputs", "output redistribution"],
     "AI-generated outputs may be reused or resold.",
     "Clarify rights to outputs and reuse."),

Rule("PROMPT_LOGGING", "ai_data", "medium",
     ["prompt logging", "record user input"],
     "User prompts may be logged for analysis.",
     "Request prompt deletion and privacy controls."),

# =========================
# 🔴 ENVIRONMENTAL & SAFETY (911–930)
# =========================

Rule("CARBON_OFFSETS", "safety_environment", "low",
     ["carbon offset", "environmental credits"],
     "Company may use offsets for compliance.",
     "Verify legitimacy and effectiveness of offsets."),

Rule("EMISSIONS_LIMITS", "safety_environment", "medium",
     ["emissions limits", "pollution cap"],
     "Strict emissions or pollution limits may apply.",
     "Confirm compliance and reporting obligations."),

Rule("RECALL_OBLIGATION", "safety_environment", "high",
     ["recall obligation", "product recall"],
     "Obligation to recall unsafe products.",
     "Establish recall procedures and insurance."),

Rule("SAFETY_AUDITS", "safety_environment", "medium",
     ["safety audit", "environmental audit"],
     "Subject to regular safety/environmental audits.",
     "Prepare documentation and corrective plans."),

]


def analyze_clause_with_rules(clause_text: str) -> dict:
    """
    Deterministically analyze a single clause against all rules.
    """
    text = clause_text.lower()
    matched = []

    for rule in RULES:
        for pattern in rule.patterns:
            if pattern.lower() in text:
                matched.append(rule)
                break

    if not matched:
        return {
            "category": "General",
            "risk_level": "Low",
            "summary": "Standard contractual language with no obvious risk.",
            "suggestion": None,
            "matched_rules": []
        }

    severity_rank = {"high": 3, "medium": 2, "low": 1}
    highest = max(matched, key=lambda r: severity_rank[r.severity])

    return {
        "category": highest.category,
        "risk_level": highest.severity.capitalize(),
        "summary": highest.summary,
        "suggestion": highest.recommendation,
        "matched_rules": [r.id for r in matched]
    }


def analyze_document_with_rules(full_text: str) -> dict:
    """
    Extract high-signal, human-readable insights from the entire document.
    """
    text = full_text.lower()

    buckets = defaultdict(list)

    for rule in RULES:
        for pattern in rule.patterns:
            if pattern.lower() in text:
                buckets[rule.category].append(rule)
                break

    def unique_summaries(rules):
        seen = set()
        out = []
        for r in rules:
            if r.summary not in seen:
                out.append(r.summary)
                seen.add(r.summary)
        return out

    high_risk = [
        r.summary for r in buckets.get("critical_alert", [])
    ]

    review_items = [
        r.summary for r in buckets.get("review_required", [])
    ]

    deadlines = []
    for match in re.findall(r"\b\d+\s+(days|day|months|month|years|year)\b", text):
        deadlines.append(match)

    obligations = unique_summaries(
        buckets.get("critical_alert", []) +
        buckets.get("review_required", [])
    )

    plain_summary = (
        "This document contains multiple obligations and risk clauses. "
        "Pay close attention to termination rights, payment terms, liability, "
        "and any clauses allowing unilateral changes."
        if high_risk else
        "This document appears mostly standard but should still be reviewed carefully."
    )

    return {
        "high_risk_flags": high_risk,
        "review_items": review_items,
        "key_obligations": obligations,
        "deadlines_detected": deadlines,
        "plain_english_summary": plain_summary
    }