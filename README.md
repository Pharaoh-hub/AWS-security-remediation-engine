# AWS Cloud Security Posture Management (CSPM) & Auto-Remediation Engine

An automated, serverless event-driven security engineering framework designed to monitor multi-account AWS environments, audit infrastructure compliance in real-time, and execute automated event-driven remediation loops within 60 seconds of threat detection.

## 🛡️ Operational Blueprint

[ AWS Resource Drift ] ──► [ AWS Config / GuardDuty ] ──► [ EventBridge Rule ] ──► [ AWS Lambda ] ──► [ Automated Remediation ]


## 🔧 Core Architectural Features
* **Real-Time Threat Detection:** Utilizes native **AWS Config Rules** and **AWS GuardDuty** to monitor infrastructure drifts (e.g., unauthorized public S3 buckets, drifted security groups, or unencrypted data volumes).
* **Serverless Execution Fabric:** Engineered an **Amazon EventBridge** routing layer that captures compliance change events and securely triggers isolated execution workers.
* **Least-Privilege Execution:** Remediation tasks are handled by decoupled **AWS Lambda** microservices running customized Python (`boto3`) automation routines, executing via granular, zero-trust IAM roles.

## 🚀 Implemented Remediation Playbooks
1. **S3 Bucket Public Access Block:** Automatically intercepts the creation of any globally public S3 bucket policies, strips the malicious ACL, and applies an explicit bucket public-access block.
2. **IAM Credential Rotation Enforcement:** Monitors active access keys, flagging and automatically disabling programmatic credentials that have exceeded corporate rotation windows (e.g., 90 days).
3. **Security Group Ingress Hardening:** Detects and immediately tears down unauthorized ingress rules exposing port `22` (SSH) or `3389` (RDP) to the public internet (`0.0.0.0/0`), resetting the boundary to localized corporate CIDR blocks.

## 📁 Repository Structure
```text
aws-security-remediation-engine/
├── src/
│   ├── handlers/
│   │   ├── s3_remediator.py        # Python/Boto3 logic for bucket hardening
│   │   ├── iam_enforcer.py         # Key lifecycle rotation automation
│   │   └── network_hardener.py     # Real-time security group containment
│   └── utils/
│       └── logger.py               # CloudWatch metrics and audit logging
├── terraform/                      # Event routing & IAM structural code
│   ├── main.tf
│   ├── iam_policies.tf             # Execution roles with strict resource locks
│   └── eventbridge.tf              # Rule event patterns matching drifted states
└── README.md


👤 Maintainer
Oladoye Toyeeb

Role: Cloud Infrastructure & DevSecOps Engineer

Location: Lagos, Nigeria
