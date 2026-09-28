from typing import List, Optional
from ai_memory_agent.models.compliance import SecurityControl, ComplianceFramework

# Standard registry of security controls mapped across industry frameworks
SECURITY_CONTROLS_REGISTRY: List[SecurityControl] = [
    # Access Control / IAM Controls
    SecurityControl(
        control_id="SOC2-CC6.1",
        framework=ComplianceFramework.SOC2,
        name="Logical Access Security",
        category="Access Control",
        description="The entity implements logical access security software, infrastructure, and architectures over protected information assets to protect them from security events.",
        remediation_guidance="Enforce least privilege access, disable anonymous/public access policies, and require IAM authentication.",
    ),
    SecurityControl(
        control_id="SOC2-CC6.3",
        framework=ComplianceFramework.SOC2,
        name="Access Modification and Revocation",
        category="Access Control",
        description="The entity authorizes, modifies, or removes access to data, software, functions, and other protected information assets based on authorized personnel changes.",
        remediation_guidance="Audit and revoke excessive access permissions, implement role-based access control (RBAC).",
    ),
    SecurityControl(
        control_id="NIST-PR.AC-04",
        framework=ComplianceFramework.NIST_CSF,
        name="Access Permissions Management",
        category="Access Control",
        description="Access permissions and authorizations are managed, incorporating the principles of least privilege and separation of duties.",
        remediation_guidance="Implement strict bucket policies, disable S3 public read/write grants, and configure automated policy linting.",
    ),
    SecurityControl(
        control_id="NIST-PR.AA-01",
        framework=ComplianceFramework.NIST_CSF,
        name="Identities and Credentials Verification",
        category="Access Control",
        description="Identities and credentials for authorized users, services, and hardware are managed, verified, and revoked.",
        remediation_guidance="Enforce MFA, restrict service role trust relationships, and disallow wildcard principals.",
    ),
    SecurityControl(
        control_id="ISO-A.5.15",
        framework=ComplianceFramework.ISO27001,
        name="Access Control Policy",
        category="Access Control",
        description="Rules to control physical and logical access to information and other associated assets shall be established and documented.",
        remediation_guidance="Establish explicit bucket policy boundaries and eliminate public ACL exemptions.",
    ),
    SecurityControl(
        control_id="CIS-Control-6.1",
        framework=ComplianceFramework.CIS_CONTROLS,
        name="Establish an Access Granting Process",
        category="Access Control",
        description="Establish and follow an access granting process that adheres to least privilege principles for all digital assets.",
        remediation_guidance="Apply S3 Block Public Access at the AWS account and bucket levels.",
    ),

    # Data Protection & Storage Controls
    SecurityControl(
        control_id="SOC2-CC6.6",
        framework=ComplianceFramework.SOC2,
        name="Boundary Protection and Perimeter Controls",
        category="Data Protection",
        description="The entity implements logical boundaries to protect against external attacks and unauthorized ingress/egress.",
        remediation_guidance="Place storage endpoints inside VPC with private endpoints and restrict CIDR blocks.",
    ),
    SecurityControl(
        control_id="SOC2-CC6.7",
        framework=ComplianceFramework.SOC2,
        name="Data Transmission and Protection",
        category="Data Protection",
        description="The entity restricts transmission, movement, and storage of sensitive data to authorized channels.",
        remediation_guidance="Enforce TLS 1.3 in-transit and KMS envelope encryption at rest.",
    ),
    SecurityControl(
        control_id="NIST-PR.DS-01",
        framework=ComplianceFramework.NIST_CSF,
        name="Data-at-Rest Protection",
        category="Data Protection",
        description="Data-at-rest is protected through cryptographic controls and access restriction mechanisms.",
        remediation_guidance="Enable default AWS KMS Customer Managed Key encryption.",
    ),
    SecurityControl(
        control_id="ISO-A.8.12",
        framework=ComplianceFramework.ISO27001,
        name="Data Leakage Prevention",
        category="Data Protection",
        description="Data leakage prevention measures shall be applied to systems, networks and any other devices that process, store or transmit sensitive information.",
        remediation_guidance="Deploy Amazon Macie or automated DLP scanners to flag exposed sensitive data.",
    ),

    # Monitoring, Logging & Incident Response Controls
    SecurityControl(
        control_id="SOC2-CC7.2",
        framework=ComplianceFramework.SOC2,
        name="Security Monitoring and Anomaly Detection",
        category="Monitoring",
        description="The entity monitors system components and the operation of controls to identify anomalies and indications of compromise.",
        remediation_guidance="Enable CloudTrail S3 data event logging and GuardDuty S3 Protection.",
    ),
    SecurityControl(
        control_id="NIST-DE.CM-01",
        framework=ComplianceFramework.NIST_CSF,
        name="Network and Asset Monitoring",
        category="Monitoring",
        description="Networks and assets are monitored to identify potential cybersecurity events.",
        remediation_guidance="Configure AWS Config rules 's3-bucket-public-read-prohibited' with automated SNS alerting.",
    ),
    SecurityControl(
        control_id="ISO-A.8.16",
        framework=ComplianceFramework.ISO27001,
        name="Monitoring Activities",
        category="Monitoring",
        description="Networks, systems and applications shall be monitored for anomalous behavior and appropriate actions taken to evaluate potential information security incidents.",
        remediation_guidance="Forward CloudTrail and access logs to centralized SIEM with immediate alerting on ACL changes.",
    ),
]


def find_controls_by_category(category_keyword: str) -> List[SecurityControl]:
    keyword = category_keyword.lower()
    return [
        ctrl for ctrl in SECURITY_CONTROLS_REGISTRY
        if keyword in ctrl.category.lower() or keyword in ctrl.name.lower() or keyword in ctrl.description.lower()
    ]


def find_control_by_id(control_id: str) -> Optional[SecurityControl]:
    clean_id = control_id.strip().upper()
    for ctrl in SECURITY_CONTROLS_REGISTRY:
        if ctrl.control_id.upper() == clean_id:
            return ctrl
    return None
