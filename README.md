# CloudOps Incident Assistant

An AI-assisted incident analysis dashboard built to help cloud and DevOps engineers investigate application incidents using logs, system metrics, and AWS monitoring data.

## Overview

CloudOps Incident Assistant combines rule-based incident detection, AI-assisted troubleshooting, local system monitoring, and AWS observability in one dashboard.

The project is designed to help engineers identify potential causes of incidents, understand relevant evidence, and plan safe troubleshooting steps. AI-generated recommendations require human review and are not automatically executed.

## Features

- **Incident log analysis:** Analyze supplied logs using rule-based patterns.
- **Gemma 4 AI analysis:** Generate incident summaries, possible root causes, severity assessments, and troubleshooting recommendations.
- **System monitoring:** View CPU, memory, and disk utilization from the application environment.
- **AWS EC2 health:** Retrieve EC2 instance state and status checks using Boto3.
- **Amazon CloudWatch integration:** Retrieve and display EC2 CPU utilization metrics.
- **Incident history:** Store incident records in SQLite using persistent Docker storage.
- **Containerized deployment:** Run the application using Docker.
- **Reverse proxy:** Use Nginx to expose the Streamlit application through HTTP port 80.

## Architecture

```text
                    User / Browser
                          |
                       HTTP :80
                          |
                    Nginx Proxy
                          |
                    Streamlit :8501
                          |
             CloudOps Incident Assistant
                 /        |         \
                /         |          \
        Rule-based     Gemma 4      System
        log analysis   AI API       metrics
                          |
                    Human review
                          |
                 Safe troubleshooting

       AWS EC2 APIs -------- Boto3
       CloudWatch ---------- CPU metrics

       SQLite database ---- /data/incidents.db
                                   |
                         Docker named volume
                    cloudops_incident_data
```

### Technology Stack

| Component | Technology |
|---|---|
| Application interface | Streamlit |
| Programming language | Python |
| AI incident analysis | Hosted Gemma 4 through Google Gen AI SDK |
| AWS integration | Boto3 |
| Cloud monitoring | Amazon CloudWatch |
| Compute | Amazon EC2 |
| Containerization | Docker |
| Reverse proxy | Nginx |
| Incident storage | SQLite |

## Deployment

The application runs in a Docker container on an Ubuntu EC2 instance. Nginx forwards HTTP requests to Streamlit, which listens on port 8501 locally.

The application container uses a named Docker volume to preserve SQLite incident history across container restarts.

### Persistent Storage

```text
Container database: /data/incidents.db
Docker volume:      cloudops_incident_data
```

The incident history persistence test confirmed that four saved records remained available after restarting the application container.

### AWS Permissions

The EC2 instance uses an IAM role for AWS API access. The implemented integrations require read access to relevant EC2 instance health information and CloudWatch metrics.

Use least-privilege IAM permissions and avoid storing AWS access keys directly in application code.

## AI Safety

Gemma 4 provides decision support, not autonomous remediation.

- AI recommendations may be incorrect.
- Root causes are hypotheses until verified.
- Severity assessments should be checked against real evidence and impact.
- Commands should be reviewed before execution.
- The application does not automatically execute AI-generated remediation commands.

## Security Considerations

- Keep API keys in environment variables and never commit `.env`.
- Restrict EC2 security group access to the required ports and trusted sources.
- Use an IAM role with only the permissions the application needs.
- Review logs and diagnostic output before sharing them because they may contain sensitive information.
- Consider HTTPS and authentication before exposing the dashboard to public users.

## Cost-Conscious Design

The project reuses an existing EC2 instance and Docker deployment. SQLite avoids the need for a separate database service, and the application retrieves existing CloudWatch metrics instead of requiring a separate monitoring server.

AWS charges may still apply to EC2, storage, data transfer, and other usage. Hosted AI API usage may also be subject to the provider's pricing and quotas. Check your billing dashboard and API plan.

## Testing

The following scenarios were tested with sample incident logs:

1. High CPU utilization and increased response latency.
2. Database connection timeouts and possible connection pool exhaustion.
3. Disk-space exhaustion and failed file writes.

These are simulated incident scenarios. They do not establish that the deployed application experienced those failures.

Container storage persistence was also tested by restarting the container and verifying that the incident count remained at four.

## Future Improvements

- More structured evidence collection and confidence-aware severity assessment.
- Additional metric and log integrations.
- Automated test coverage for incident analysis and storage.
- Improved authentication and HTTPS configuration.
- A documented demonstration workflow for incident investigation.


