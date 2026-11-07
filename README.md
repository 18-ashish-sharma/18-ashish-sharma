<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
  <img alt="Ashish Sharma: Platform & DevOps Engineer. AWS, Kubernetes, Terraform, FinOps." src="assets/banner-light.svg" width="100%">
</picture>

I build cloud platforms as code: Kubernetes on AWS, Terraform from network to dashboards, CI that deploys without long-lived keys, and monitoring and cost controls included from the first commit. 7+ years across AWS and Azure.

<p>
  <a href="https://github.com/18-ashish-sharma?tab=repositories"><img alt="Repositories" src="https://img.shields.io/badge/repositories-browse-24292f?style=flat-square&logo=github&logoColor=white"></a>
</p>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/infra-map-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/infra-map-light.svg">
  <img alt="How the work fits together: Code, then CI/CD (GitHub Actions, GitLab CI, Azure DevOps, OIDC), then Terraform, then AWS and Azure, then observability (Prometheus, Grafana, OpenSearch), then FinOps (Budgets, scheduled stop-start), with metrics and spend feeding the next change." src="assets/infra-map-light.svg" width="100%">
</picture>

## Featured work

<table>
<tr>
<td width="50%" valign="top">

**[eks-observability-terraform](https://github.com/18-ashish-sharma/eks-observability-terraform)**<br>
Prometheus and Grafana on EKS, with one Terraform codebase across environments using workspaces. CI runs on both GitHub Actions and GitLab CI, authenticating to AWS through OIDC with no stored keys. AWS Budgets set the spending guardrails.

<sub>`Terraform` · `EKS` · `Prometheus` · `Grafana` · `OIDC` · `GitLab CI` · `AWS Budgets`</sub>

</td>
<td width="50%" valign="top">

**[aws-os-eks-logs-terraform](https://github.com/18-ashish-sharma/aws-os-eks-logs-terraform)**<br>
Sends EKS pod logs to Amazon OpenSearch, with SAML single sign-on through Azure AD. Built from separate modules for the cluster, the search domain and remote state.

<sub>`Terraform` · `EKS` · `OpenSearch` · `SAML SSO` · `Azure AD`</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

**[cost-optimisation-terraform](https://github.com/18-ashish-sharma/cost-optimisation-terraform)**<br>
Puts idle-time spending under code. EventBridge schedules trigger Python Lambdas that stop and start EC2 and RDS outside working hours, using scoped IAM roles, with checks in CI.

<sub>`Terraform` · `Lambda` · `EventBridge` · `Python` · `IAM` · `FinOps`</sub>

</td>
<td width="50%" valign="top">

**[azure-java-terraform](https://github.com/18-ashish-sharma/azure-java-terraform)**<br>
Azure App Service and PostgreSQL provisioned separately for dev, stage and prod. A Spring Boot service is deployed by both Azure DevOps and GitHub Actions pipelines.

<sub>`Terraform` · `Azure` · `App Service` · `PostgreSQL` · `Azure DevOps` · `GitHub Actions`</sub>

</td>
</tr>
</table>

## Toolbox

| | |
|---|---|
| **Cloud** | ![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square) ![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat-square) |
| **IaC** | ![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white) |
| **Containers** | ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white) ![Amazon EKS](https://img.shields.io/badge/Amazon_EKS-FF9900?style=flat-square) |
| **CI/CD** | ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white) ![GitLab CI](https://img.shields.io/badge/GitLab_CI-FC6D26?style=flat-square&logo=gitlab&logoColor=white) ![Azure DevOps](https://img.shields.io/badge/Azure_DevOps-0078D7?style=flat-square) |
| **Observability** | ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white) ![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white) ![OpenSearch](https://img.shields.io/badge/OpenSearch-005EB8?style=flat-square&logo=opensearch&logoColor=white) |
| **Security** | ![OIDC](https://img.shields.io/badge/OIDC_federation-555?style=flat-square&logo=openid&logoColor=white) ![SAML SSO](https://img.shields.io/badge/SAML_SSO-555?style=flat-square) ![IAM](https://img.shields.io/badge/IAM_least_privilege-555?style=flat-square) |
| **Languages** | ![HCL](https://img.shields.io/badge/HCL-844FBA?style=flat-square&logo=terraform&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=white) ![YAML](https://img.shields.io/badge/YAML-CB171E?style=flat-square&logo=yaml&logoColor=white) |

## Certifications

| | Certification | Issuer |
|---|---|---|
| ☁️ | AWS Certified DevOps Engineer – Professional | Amazon Web Services |
| ⎈ | Certified Kubernetes Administrator (CKA) | CNCF / The Linux Foundation |
| ⎈ | Certified Kubernetes Security Specialist (CKS) | CNCF / The Linux Foundation |
| ▣ | NVIDIA-Certified Associate: AI Infrastructure and Operations | NVIDIA |

## How I work

- **Everything as code.** Infrastructure, pipelines, dashboards and alerts live in Git and change through review. A console click that isn't in code is drift.
- **Least privilege by default.** CI gets short-lived credentials through OIDC, workloads get scoped roles, and people sign in through SSO.
- **Observable by design.** Metrics, logs and dashboards ship with the service, not after the first incident.
- **Cost is a requirement.** Budgets, alerts and off-hours scheduling go in the same pull request as the resources they pay for.
