"""Generate light/dark SVG assets for the GitHub profile README."""
import sys, pathlib

OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", text="#e6edf3", muted="#8b949e",
                 faint="#21262d", accent="#7ee787", accent2="#79c0ff", prompt="#7ee787",
                 ramp=["#7ee787", "#56d4dd", "#79c0ff", "#a5a5ff", "#d2a8ff", "#ffa657"],
                 dots=("#ff7b72", "#d29922", "#3fb950")),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#59636e",
                  faint="#eaeef2", accent="#1a7f37", accent2="#0969da", prompt="#1a7f37",
                  ramp=["#1a7f37", "#0e7c86", "#0969da", "#5a4fcf", "#8250df", "#bc4c00"],
                  dots=("#cf222e", "#9a6700", "#1a7f37")),
}

REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def banner(t, mode):
    W, H = 1000, 270
    lines = [
        ("$", "terraform validate"),
        ("", "Success! The configuration is valid."),
        ("$", "terraform plan -out=tfplan"),
        ("$", "kubectl -n monitoring get pods"),
        ("$", ""),
    ]
    term = []
    y = 104
    for i, (p, cmd) in enumerate(lines):
        delay = 0.3 + i * 0.55
        if p:
            term.append(f'<text class="ln" style="animation-delay:{delay:.2f}s" x="60" y="{y}">'
                        f'<tspan fill="{t["muted"]}">~/infra </tspan><tspan fill="{t["prompt"]}">$</tspan> '
                        f'<tspan fill="{t["text"]}">{cmd}</tspan></text>')
        else:
            term.append(f'<text class="ln" style="animation-delay:{delay:.2f}s" x="60" y="{y}" fill="{t["accent"]}">{cmd}</text>')
        y += 28
    cursor_y = y - 28
    # hex motif (kubernetes-ish nodes) on the right, faint
    hexes = []
    import math
    def hexpath(cx, cy, r):
        pts = [(cx + r * math.cos(math.radians(60 * k - 30)), cy + r * math.sin(math.radians(60 * k - 30))) for k in range(6)]
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    for (cx, cy) in [(938, 44), (966, 60), (938, 76), (966, 92), (910, 60)]:
        hexes.append(f'<path d="{hexpath(cx, cy, 15)}" fill="none" stroke="{t["border"]}" stroke-width="1.2"/>')
    hexes.append(f'<path class="pulse" d="{hexpath(938, 76, 15)}" fill="none" stroke="{t["accent2"]}" stroke-width="1.6"/>')

    chips = []
    x = 540
    for label in ["AWS DevOps Pro", "CKA", "CKS", "NVIDIA AI Infra"]:
        w = 14 + len(label) * 7.4
        chips.append(f'<rect x="{x}" y="200" width="{w:.0f}" height="26" rx="13" fill="none" stroke="{t["border"]}"/>'
                     f'<text x="{x + w / 2:.0f}" y="217.5" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{label}</text>')
        x += w + 8

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">Ashish Sharma — Platform &amp; DevOps Engineer</title>
<desc id="d">Banner with a terminal running terraform validate, terraform plan and kubectl, next to the name Ashish Sharma, the title Platform and DevOps Engineer, the focus areas AWS, Kubernetes, Terraform and FinOps, and four certifications: AWS DevOps Engineer Professional, CKA, CKS and NVIDIA AI Infrastructure.</desc>
<defs>
<pattern id="g" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.1" fill="{t["faint"]}"/></pattern>
<style>
.cur {{ animation: blink 1.1s steps(1) infinite; }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
.pulse {{ animation: pulse 3.2s ease-in-out infinite; }}
@keyframes pulse {{ 0%,100% {{ opacity: .15; }} 50% {{ opacity: 1; }} }}
{REDUCED}
</style>
</defs>
<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}"/>
<rect width="{W}" height="{H}" rx="14" fill="url(#g)"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{t["border"]}"/>
{"".join(hexes)}
<g>
<rect x="30" y="34" width="470" height="202" rx="10" fill="{t["panel"]}" stroke="{t["border"]}"/>
<path d="M30 44a10 10 0 0 1 10-10h450a10 10 0 0 1 10 10v20H30z" fill="{t["faint"]}"/>
<circle cx="50" cy="49" r="5" fill="{t["dots"][0]}"/><circle cx="68" cy="49" r="5" fill="{t["dots"][1]}"/><circle cx="86" cy="49" r="5" fill="{t["dots"][2]}"/>
<text x="265" y="53.5" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["muted"]}">platform — zsh</text>
<g font-family="{MONO}" font-size="13.5">
{chr(10).join(term)}
<rect class="cur" x="139" y="{cursor_y - 13}" width="8" height="16" fill="{t["accent"]}"/>
</g>
</g>
<g font-family="{SANS}">
<text x="540" y="100" font-size="44" font-weight="700" fill="{t["text"]}" letter-spacing="-0.5">Ashish Sharma</text>
<text x="541" y="136" font-size="21" font-weight="600" fill="{t["accent2"]}">Platform &amp; DevOps Engineer</text>
<text x="541" y="170" font-family="{MONO}" font-size="13.5" fill="{t["muted"]}">AWS · Kubernetes · Terraform · FinOps</text>
</g>
{"".join(chips)}
</svg>
'''


def infra_map(t, mode):
    W, H = 1000, 500
    cw, ch = 290, 170
    xs = [25, 355, 685]
    y1, y2 = 70, 300
    stages = [
        ("01", "Code", ["Git, pull-request review", "HCL · Python · YAML", "plan output read before apply"], "every repo below"),
        ("02", "CI / CD", ["GitHub Actions · GitLab CI", "Azure DevOps Pipelines", "OIDC to AWS — no static keys"], "eks-observability-terraform"),
        ("03", "Infrastructure as Code", ["Terraform modules", "workspaces + remote state", "dev / stage / prod layouts"], "all four Terraform repos"),
        ("04", "Cloud", ["AWS: EKS · OpenSearch · Lambda", "EventBridge · S3 · RDS · IAM", "Azure: App Service · PostgreSQL"], "aws-os-eks-logs · azure-java"),
        ("05", "Observability", ["Prometheus · Grafana", "OpenSearch for pod logs", "SAML SSO via Azure AD"], "eks-observability · aws-os-eks-logs"),
        ("06", "FinOps", ["AWS Budgets + alerts", "EventBridge → Lambda", "scheduled EC2 / RDS stop-start"], "cost-optimisation-terraform"),
    ]
    # row1 L->R positions 0,1,2 ; row2 R->L: stage 4 at x2, 5 at x1, 6 at x0
    pos = [(xs[0], y1), (xs[1], y1), (xs[2], y1), (xs[2], y2), (xs[1], y2), (xs[0], y2)]
    cards = []
    for i, ((num, title, items, repo), (x, y)) in enumerate(zip(stages, pos)):
        c = t["ramp"][i]
        body = "".join(
            f'<text x="{x + 20}" y="{y + 78 + k * 23}" font-size="14" fill="{t["text"]}">{esc(it) if "→" not in it else it.replace("&", "&amp;")}</text>'
            for k, it in enumerate(items))
        cards.append(f'''<g>
<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>
<rect x="{x}" y="{y + 14}" width="3" height="30" rx="1.5" fill="{c}"/>
<text x="{x + 20}" y="{y + 36}" font-family="{MONO}" font-size="13" fill="{c}">{num}</text>
<text x="{x + 48}" y="{y + 36}" font-size="17" font-weight="650" fill="{t["text"]}">{esc(title)}</text>
<line x1="{x + 20}" y1="{y + 54}" x2="{x + cw - 20}" y2="{y + 54}" stroke="{t["faint"]}"/>
{body}
<text x="{x + 20}" y="{y + ch - 14}" font-family="{MONO}" font-size="11.5" fill="{t["muted"]}">↳ {esc(repo)}</text>
</g>''')

    ac = t["muted"]
    flows = []
    mid1 = y1 + ch / 2
    mid2 = y2 + ch / 2
    # row1 arrows
    for a, b in [(0, 1), (1, 2)]:
        x0 = xs[a] + cw + 4
        x1 = xs[b] - 6
        flows.append(f'<path class="flow" d="M{x0} {mid1} H{x1}"/>')
        flows.append(f'<path d="M{x1 - 7} {mid1 - 5} L{x1} {mid1} L{x1 - 7} {mid1 + 5}" class="head"/>')
    # turn down on the right: from IaC bottom to Cloud top
    xc = xs[2] + cw / 2
    flows.append(f'<path class="flow" d="M{xc} {y1 + ch + 4} V{y2 - 6}"/>')
    flows.append(f'<path d="M{xc - 5} {y2 - 13} L{xc} {y2 - 6} L{xc + 5} {y2 - 13}" class="head"/>')
    # row2 R->L
    for a, b in [(2, 1), (1, 0)]:
        x0 = xs[a] - 4
        x1 = xs[b] + cw + 6
        flows.append(f'<path class="flow" d="M{x0} {mid2} H{x1}"/>')
        flows.append(f'<path d="M{x1 + 7} {mid2 - 5} L{x1} {mid2} L{x1 + 7} {mid2 + 5}" class="head"/>')
    # feedback loop: FinOps -> Code (left side)
    xf = xs[0] + cw / 2
    flows.append(f'<path class="flow fb" d="M{xf} {y2 - 4} V{y1 + ch + 6}"/>')
    flows.append(f'<path d="M{xf - 5} {y1 + ch + 13} L{xf} {y1 + ch + 6} L{xf + 5} {y1 + ch + 13}" class="head"/>')
    flows.append(f'<text x="{xf + 12}" y="{(y1 + ch + y2) / 2 + 4}" font-family="{MONO}" font-size="11.5" fill="{t["muted"]}">metrics + spend feed the next change</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">How the work fits together</title>
<desc id="d">A six-stage loop. 01 Code in Git with pull-request review. 02 CI/CD on GitHub Actions, GitLab CI and Azure DevOps using OIDC instead of static keys. 03 Terraform modules with workspaces and remote state. 04 Cloud: AWS EKS, OpenSearch, Lambda, EventBridge, S3, RDS and IAM, and Azure App Service and PostgreSQL. 05 Observability with Prometheus, Grafana and OpenSearch with SAML SSO. 06 FinOps with AWS Budgets and scheduled EC2 and RDS stop-start. Metrics and spend feed back into the next code change. Each stage names the public repository that shows it.</desc>
<style>
.flow {{ fill: none; stroke: {ac}; stroke-width: 1.6; stroke-dasharray: 6 6; animation: dash 1.4s linear infinite; }}
.fb {{ stroke-dasharray: 2 6; }}
.head {{ fill: none; stroke: {ac}; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }}
@keyframes dash {{ to {{ stroke-dashoffset: -24; }} }}
{REDUCED}
</style>
<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{t["border"]}"/>
<g font-family="{SANS}">
<text x="25" y="44" font-size="15" font-weight="600" fill="{t["text"]}">How the work fits together</text>
<text x="975" y="44" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t["muted"]}">every box is code in a public repo</text>
{"".join(flows)}
{"".join(cards)}
</g>
</svg>
'''


for mode, t in THEMES.items():
    (OUT / f"banner-{mode}.svg").write_text(banner(t, mode))
    (OUT / f"infra-map-{mode}.svg").write_text(infra_map(t, mode))
print("ok")
