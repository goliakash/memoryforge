from typing import Dict, Any, List
from ai_memory_agent.models.investigation import MITRETechnique

THREAT_PATTERNS: Dict[str, Dict[str, Any]] = {
    "public_cloud_storage_exposure": {
        "keywords": ["storage", "bucket", "s3", "blob", "public read", "public access", "cloud storage", "acl"],
        "mitre_techniques": [
            MITRETechnique(technique_id="T1530", name="Data from Cloud Storage", tactic="Collection"),
            MITRETechnique(technique_id="T1580", name="Cloud Infrastructure Discovery", tactic="Discovery"),
            MITRETechnique(technique_id="T1190", name="Exploit Public-Facing Application", tactic="Initial Access"),
        ],
        "root_cause_category": "Access Policy Misconfiguration",
        "primary_control_category": "Access Control",
        "default_controls": ["SOC2-CC6.1", "NIST-PR.AC-04", "ISO-A.5.15"],
    },
    "iam_privilege_escalation": {
        "keywords": ["iam", "role", "assume_role", "privilege escalation", "wildcard", "admin policy", "permission"],
        "mitre_techniques": [
            MITRETechnique(technique_id="T1078.004", name="Valid Accounts: Cloud Accounts", tactic="Defense Evasion"),
            MITRETechnique(technique_id="T1098", name="Account Manipulation", tactic="Persistence"),
        ],
        "root_cause_category": "Excessive IAM Permissions",
        "primary_control_category": "Access Control",
        "default_controls": ["SOC2-CC6.3", "NIST-PR.AA-01", "CIS-Control-6.1"],
    },
    "unencrypted_sensitive_data": {
        "keywords": ["unencrypted", "plaintext", "encryption", "kms", "data leak", "ssl", "tls"],
        "mitre_techniques": [
            MITRETechnique(technique_id="T1005", name="Data from Local System", tactic="Collection"),
        ],
        "root_cause_category": "Cryptographic Control Failure",
        "primary_control_category": "Data Protection",
        "default_controls": ["SOC2-CC6.7", "NIST-PR.DS-01", "ISO-A.8.12"],
    },
    "unmonitored_infrastructure": {
        "keywords": ["logging disabled", "cloudtrail", "guardduty", "unmonitored", "alert failure"],
        "mitre_techniques": [
            MITRETechnique(technique_id="T1562.001", name="Impair Defenses: Disable or Modify Tools", tactic="Defense Evasion"),
        ],
        "root_cause_category": "Observability and Auditing Deficit",
        "primary_control_category": "Monitoring",
        "default_controls": ["SOC2-CC7.2", "NIST-DE.CM-01", "ISO-A.8.16"],
    },
}


def match_threat_pattern(text: str) -> Dict[str, Any]:
    text_lower = text.lower()
    best_pattern = THREAT_PATTERNS["public_cloud_storage_exposure"]
    max_score = 0

    for pattern_key, pattern_data in THREAT_PATTERNS.items():
        score = sum(1 for kw in pattern_data["keywords"] if kw in text_lower)
        if score > max_score:
            max_score = score
            best_pattern = pattern_data

    return best_pattern
