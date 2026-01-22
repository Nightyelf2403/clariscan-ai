

from dataclasses import dataclass
from typing import List


@dataclass
class Rule:
    id: str
    title: str
    description: str
    risk_level: str  # "High" | "Medium" | "Low"
    keywords: List[str]
    suggestion: str
    min_hits: int = 1          # minimum keyword matches required to trigger
    expected_hits: int = 0     # optional override for confidence calculation


# ============================================================
# CORE CONTRACT RISK RULES (FOUNDATIONAL SET – 5 RULES ONLY)
# ============================================================

RULES: List[Rule] = [

    Rule(
        id="UNILATERAL_TERMINATION",
        title="One-Sided Termination Rights",
        description=(
            "One party can terminate the agreement with minimal notice while the "
            "other party faces stricter or no termination rights."
        ),
        risk_level="High",
        keywords=[
            "terminate at any time",
            "sole discretion",
            "without cause",
            "only terminate",
            "may terminate this agreement"
        ],
        suggestion=(
            "Seek mutual termination rights or equal notice periods for both parties."
        ),
    ),

    Rule(
        id="CURE_PERIOD_IMBALANCE",
        title="Unbalanced Cure Period",
        description=(
            "One party is granted a long cure period to fix breaches while the other "
            "party has limited or no opportunity to cure."
        ),
        risk_level="Medium",
        keywords=[
            "cure period",
            "material breach",
            "days to cure",
            "written notice and opportunity to cure"
        ],
        suggestion=(
            "Ensure both parties are granted a reasonable and equal cure period."
        ),
        min_hits=2
    ),

    Rule(
        id="LIMITATION_OF_LIABILITY",
        title="Liability Cap or Liability Exclusion",
        description=(
            "The agreement limits or excludes liability, which may prevent recovery "
            "of meaningful damages."
        ),
        risk_level="High",
        keywords=[
            "limitation of liability",
            "shall not be liable",
            "indirect damages",
            "consequential damages",
            "liability shall not exceed"
        ],
        suggestion=(
            "Review liability caps carefully and negotiate carve-outs for gross negligence or willful misconduct."
        ),
    ),

    Rule(
        id="INDEMNIFICATION_OBLIGATION",
        title="Broad Indemnification Obligation",
        description=(
            "One party agrees to indemnify the other for a wide range of claims, "
            "possibly including third-party actions."
        ),
        risk_level="High",
        keywords=[
            "indemnify",
            "hold harmless",
            "defend against",
            "claims arising from"
        ],
        suggestion=(
            "Limit indemnification scope and exclude indirect or unrelated claims."
        ),
    ),

    Rule(
        id="INTELLECTUAL_PROPERTY_OWNERSHIP",
        title="Unfavorable Intellectual Property Ownership",
        description=(
            "All intellectual property is retained by one party, leaving the other "
            "with limited or revocable usage rights."
        ),
        risk_level="Medium",
        keywords=[
            "intellectual property",
            "sole property",
            "exclusive ownership",
            "revocable license",
            "non-transferable license"
        ],
        suggestion=(
            "Clarify IP ownership and ensure sufficient rights for continued use."
        ),
        min_hits=2
    ),

    Rule(
        id="PAYMENT_PENALTIES_INTEREST",
        title="Aggressive Late Payment Penalties",
        description=(
            "The contract imposes high interest rates or severe penalties for late payments."
        ),
        risk_level="Medium",
        keywords=[
     "interest at",
     "interest per month",
     "interest per annum",
     "late payment interest",
     "finance charge of"
],
        suggestion=(
            "Negotiate lower interest rates and reasonable grace periods for late payments."
        ),
        min_hits=2
    ),

    Rule(
        id="AUTO_RENEWAL",
        title="Automatic Renewal Without Clear Opt-Out",
        description=(
            "The agreement renews automatically unless terminated within a narrow notice window."
        ),
        risk_level="Medium",
        keywords=[
            "automatically renew",
            "auto-renewal",
            "renew for successive terms",
            "unless terminated"
        ],
        suggestion=(
            "Add clear renewal reminders and broader termination windows."
        ),
        min_hits=2
    ),

    Rule(
        id="GOVERNING_LAW_BIAS",
        title="Unfavorable Governing Law or Venue",
        description=(
            "The governing law or jurisdiction favors one party and may increase litigation burden."
        ),
        risk_level="Medium",
        keywords=[
            "governing law",
            "laws of the state",
            "exclusive jurisdiction",
            "venue shall be"
        ],
        suggestion=(
            "Seek neutral governing law or a mutually acceptable jurisdiction."
        ),
        min_hits=2
    ),

    Rule(
        id="ASSIGNMENT_WITHOUT_CONSENT",
        title="Assignment Without Consent",
        description=(
            "One party may assign the agreement without the other party’s consent."
        ),
        risk_level="High",
        keywords=[
            "assign this agreement",
            "without consent",
            "freely assignable",
            "assignment permitted"
        ],
        suggestion=(
            "Require prior written consent for assignment, except in limited cases."
        ),
    ),

    Rule(
        id="AUDIT_RIGHTS",
        title="Broad Audit or Inspection Rights",
        description=(
            "The contract allows one party to audit or inspect the other with minimal limits."
        ),
        risk_level="Low",
        keywords=[
            "audit",
            "inspection",
            "examine records",
            "access books"
        ],
        suggestion=(
            "Limit audit frequency, scope, and require reasonable notice."
        ),
    ),

    Rule(
        id="CONFIDENTIALITY_SURVIVAL",
        title="Confidentiality Obligations That Survive Indefinitely",
        description=(
            "Confidentiality obligations survive termination indefinitely or for an unreasonably long period."
        ),
        risk_level="Medium",
        keywords=[
            "confidentiality shall survive",
            "survive termination",
            "perpetual confidentiality",
            "indefinitely"
        ],
        suggestion=(
            "Limit confidentiality survival periods to a reasonable timeframe, such as 2–5 years."
        ),
        min_hits=2
    ),

    Rule(
        id="DATA_USAGE_RIGHTS",
        title="Broad Data Usage or Data Sale Rights",
        description=(
            "The agreement allows one party to use, sell, or share data beyond what is necessary for the service."
        ),
        risk_level="High",
        keywords=[
            "use data",
            "share data",
            "sell data",
            "data analytics",
            "data aggregation"
        ],
        suggestion=(
            "Restrict data usage strictly to service delivery and prohibit resale or secondary use."
        ),
    ),

    Rule(
        id="UNILATERAL_AMENDMENTS",
        title="Unilateral Contract Modification Rights",
        description=(
            "One party can modify the agreement unilaterally without explicit consent."
        ),
        risk_level="High",
        keywords=[
            "may modify this agreement",
            "reserve the right to change",
            "amend at any time",
            "update terms without notice"
        ],
        suggestion=(
            "Require mutual written consent for any material contract changes."
        ),
    ),

    Rule(
        id="ARBITRATION_CLASS_WAIVER",
        title="Mandatory Arbitration or Class Action Waiver",
        description=(
            "The contract forces arbitration or waives class action rights."
        ),
        risk_level="High",
        keywords=[
            "binding arbitration",
            "class action waiver",
            "waive right to jury",
            "arbitration shall be"
        ],
        suggestion=(
            "Carefully review dispute resolution clauses and understand rights being waived."
        ),
    ),

    Rule(
        id="FORCE_MAJEURE_OVERBROAD",
        title="Overly Broad Force Majeure Clause",
        description=(
            "Force majeure is defined too broadly, excusing performance for avoidable events."
        ),
        risk_level="Low",
        keywords=[
            "force majeure",
            "events beyond reasonable control",
            "acts of god",
            "government action"
        ],
        suggestion=(
            "Narrow force majeure definitions and exclude foreseeable or controllable events."
        ),
    ),

    Rule(
        id="EMPLOYMENT_AT_WILL_OVERRIDE",
        title="At-Will Employment Override or Hidden Termination",
        description=(
            "The agreement weakens or overrides statutory employment protections, "
            "allowing termination with minimal safeguards."
        ),
        risk_level="High",
        keywords=[
            "at-will employment",
            "terminate employment at any time",
            "without notice or cause",
            "sole discretion of employer"
        ],
        suggestion=(
            "Confirm that statutory employment rights are not waived or restricted."
        ),
    ),

    Rule(
        id="NON_COMPETE_BREADTH",
        title="Overly Broad Non-Compete Restriction",
        description=(
            "Non-compete obligations are excessively broad in scope, geography, or duration."
        ),
        risk_level="High",
        keywords=[
            "non-compete",
            "restrict competition",
            "any competing business",
            "worldwide",
            "for any reason"
        ],
        suggestion=(
            "Limit non-compete clauses by geography, duration, and scope of activities."
        ),
    ),

    Rule(
        id="SURVEILLANCE_MONITORING",
        title="Employee or User Surveillance Rights",
        description=(
            "The agreement permits monitoring, tracking, or surveillance of users or employees."
        ),
        risk_level="Medium",
        keywords=[
    "monitor user activity",
    "record communications",
    "track employee behavior",
    "keystroke logging",
    "screen monitoring"
],
        suggestion=(
            "Ensure monitoring is transparent, limited, and compliant with privacy laws."
        ),
        min_hits=2
    ),

    Rule(
        id="FEE_INCREASE_UNILATERAL",
        title="Unilateral Fee or Price Increases",
        description=(
            "One party may increase fees or pricing without meaningful consent."
        ),
        risk_level="Medium",
        keywords=[
            "increase fees",
            "change pricing",
            "adjust charges",
            "fees may be modified"
        ],
        suggestion=(
            "Require advance notice and termination rights for fee increases."
        ),
        min_hits=2
    ),

    Rule(
        id="RIGHTS_WAIVER_GENERAL",
        title="General Waiver of Legal Rights",
        description=(
            "The contract broadly waives legal rights, remedies, or statutory protections."
        ),
        risk_level="High",
        keywords=[
            "waive all rights",
            "release of claims",
            "irrevocably waive",
            "no legal recourse"
        ],
        suggestion=(
            "Avoid broad waivers and preserve statutory and consumer protection rights."
        ),
    ),

    Rule(
        id="REFUND_RESTRICTIONS",
        title="No Refunds or Strict Refund Limitations",
        description=(
            "The agreement restricts refunds entirely or allows refunds only under very narrow conditions."
        ),
        risk_level="Medium",
        keywords=[
            "no refunds",
            "non-refundable",
            "all sales are final",
            "refunds will not be issued"
        ],
        suggestion=(
            "Ensure reasonable refund rights or clearly defined refund conditions."
        ),
        min_hits=2
    ),

    Rule(
        id="SUBSCRIPTION_CANCELLATION_BARRIERS",
        title="Difficult Subscription Cancellation",
        description=(
            "The contract makes cancellation intentionally difficult or burdensome."
        ),
        risk_level="Medium",
        keywords=[
            "cancel only by",
            "written cancellation required",
            "phone cancellation",
            "account termination process"
        ],
        suggestion=(
            "Require simple and accessible cancellation methods."
        ),
        min_hits=2
    ),

    Rule(
        id="JURISDICTION_EXCLUSIVE_FOREIGN",
        title="Exclusive Foreign Jurisdiction",
        description=(
            "Disputes must be resolved in a foreign or distant jurisdiction."
        ),
        risk_level="High",
        keywords=[
            "exclusive jurisdiction",
            "courts of",
            "venue shall lie exclusively",
            "foreign courts"
        ],
        suggestion=(
            "Negotiate jurisdiction closer to your residence or business operations."
        ),
    ),

    Rule(
        id="DATA_RETENTION_INDEFINITE",
        title="Indefinite Data Retention",
        description=(
            "The agreement allows indefinite retention of personal or business data."
        ),
        risk_level="High",
        keywords=[
            "retain data indefinitely",
            "data retention period",
            "retain information",
            "store data permanently"
        ],
        suggestion=(
            "Limit data retention to legally required or operationally necessary periods."
        ),
    ),

    Rule(
        id="SERVICE_SUSPENSION_DISCRETION",
        title="Service Suspension at Sole Discretion",
        description=(
            "One party may suspend services without clear standards or notice."
        ),
        risk_level="High",
        keywords=[
    "suspend services at its discretion",
    "may disable access without notice",
    "immediately suspend services",
    "sole discretion to suspend"
],
        suggestion=(
            "Require notice, justification, and opportunity to cure before suspension."
        ),
    ),

    Rule(
        id="TERMINATION_NOTICE_SHORT",
        title="Unreasonably Short Termination Notice",
        description=(
            "The agreement allows termination with an unreasonably short notice period, "
            "creating operational or financial risk."
        ),
        risk_level="High",
        keywords=[
            "immediate termination",
            "terminate immediately",
            "without prior notice",
            "upon notice"
        ],
        suggestion=(
            "Negotiate a longer termination notice period to allow transition planning."
        ),
    ),

    Rule(
        id="ONE_SIDED_CONFIDENTIALITY",
        title="One-Sided Confidentiality Obligations",
        description=(
            "Confidentiality obligations apply primarily or exclusively to one party."
        ),
        risk_level="Medium",
        keywords=[
            "recipient shall keep confidential",
            "disclosing party",
            "obligations of recipient only"
        ],
        suggestion=(
            "Ensure confidentiality obligations apply equally to both parties."
        ),
        min_hits=2
    ),

    Rule(
        id="NO_SERVICE_LEVEL_COMMITMENT",
        title="No Service Level or Performance Commitment",
        description=(
            "The agreement lacks service levels, uptime commitments, or performance guarantees."
        ),
        risk_level="Medium",
        keywords=[
            "no service level",
            "as is",
            "no warranty",
            "best efforts only"
        ],
        suggestion=(
            "Add measurable service levels, uptime guarantees, or remedies for failure."
        ),
        min_hits=2
    ),

    Rule(
        id="WARRANTY_DISCLAIMER",
        title="Broad Warranty Disclaimer",
        description=(
            "All warranties are disclaimed, limiting remedies for defective performance."
        ),
        risk_level="High",
        keywords=[
            "disclaims all warranties",
            "as is basis",
            "no warranties express or implied",
            "merchantability"
        ],
        suggestion=(
            "Seek limited warranties covering performance, compliance, and non-infringement."
        ),
    ),

    Rule(
        id="COMPLIANCE_SHIFT",
        title="Regulatory Compliance Shifted to User",
        description=(
            "The agreement shifts all regulatory or legal compliance responsibility to one party."
        ),
        risk_level="High",
        keywords=[
            "user responsible for compliance",
            "sole responsibility",
            "applicable laws compliance",
            "at its own expense"
        ],
        suggestion=(
            "Clarify shared compliance responsibilities and provider obligations."
        ),
    ),

    Rule(
        id="INSURANCE_REQUIREMENTS",
        title="Missing or Inadequate Insurance Requirements",
        description=(
            "The contract lacks clear insurance requirements or minimum coverage levels."
        ),
        risk_level="Low",
        keywords=[
            "insurance",
            "coverage",
            "policy limits",
            "certificate of insurance"
        ],
        suggestion=(
            "Specify required insurance types and minimum coverage amounts."
        ),
    ),
    Rule(
        id="EXPENSE_REIMBURSEMENT_OPEN_ENDED",
        title="Open-Ended Expense Reimbursement",
        description=(
            "One party is required to reimburse expenses without caps, approvals, or clear definitions."
        ),
        risk_level="Medium",
        keywords=[
            "reimburse all expenses",
            "reasonable expenses incurred",
            "without limitation",
            "expense reimbursement"
        ],
        suggestion=(
            "Add expense caps, approval requirements, and clear definitions of reimbursable costs."
        ),
        min_hits=2
    ),

    Rule(
        id="SURVIVAL_CLAUSE_OVERBROAD",
        title="Overly Broad Survival Clause",
        description=(
            "Multiple obligations survive termination unnecessarily, extending liability indefinitely."
        ),
        risk_level="Medium",
        keywords=[
            "shall survive termination",
            "survive expiration",
            "continue in full force",
            "notwithstanding termination"
        ],
        suggestion=(
            "Limit survival clauses to essential provisions like confidentiality and payment."
        ),
        min_hits=2
    ),

    Rule(
        id="LIQUIDATED_DAMAGES_PENALTY",
        title="Punitive Liquidated Damages",
        description=(
            "The contract imposes liquidated damages that may function as penalties rather than estimates of loss."
        ),
        risk_level="High",
        keywords=[
            "liquidated damages",
            "penalty",
            "pre-estimated damages",
            "fixed damages amount"
        ],
        suggestion=(
            "Ensure liquidated damages are reasonable and proportionate to actual harm."
        ),
    ),

    Rule(
        id="THIRD_PARTY_BENEFICIARY",
        title="Unexpected Third-Party Beneficiaries",
        description=(
            "The agreement grants enforcement rights to third parties not directly involved in the contract."
        ),
        risk_level="Medium",
        keywords=[
            "third-party beneficiary",
            "enforce this agreement",
            "benefit of third parties",
            "successors and assigns"
        ],
        suggestion=(
            "Explicitly exclude unintended third-party beneficiaries."
        ),
        min_hits=2
    ),

    Rule(
        id="PUBLICITY_RIGHTS",
        title="Unrestricted Publicity or Marketing Rights",
        description=(
            "One party may use the other’s name, logo, or marks without consent."
        ),
        risk_level="Low",
        keywords=[
            "use name",
            "use logo",
            "publicity",
            "marketing materials",
            "press release"
        ],
        suggestion=(
            "Require prior written approval for any public or marketing use."
        ),
    ),

    Rule(
        id="UNILATERAL_OFFSET_RIGHTS",
        title="Unilateral Setoff or Offset Rights",
        description=(
            "One party may offset payments or amounts owed without mutual agreement or dispute resolution."
        ),
        risk_level="Medium",
        keywords=[
            "setoff",
            "offset amounts",
            "deduct from payments",
            "withhold payment"
        ],
        suggestion=(
            "Require mutual agreement or final determination before exercising setoff rights."
        ),
        min_hits=2
    ),

    Rule(
        id="CHANGE_OF_CONTROL_TERMINATION",
        title="Termination Upon Change of Control",
        description=(
            "The agreement allows termination solely due to a merger, acquisition, or ownership change."
        ),
        risk_level="Medium",
        keywords=[
            "change of control",
            "merger or acquisition",
            "ownership change",
            "control of the company"
        ],
        suggestion=(
            "Limit termination rights to material adverse impacts, not ownership changes alone."
        ),
        min_hits=2
    ),

    Rule(
        id="NO_ASSIGNMENT_TO_CUSTOMER",
        title="Customer Assignment Prohibited",
        description=(
            "One party is restricted from assigning the agreement, while the other party is not."
        ),
        risk_level="Low",
        keywords=[
            "may not assign",
            "assignment prohibited",
            "without prior written consent"
        ],
        suggestion=(
            "Ensure assignment restrictions apply equally or allow assignment to affiliates."
        ),
    ),

    Rule(
        id="EXPORT_CONTROL_RISK",
        title="Export Control and Sanctions Exposure",
        description=(
            "The agreement creates exposure to export control, sanctions, or trade compliance violations."
        ),
        risk_level="High",
        keywords=[
            "export control",
            "sanctions",
            "restricted countries",
            "trade compliance"
        ],
        suggestion=(
            "Clarify export responsibilities and ensure compliance obligations are shared."
        ),
    ),

    Rule(
        id="NO_ESCROW_SOURCE_CODE",
        title="No Source Code Escrow for Critical Software",
        description=(
            "The agreement lacks source code escrow protections for essential software services."
        ),
        risk_level="Medium",
        keywords=[
            "source code escrow",
            "no escrow",
            "software dependency",
            "business continuity"
        ],
        suggestion=(
            "Add source code escrow provisions for mission-critical software."
        ),
        min_hits=2
    ),
    Rule(
        id="DATA_BREACH_NOTIFICATION_DELAY",
        title="Delayed Data Breach Notification",
        description=(
            "The agreement allows excessive delay before notifying affected parties of a data breach."
        ),
        risk_level="High",
        keywords=[
            "data breach notification",
            "notify within",
            "without undue delay",
            "security incident notice"
        ],
        suggestion=(
            "Require prompt breach notification within a fixed and short timeframe (e.g., 48–72 hours)."
        ),
    ),
    Rule(
        id="BACKGROUND_CHECK_CONSENT",
        title="Broad Background Check Authorization",
        description=(
            "The agreement authorizes extensive background, credit, or identity checks without limits."
        ),
        risk_level="Medium",
        keywords=[
            "background check",
            "credit check",
            "criminal history",
            "identity verification"
        ],
        suggestion=(
            "Limit background checks to what is legally required and relevant to the role or service."
        ),
        min_hits=2
    ),
    Rule(
        id="POST_TERMINATION_FEES",
        title="Post-Termination Fees or Charges",
        description=(
            "Fees or payment obligations continue after termination without clear justification."
        ),
        risk_level="Medium",
        keywords=[
            "post-termination fees",
            "fees shall survive termination",
            "charges after termination",
            "continuing payment obligation"
        ],
        suggestion=(
            "Ensure post-termination fees are limited to earned or unavoidable costs only."
        ),
        min_hits=2
    ),
    Rule(
        id="DATA_LOCATION_RESTRICTION",
        title="Unrestricted Data Storage Location",
        description=(
            "The agreement permits data storage or processing in any country without restriction."
        ),
        risk_level="Medium",
        keywords=[
            "data may be stored",
            "processed in any country",
            "global data centers",
            "international transfer"
        ],
        suggestion=(
            "Restrict data storage to jurisdictions with adequate data protection laws."
        ),
        min_hits=2
    ),
    Rule(
        id="RIGHT_TO_INJUNCTIVE_RELIEF_ONE_SIDED",
        title="One-Sided Injunctive Relief Rights",
        description=(
            "Only one party may seek injunctive or equitable relief in court."
        ),
        risk_level="High",
        keywords=[
            "injunctive relief",
            "equitable relief",
            "without posting bond",
            "sole right to seek"
        ],
        suggestion=(
            "Ensure injunctive relief rights apply equally to both parties."
        ),
    ),

    Rule(
        id="DATA_DELETION_AFTER_TERMINATION",
        title="No Data Deletion After Termination",
        description=(
            "The agreement does not clearly require deletion or return of data after termination."
        ),
        risk_level="High",
        keywords=[
            "retain data after termination",
            "data may be retained",
            "no obligation to delete",
            "data retention after termination"
        ],
        suggestion=(
            "Require clear data deletion or return obligations within a fixed timeframe after termination."
        ),
    ),

    Rule(
        id="UNLIMITED_SUBCONTRACTING",
        title="Unrestricted Subcontracting",
        description=(
            "One party may subcontract obligations without disclosure or consent."
        ),
        risk_level="Medium",
        keywords=[
            "subcontract",
            "third-party providers",
            "may engage subcontractors",
            "without prior consent"
        ],
        suggestion=(
            "Require notice and consent for subcontracting, especially where data or IP is involved."
        ),
        min_hits=2
    ),

    Rule(
        id="NO_NOTICE_POLICY_CHANGES",
        title="Policy Changes Without Notice",
        description=(
            "Policies or terms may be changed without advance notice to the user."
        ),
        risk_level="High",
        keywords=[
            "policies may change",
            "without notice",
            "subject to change at any time",
            "we may update policies"
        ],
        suggestion=(
            "Require advance notice and opt-out rights for material policy changes."
        ),
    ),

    Rule(
        id="EXCESSIVE_NOTICE_REQUIREMENTS",
        title="Excessive Notice Formalities",
        description=(
            "The agreement requires overly burdensome notice methods that may invalidate user actions."
        ),
        risk_level="Medium",
        keywords=[
            "notice shall be delivered",
            "certified mail only",
            "registered post",
            "hand delivered notice"
        ],
        suggestion=(
            "Allow modern notice methods such as email with confirmation."
        ),
        min_hits=2
    ),

    Rule(
        id="NO_CONSUMER_PROTECTION_REFERENCE",
        title="Missing Consumer Protection Acknowledgment",
        description=(
            "The agreement omits reference to mandatory consumer protection or statutory rights."
        ),
        risk_level="Low",
        keywords=[
            "to the fullest extent permitted",
            "waive statutory rights",
            "consumer protection",
            "mandatory law"
        ],
        suggestion=(
            "Explicitly preserve mandatory consumer or statutory rights."
        ),
    ),
    Rule(
        id="NO_TERMINATION_ASSISTANCE",
        title="No Transition or Termination Assistance",
        description=(
            "The agreement does not require assistance during transition or exit, "
            "creating operational risk after termination."
        ),
        risk_level="Medium",
        keywords=[
            "no transition assistance",
            "upon termination no obligation",
            "no support after termination",
            "as is upon termination"
        ],
        suggestion=(
            "Add reasonable transition or termination assistance obligations."
        ),
        min_hits=2
    ),

    Rule(
        id="RESTRICTION_ON_DISPUTE_PUBLICITY",
        title="Restriction on Discussing Disputes",
        description=(
            "The agreement restricts parties from publicly discussing disputes or outcomes."
        ),
        risk_level="Low",
        keywords=[
            "non-disparagement",
            "may not disclose dispute",
            "no public statements",
            "confidential dispute resolution"
        ],
        suggestion=(
            "Limit non-disparagement obligations to false or malicious statements only."
        ),
    ),

    Rule(
        id="UNDEFINED_MATERIAL_BREACH",
        title="Undefined Material Breach Standard",
        description=(
            "Material breach is referenced but not clearly defined, allowing subjective enforcement."
        ),
        risk_level="Medium",
        keywords=[
            "material breach",
            "in the event of breach",
            "breach of this agreement",
            "default under this agreement"
        ],
        suggestion=(
            "Define material breach clearly or include objective thresholds."
        ),
        min_hits=2
    ),

    Rule(
        id="NO_DATA_PORTABILITY",
        title="No Data Portability or Export Rights",
        description=(
            "The agreement does not guarantee access to or export of data upon request or termination."
        ),
        risk_level="High",
        keywords=[
            "no obligation to provide data",
            "data export",
            "portability",
            "access to data upon termination"
        ],
        suggestion=(
            "Require data export in a usable format during and after the agreement."
        ),
    ),

    Rule(
        id="SERVICE_DEPENDENCY_LOCK_IN",
        title="Service Dependency or Vendor Lock-In",
        description=(
            "The agreement creates dependency on proprietary systems without exit safeguards."
        ),
        risk_level="Medium",
        keywords=[
            "proprietary system",
            "exclusive platform",
            "no alternative provider",
            "dependency on service"
        ],
        suggestion=(
            "Add exit rights, data portability, or interoperability protections."
        ),
        min_hits=2
    ),

    Rule(
        id="THIRD_PARTY_FEE_COLLECTION",
        title="Mandatory Third-Party Fee or Payment Handling",
        description=(
            "Payments or fees are processed through third-party providers, "
            "which may introduce additional costs, delays, or disputes."
        ),
        risk_level="Medium",
        keywords=[
            "third-party payment",
            "payment processor",
            "processed by a third party",
            "collection agent",
            "payment intermediary"
        ],
        suggestion=(
            "Clarify responsibility for third-party fees and require transparency on all charges."
        ),
        min_hits=2
    ),

    Rule(
        id="NO_REFUND_ON_SERVICE_FAILURE",
        title="No Refunds Even if Service Fails",
        description=(
            "The agreement denies refunds even when services are unavailable, defective, or terminated early."
        ),
        risk_level="High",
        keywords=[
            "no refunds under any circumstances",
            "no refund even if",
            "service failure",
            "downtime",
            "non-refundable fees"
        ],
        suggestion=(
            "Ensure refunds or credits are available for service failures or non-performance."
        ),
    ),

    Rule(
        id="ONE_SIDED_EVIDENCE_STANDARD",
        title="One-Sided Evidence or Proof Standard",
        description=(
            "Only one party’s records or determinations are treated as conclusive evidence."
        ),
        risk_level="High",
        keywords=[
            "conclusive evidence",
            "final and binding determination",
            "sole evidence",
            "records shall be deemed correct"
        ],
        suggestion=(
            "Require neutral or mutually verifiable evidence standards."
        ),
    ),

    Rule(
        id="UNDEFINED_REASONABLE_STANDARD",
        title="Undefined 'Reasonable' Standards",
        description=(
            "The contract repeatedly uses vague terms like 'reasonable' without definition, "
            "allowing subjective enforcement."
        ),
        risk_level="Medium",
        keywords=[
            "reasonable efforts",
            "reasonably acceptable",
            "reasonable discretion",
            "commercially reasonable"
        ],
        suggestion=(
            "Define objective standards or measurable criteria for reasonableness."
        ),
        min_hits=2
    ),

    Rule(
        id="RIGHTS_LOSS_BY_INACTION",
        title="Loss of Rights Due to Inaction",
        description=(
            "Failure to act, respond, or object within short timelines may permanently waive rights."
        ),
        risk_level="High",
        keywords=[
            "failure to respond",
            "shall be deemed accepted",
            "waive any objection",
            "if no response within"
        ],
        suggestion=(
            "Extend response timelines and avoid automatic waiver of rights."
        ),
    ),

    Rule(
        id="LONG_TERM_LOCK_IN",
        title="Long-Term Contract Lock-In",
        description=(
            "The agreement commits one party to a long fixed term without flexible exit options."
        ),
        risk_level="Medium",
        keywords=[
    "initial term of",
    "shall remain in effect for",
    "fixed term of",
    "multi-year term"
],
        suggestion=(
            "Add early termination rights or shorter initial terms."
        ),
        min_hits=2
    ),

    Rule(
        id="SERVICE_SUSPENSION_FOR_NONPAYMENT",
        title="Service Suspension for Non-Payment",
        description=(
            "Services may be suspended immediately for payment issues, disrupting operations."
        ),
        risk_level="High",
        keywords=[
    "suspend services for non-payment",
    "failure to pay invoices",
    "non-payment of fees",
    "services may be suspended"
],
        suggestion=(
            "Require notice and cure period before service suspension."
        ),
    ),

    Rule(
        id="IP_LICENSE_RESTRICTIONS",
        title="Highly Restricted IP License",
        description=(
            "The license granted is limited, revocable, and restricts transfer or continued use."
        ),
        risk_level="Medium",
        keywords=[
            "limited license",
            "revocable",
            "non-transferable",
            "license granted"
        ],
        suggestion=(
            "Seek broader, irrevocable, or perpetual usage rights where possible."
        ),
        min_hits=2
    ),
]