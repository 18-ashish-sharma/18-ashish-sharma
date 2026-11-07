<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/banner-m-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/banner-m-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="Ashish Sharma — Platform & DevOps Engineer. AWS, Azure, Kubernetes, Terraform, 7+ years." src="assets/banner-light.svg" width="100%">
</picture>

I build cloud platforms as code: Kubernetes on AWS, Terraform from the network up to the dashboards, pipelines that deploy without long-lived keys, and monitoring and cost controls in the same pull request as the resources. 7+ years across AWS and Azure. Based in India (IST, UTC+5:30).

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/numbers-m-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/numbers-m-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/numbers-dark.svg">
  <img alt="By the numbers, counted from the public repos: 6 Terraform modules, 6 pipeline definitions (4 GitHub Actions workflows and 2 Azure DevOps pipelines), 26 automated tests (14 pytest, 7 terraform test, 5 JUnit), 0 cloud keys stored in CI." src="assets/numbers-light.svg" width="100%">
</picture>

<p>
<a href="https://github.com/18-ashish-sharma/cost-optimisation-terraform/actions/workflows/terraform.yml"><img alt="cost--optimisation CI status" src="https://img.shields.io/github/actions/workflow/status/18-ashish-sharma/cost-optimisation-terraform/terraform.yml?branch=main&style=flat-square&label=cost--optimisation"></a>
<a href="https://github.com/18-ashish-sharma/azure-java-terraform/actions/workflows/terraform.yml"><img alt="azure--java%20terraform CI status" src="https://img.shields.io/github/actions/workflow/status/18-ashish-sharma/azure-java-terraform/terraform.yml?branch=main&style=flat-square&label=azure--java%20terraform"></a>
<a href="https://github.com/18-ashish-sharma/azure-java-terraform/actions/workflows/app.yml"><img alt="azure--java%20app CI status" src="https://img.shields.io/github/actions/workflow/status/18-ashish-sharma/azure-java-terraform/app.yml?branch=main&style=flat-square&label=azure--java%20app"></a>
</p>

<sub>Live pipeline status. Every pull request runs <code>terraform fmt</code>, <code>validate</code>, <code>tflint</code> and <code>checkov</code> (SARIF to the Security tab) without cloud credentials; in the AWS repos <code>gitleaks</code> also runs as a pre-commit hook.</sub>

## Featured work

<p>
<a href="https://github.com/18-ashish-sharma/eks-observability-terraform"><picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/card-m-eks-observability-terraform-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/card-m-eks-observability-terraform-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-eks-observability-terraform-dark.svg">
  <img alt="eks-observability-terraform: Prometheus and Grafana on EKS from one Terraform codebase across workspaces, CI on GitHub Actions and GitLab CI via OIDC, AWS Budgets guardrails. In progress." src="assets/card-eks-observability-terraform-light.svg" width="49%">
</picture></a>
<a href="https://github.com/18-ashish-sharma/aws-os-eks-logs-terraform"><picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/card-m-aws-os-eks-logs-terraform-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/card-m-aws-os-eks-logs-terraform-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-aws-os-eks-logs-terraform-dark.svg">
  <img alt="aws-os-eks-logs-terraform: VPC and EKS, pod logs shipped by a Fluent Bit DaemonSet using IRSA to Amazon OpenSearch, SAML sign-in through Microsoft Entra ID." src="assets/card-aws-os-eks-logs-terraform-light.svg" width="49%">
</picture></a>
<a href="https://github.com/18-ashish-sharma/cost-optimisation-terraform"><picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/card-m-cost-optimisation-terraform-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/card-m-cost-optimisation-terraform-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-cost-optimisation-terraform-dark.svg">
  <img alt="cost-optimisation-terraform: scheduled stop and start of tagged EC2 and RDS through EventBridge and Lambda with tag-scoped IAM, plus AWS Budgets and anomaly alerts over SNS. Tested with pytest, moto and terraform test." src="assets/card-cost-optimisation-terraform-light.svg" width="49%">
</picture></a>
<a href="https://github.com/18-ashish-sharma/azure-java-terraform"><picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/card-m-azure-java-terraform-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/card-m-azure-java-terraform-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-azure-java-terraform-dark.svg">
  <img alt="azure-java-terraform: Spring Boot on Java 17 on Azure App Service with PostgreSQL Flexible Server and Key Vault through managed identity, deployed with GitHub Actions OIDC and an approval gate, plus Azure DevOps pipelines." src="assets/card-azure-java-terraform-light.svg" width="49%">
</picture></a>
</p>

<sub>Also: <a href="https://github.com/18-ashish-sharma/aws-terraform-react-js">aws-terraform-react-js</a> (React on S3 with Terraform) · <a href="https://github.com/18-ashish-sharma/azure-react-storage">azure-react-storage</a> (React on Azure Storage with Terraform). Both are being tidied up.</sub>

<br>

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/infra-map-m-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/infra-map-m-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/infra-map-dark.svg">
  <img alt="How the work fits together: 01 Code in Git with review, 02 CI/CD on GitHub Actions, GitLab CI and Azure DevOps with OIDC and approval-gated apply, 03 Terraform modules and remote state gated by tflint, checkov and gitleaks, 04 Cloud on AWS and Azure, 05 Observability with Prometheus, Grafana and Fluent Bit to OpenSearch with SAML, 06 FinOps with AWS Budgets and scheduled stop-start. Metrics and spend feed the next change." src="assets/infra-map-light.svg" width="100%">
</picture>

## Currently

- **Running a multi-service platform on Kubernetes** at work: Helm charts per service, CI that builds and tests every change, CD pipelines that roll releases out, and PostgreSQL behind it.
- **Writing observability and cost guardrails as code:** Prometheus and Grafana on EKS, budgets and off-hours scheduling in Terraform.
- **Raising the bar on my public repos:** pinned providers, CI gates on every pull request, and READMEs that describe exactly what the code does.

## Certifications

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/certs-m-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/certs-m-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/certs-dark.svg">
  <img alt="Certifications: AWS Certified DevOps Engineer – Professional; Certified Kubernetes Administrator (CKA); Certified Kubernetes Security Specialist (CKS); NVIDIA-Certified Associate: AI Infrastructure and Operations." src="assets/certs-light.svg" width="100%">
</picture>

## Toolbox

| Area | Tools |
|---|---|
| Cloud | AWS (EKS, Lambda, EventBridge, RDS, OpenSearch, IAM, Budgets) · Azure (App Service, PostgreSQL Flexible, Key Vault, Entra ID) |
| Infrastructure as code | Terraform: modules, remote state with locking, workspaces, `terraform test` |
| Containers | Kubernetes, Amazon EKS, Helm, Fluent Bit |
| CI/CD | GitHub Actions, GitLab CI, Azure DevOps · OIDC / workload identity federation |
| Observability | Prometheus, Grafana, OpenSearch, CloudWatch, Application Insights |
| Security | tflint, checkov, gitleaks, least-privilege IAM, IRSA, SAML SSO |
| FinOps | AWS Budgets, Cost Anomaly Detection, scheduled stop/start, rightsizing |
| Languages | HCL, Python, Bash, YAML |

## How I work

- **Everything as code.** Infrastructure, pipelines, dashboards and alerts live in Git and change through review. A console click that isn't in code is drift.
- **Least privilege by default.** CI gets short-lived credentials through OIDC, workloads get scoped roles, people sign in through SSO.
- **Read the plan before the apply.** Production applies run a saved plan behind an approval gate, never a fresh one.
- **Observable and costed from day one.** Metrics, logs, budgets and off-hours schedules ship with the service, not after the first incident or the first bill.

---

<sub>Questions about any of this work: open an issue on the repository it relates to. Browse everything on the <a href="https://github.com/18-ashish-sharma?tab=repositories">repositories tab</a>.</sub>
