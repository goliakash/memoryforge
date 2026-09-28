from typing import List
from ai_memory_agent.models.compliance import RemediationStep, RemediationStatus


def generate_storage_exposure_remediation(asset_name: str) -> List[RemediationStep]:
    return [
        RemediationStep(
            step_id=f"REM-{asset_name}-01",
            action="Remove public read and write access grants from bucket ACL and policy",
            target_asset=asset_name,
            priority=1,
            status=RemediationStatus.PENDING,
            command_or_config=f"aws s3api put-public-access-block --bucket {asset_name} --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true",
            verification_criteria=f"Execute 'aws s3api get-public-access-block --bucket {asset_name}' and verify all 4 flags return true.",
        ),
        RemediationStep(
            step_id=f"REM-{asset_name}-02",
            action="Enable preventive cloud protection and account-level Guardrail",
            target_asset=asset_name,
            priority=2,
            status=RemediationStatus.PENDING,
            command_or_config="aws s3control put-public-access-block --account-id $AWS_ACCOUNT_ID --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true",
            verification_criteria="Ensure account-wide SCP (Service Control Policy) denies s3:PutBucketPolicy with Principal: '*'.",
        ),
        RemediationStep(
            step_id=f"REM-{asset_name}-03",
            action="Review and restrict IAM policies attached to service roles and pipelines",
            target_asset=asset_name,
            priority=3,
            status=RemediationStatus.PENDING,
            command_or_config=f"aws s3api get-bucket-policy --bucket {asset_name} | jq '.Statement[] | select(.Principal == \"*\")'",
            verification_criteria="Confirm bucket policy contains explicit Deny for all non-authenticated and non-VPC principals.",
        ),
        RemediationStep(
            step_id=f"REM-{asset_name}-04",
            action="Enable automated compliance monitoring and real-time alerts",
            target_asset=asset_name,
            priority=4,
            status=RemediationStatus.PENDING,
            command_or_config=f"aws configservice put-evaluations --evaluations ComplianceType=COMPLIANT,ComplianceResourceId={asset_name},ComplianceResourceType=AWS::S3::Bucket",
            verification_criteria="AWS Config rule 's3-bucket-public-read-prohibited' evaluates to COMPLIANT with CloudWatch alarm active.",
        ),
    ]


def generate_iam_remediation(asset_name: str) -> List[RemediationStep]:
    return [
        RemediationStep(
            step_id=f"REM-{asset_name}-01",
            action="Revoke administrator privileges and remove wildcard '*' permissions",
            target_asset=asset_name,
            priority=1,
            status=RemediationStatus.PENDING,
            command_or_config=f"aws iam detach-role-policy --role-name {asset_name} --policy-arn arn:aws:iam::aws:policy/AdministratorAccess",
            verification_criteria="Validate IAM Access Analyzer identifies zero external or unintended access findings.",
        ),
        RemediationStep(
            step_id=f"REM-{asset_name}-02",
            action="Implement least-privilege inline policy scoped to specific resource ARNs",
            target_asset=asset_name,
            priority=2,
            status=RemediationStatus.PENDING,
            command_or_config=f"aws iam put-role-policy --role-name {asset_name} --policy-name ScopedLeastPrivilege --policy-document file://scoped-policy.json",
            verification_criteria="Confirm role cannot perform actions outside authorized service actions.",
        ),
    ]
