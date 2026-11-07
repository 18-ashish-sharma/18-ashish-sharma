"""Generate the light/dark SVG assets for the GitHub profile README.

Usage: python3 assets/gen_svgs.py assets [path/to/avatar.svg]

Every asset is written twice (dark, light). The banner, numbers strip, work map and
certifications also get a "-m" (mobile) variant: a taller, stacked layout that the
README serves to narrow screens through <picture media="(max-width: 600px)">.
System font stacks only, no external fonts, no scripts. Animation is SVG-internal CSS
and switches off under prefers-reduced-motion.
"""
import math
import pathlib
import sys

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "assets")
OUT.mkdir(parents=True, exist_ok=True)

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", text="#e6edf3", muted="#8b949e",
                 faint="#21262d", grid="#1c222b", accent="#3fb950", accent2="#58a6ff",
                 chip="#1f2937", chiptext="#c9d1d9",
                 ramp=["#3fb950", "#39c5cf", "#58a6ff", "#a371f7", "#db61a2", "#f0883e"]),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#59636e",
                  faint="#eaeef2", grid="#e8ecf0", accent="#1a7f37", accent2="#0969da",
                  chip="#eef2f6", chiptext="#24292f",
                  ramp=["#1a7f37", "#0e7c86", "#0969da", "#8250df", "#bf3989", "#bc4c00"]),
}

REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tw(text, size, mono=False):
    """Rough rendered width of a string, used for chip sizing and layout."""
    return len(text) * size * (0.61 if mono else 0.56)


def hexpath(cx, cy, r, rot=-30):
    pts = [(cx + r * math.cos(math.radians(60 * k + rot)), cy + r * math.sin(math.radians(60 * k + rot)))
           for k in range(6)]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def svg(W, H, title, desc, body, style, t):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">{esc(title)}</title>
<desc id="d">{esc(desc)}</desc>
<style>
{style}
{REDUCED}
</style>
<rect width="{W}" height="{H}" rx="16" fill="{t["bg"]}"/>
{body}
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="16" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>
</svg>
'''


def chips(x, y, labels, t, size=15, h=30, gap=8, maxx=None):
    out, cx, cy = [], x, y
    for lab in labels:
        w = tw(lab, size, True) + 22
        if maxx and cx + w > maxx:
            cx, cy = x, cy + h + 8
        out.append(f'<rect x="{cx:.0f}" y="{cy}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{t["chip"]}" stroke="{t["border"]}"/>'
                   f'<text x="{cx + w / 2:.0f}" y="{cy + h / 2 + size * 0.35:.1f}" text-anchor="middle" font-family="{MONO}" '
                   f'font-size="{size}" fill="{t["chiptext"]}">{esc(lab)}</text>')
        cx += w + gap
    return "".join(out), cy + h


# ----------------------------------------------------------------------------- banner
def cluster(t, cx, cy, r):
    """Seven-node hex cluster (a control plane and six workers) with a staggered pulse."""
    out = []
    ring = [(0, 0)] + [(math.sqrt(3) * r * math.cos(math.radians(60 * k)), math.sqrt(3) * r * math.sin(math.radians(60 * k)))
                       for k in range(6)]
    for i, (dx, dy) in enumerate(ring):
        x, y = cx + dx, cy + dy
        if i == 0:
            out.append(f'<path d="{hexpath(x, y, r - 3)}" fill="{t["accent2"]}" fill-opacity=".14" stroke="{t["accent2"]}" stroke-width="2"/>')
            k = r / 44
            spokes = "".join(
                f'<line x1="{x + 9 * k * math.cos(math.radians(a)):.1f}" y1="{y + 9 * k * math.sin(math.radians(a)):.1f}" '
                f'x2="{x + 19 * k * math.cos(math.radians(a)):.1f}" y2="{y + 19 * k * math.sin(math.radians(a)):.1f}"/>'
                for a in range(-90, 270, 51))
            out.append(f'<g stroke="{t["accent2"]}" stroke-width="2.4" stroke-linecap="round" fill="none">'
                       f'<circle cx="{x}" cy="{y}" r="{9 * k:.1f}"/><circle cx="{x}" cy="{y}" r="{19 * k:.1f}"/>{spokes}</g>')
        else:
            out.append(f'<path d="{hexpath(x, y, r - 3)}" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.6"/>')
            out.append(f'<path class="node" style="animation-delay:{(i - 1) * 0.5:.1f}s" d="{hexpath(x, y, r - 3)}" '
                       f'fill="{t["accent"]}" fill-opacity=".18" stroke="{t["accent"]}" stroke-width="2"/>')
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{t["muted"]}"/>')
    return "".join(out)


def pipeline(t, x0, y, length, size):
    stages = ["commit", "plan", "apply", "observe"]
    step = length / (len(stages) - 1)
    out = [f'<line x1="{x0}" y1="{y}" x2="{x0 + length}" y2="{y}" stroke="{t["border"]}" stroke-width="3" stroke-linecap="round"/>']
    for i, s in enumerate(stages):
        x = x0 + i * step
        out.append(f'<circle cx="{x:.0f}" cy="{y}" r="8" fill="{t["bg"]}" stroke="{t["ramp"][[0, 2, 3, 5][i]]}" stroke-width="3"/>')
        out.append(f'<text x="{x:.0f}" y="{y + size + 16}" text-anchor="middle" font-family="{MONO}" font-size="{size}" fill="{t["muted"]}">{s}</text>')
    out.append(f'<circle class="travel" cx="{x0}" cy="{y}" r="6" fill="{t["accent"]}"/>')
    return "".join(out), length


BANNER_DESC = ("Ashish Sharma, Platform and DevOps Engineer. AWS, Azure, Kubernetes and Terraform, 7+ years. "
               "Illustrated with a seven-node Kubernetes-style cluster and a commit, plan, apply, observe pipeline.")


def banner_style(L):
    return f""".cur {{ animation: blink 1.1s steps(1) infinite; }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
.node {{ opacity: 0; animation: pulse 3s ease-in-out infinite; }}
@keyframes pulse {{ 0%, 100% {{ opacity: 0; }} 15% {{ opacity: 1; }} 45% {{ opacity: 0; }} }}
.travel {{ animation: travel 4s cubic-bezier(.45,0,.55,1) infinite; }}
@keyframes travel {{ 0% {{ transform: translateX(0); opacity: 0; }} 8% {{ opacity: 1; }} 92% {{ opacity: 1; }} 100% {{ transform: translateX({L}px); opacity: 0; }} }}"""


def dots(t, W, H):
    return (f'<defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse">'
            f'<circle cx="2" cy="2" r="1.4" fill="{t["grid"]}"/></pattern></defs>'
            f'<rect width="{W}" height="{H}" rx="16" fill="url(#g)"/>')


def banner(t):
    W, H = 1200, 340
    pipe, L = pipeline(t, 838, 284, 290, 16)
    body = f'''{dots(t, W, H)}
<rect x="56" y="70" width="6" height="204" rx="3" fill="{t["accent"]}"/>
<g font-family="{SANS}">
<text x="88" y="100" font-family="{MONO}" font-size="22" fill="{t["muted"]}"><tspan fill="{t["accent"]}">$</tspan> whoami<tspan class="cur" fill="{t["accent"]}"> ▍</tspan></text>
<text x="84" y="184" font-size="82" font-weight="700" letter-spacing="-1.5" fill="{t["text"]}">Ashish Sharma</text>
<text x="88" y="232" font-size="34" font-weight="600" fill="{t["accent2"]}">Platform &amp; DevOps Engineer</text>
<text x="88" y="272" font-family="{MONO}" font-size="21" fill="{t["muted"]}">AWS · Azure · Kubernetes · Terraform · 7+ years</text>
</g>
{cluster(t, 983, 136, 42)}
{pipe}'''
    return svg(W, H, "Ashish Sharma — Platform & DevOps Engineer", BANNER_DESC, body, banner_style(L), t)


def banner_m(t):
    W, H = 800, 560
    pipe, L = pipeline(t, 80, 470, 600, 24)
    body = f'''{dots(t, W, H)}
{cluster(t, 650, 120, 32)}
<g font-family="{SANS}">
<text x="56" y="100" font-family="{MONO}" font-size="30" fill="{t["muted"]}"><tspan fill="{t["accent"]}">$</tspan> whoami<tspan class="cur" fill="{t["accent"]}"> ▍</tspan></text>
<text x="50" y="262" font-size="88" font-weight="700" letter-spacing="-1.5" fill="{t["text"]}">Ashish Sharma</text>
<text x="56" y="318" font-size="40" font-weight="600" fill="{t["accent2"]}">Platform &amp; DevOps Engineer</text>
<text x="56" y="370" font-family="{MONO}" font-size="28" fill="{t["muted"]}">AWS · Azure · Kubernetes</text>
<text x="56" y="408" font-family="{MONO}" font-size="28" fill="{t["muted"]}">Terraform · 7+ years</text>
</g>
{pipe}'''
    return svg(W, H, "Ashish Sharma — Platform & DevOps Engineer", BANNER_DESC, body, banner_style(L), t)


# ----------------------------------------------------------------------------- numbers
# Counted by hand from the default branches of the public repos on 2026-11-07.
NUMBERS = [
    ("6", "Terraform modules", "scheduler · budget-alerts", "java-webapp · eks-cluster · …"),
    ("6", "pipeline definitions", "4 GitHub Actions workflows", "2 Azure DevOps pipelines"),
    ("26", "automated tests", "14 pytest · 7 terraform test", "5 JUnit"),
    ("0", "cloud keys in CI", "deploys sign in with OIDC;", "checks need no credentials"),
]
NUMBERS_DESC = ("By the numbers, counted from the public repositories: 6 Terraform modules; 6 pipeline definitions "
                "(4 GitHub Actions workflows and 2 Azure DevOps pipelines); 26 automated tests (14 pytest, 7 terraform "
                "test runs, 5 JUnit); 0 cloud keys stored in CI, because deploys sign in with OIDC and checks run without credentials.")


def numbers(t):
    W, H = 1200, 196
    cw, gap, x0 = 270, 20, 30
    out = []
    for i, (n, lab, s1, s2) in enumerate(NUMBERS):
        x = x0 + i * (cw + gap)
        c = t["ramp"][[0, 2, 3, 5][i]]
        out.append(f'''<rect x="{x}" y="24" width="{cw}" height="148" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>
<rect x="{x}" y="44" width="4" height="54" rx="2" fill="{c}"/>
<text x="{x + 24}" y="94" font-size="58" font-weight="700" fill="{c}" letter-spacing="-1">{n}</text>
<text x="{x + 24 + tw(n, 58) + 14:.0f}" y="88" font-size="18" font-weight="600" fill="{t["text"]}">{esc(lab)}</text>
<text x="{x + 24}" y="128" font-family="{MONO}" font-size="13.5" fill="{t["muted"]}">{esc(s1)}</text>
<text x="{x + 24}" y="150" font-family="{MONO}" font-size="13.5" fill="{t["muted"]}">{esc(s2)}</text>''')
    return svg(W, H, "By the numbers", NUMBERS_DESC, f'<g font-family="{SANS}">{"".join(out)}</g>', "", t)


def numbers_m(t):
    W, H = 800, 520
    cw, ch = 360, 220
    out = []
    for i, (n, lab, s1, s2) in enumerate(NUMBERS):
        x = 28 + (i % 2) * (cw + 24)
        y = 28 + (i // 2) * (ch + 24)
        c = t["ramp"][[0, 2, 3, 5][i]]
        out.append(f'''<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="14" fill="{t["panel"]}" stroke="{t["border"]}"/>
<rect x="{x}" y="{y + 30}" width="5" height="70" rx="2.5" fill="{c}"/>
<text x="{x + 28}" y="{y + 96}" font-size="78" font-weight="700" fill="{c}" letter-spacing="-1">{n}</text>
<text x="{x + 28}" y="{y + 146}" font-size="27" font-weight="600" fill="{t["text"]}">{esc(lab)}</text>
<text x="{x + 28}" y="{y + 184}" font-family="{MONO}" font-size="18" fill="{t["muted"]}">{esc(s1)}</text>''')
    return svg(W, H, "By the numbers", NUMBERS_DESC, f'<g font-family="{SANS}">{"".join(out)}</g>', "", t)


# ----------------------------------------------------------------------------- work map
STAGES = [
    ("01", "Code", ["Git + pull-request review", "plan read before apply"], "every repo"),
    ("02", "CI / CD", ["Actions · GitLab CI · Azure DevOps", "OIDC, approval-gated apply"], "azure-java · eks-observability"),
    ("03", "Infrastructure as Code", ["Terraform modules, remote state", "tflint · checkov · gitleaks"], "all Terraform repos"),
    ("04", "Cloud", ["AWS: EKS · Lambda · RDS · IAM", "Azure: App Service · Key Vault"], "aws-os-eks-logs · azure-java"),
    ("05", "Observability", ["Prometheus · Grafana", "Fluent Bit → OpenSearch, SAML"], "eks-observability · aws-os-eks-logs"),
    ("06", "FinOps", ["AWS Budgets + SNS alerts", "scheduled EC2 / RDS stop-start"], "cost-optimisation-terraform"),
]
MAP_DESC = ("A six-stage loop. 01 Code in Git with pull-request review. 02 CI/CD on GitHub Actions, GitLab CI and Azure "
            "DevOps with OIDC and an approval-gated apply. 03 Terraform modules and remote state, gated by tflint, checkov "
            "and gitleaks. 04 Cloud: AWS EKS, Lambda, RDS and IAM, and Azure App Service and Key Vault. 05 Observability: "
            "Prometheus, Grafana, Fluent Bit to OpenSearch with SAML sign-in. 06 FinOps: AWS Budgets with SNS alerts and "
            "scheduled EC2 and RDS stop-start. Metrics and spend feed the next change. Each stage names the repository that shows it.")

FLOW_STYLE = """.flow { fill: none; stroke-width: 2.4; stroke-dasharray: 7 7; animation: dash 1.4s linear infinite; }
@keyframes dash { to { stroke-dashoffset: -28; } }"""


def head(x, y, d, color):
    pts = {"r": (-9, -7, -9, 7), "l": (9, -7, 9, 7), "d": (-7, -9, 7, -9), "u": (-7, 9, 7, 9)}[d]
    return (f'<path d="M{x + pts[0]} {y + pts[1]} L{x} {y} L{x + pts[2]} {y + pts[3]}" fill="none" stroke="{color}" '
            f'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')


def stage_card(t, i, x, y, cw, ch, ts, isz, rsz):
    num, title, items, repo = STAGES[i]
    c = t["ramp"][i]
    body = "".join(f'<text x="{x + 24}" y="{y + ts + 64 + k * (isz + 12)}" font-size="{isz}" fill="{t["text"]}">{esc(it)}</text>'
                   for k, it in enumerate(items))
    return f'''<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>
<rect x="{x}" y="{y + 18}" width="4" height="{ts + 14}" rx="2" fill="{c}"/>
<text x="{x + 24}" y="{y + ts + 22}" font-family="{MONO}" font-size="{ts - 6}" font-weight="600" fill="{c}">{num}</text>
<text x="{x + 24 + tw(num, ts - 6, True) + 12:.0f}" y="{y + ts + 22}" font-size="{ts}" font-weight="650" fill="{t["text"]}">{esc(title)}</text>
{body}
<text x="{x + 24}" y="{y + ch - 18}" font-family="{MONO}" font-size="{rsz}" fill="{t["muted"]}">↳ {esc(repo)}</text>'''


def infra_map(t):
    W, H = 1200, 580
    cw, ch = 356, 180
    xs = [30, 422, 814]
    y1, y2 = 82, 370
    pos = [(xs[0], y1), (xs[1], y1), (xs[2], y1), (xs[2], y2), (xs[1], y2), (xs[0], y2)]
    cards = "".join(stage_card(t, i, x, y, cw, ch, 24, 19, 14) for i, (x, y) in enumerate(pos))
    ac = t["muted"]
    f = []
    m1, m2 = y1 + ch / 2, y2 + ch / 2
    for a, b in [(0, 1), (1, 2)]:
        f.append(f'<path class="flow" stroke="{ac}" d="M{xs[a] + cw + 6} {m1} H{xs[b] - 8}"/>' + head(xs[b] - 8, m1, "r", ac))
    xc = xs[2] + cw / 2
    f.append(f'<path class="flow" stroke="{ac}" d="M{xc} {y1 + ch + 6} V{y2 - 8}"/>' + head(xc, y2 - 8, "d", ac))
    for a, b in [(2, 1), (1, 0)]:
        f.append(f'<path class="flow" stroke="{ac}" d="M{xs[a] - 6} {m2} H{xs[b] + cw + 8}"/>' + head(xs[b] + cw + 8, m2, "l", ac))
    xf = xs[0] + cw / 2
    f.append(f'<path class="flow" stroke="{t["accent"]}" d="M{xf} {y2 - 6} V{y1 + ch + 8}"/>' + head(xf, y1 + ch + 8, "u", t["accent"]))
    f.append(f'<text x="{xf + 18}" y="{(y1 + ch + y2) / 2 + 6}" font-family="{MONO}" font-size="15" fill="{t["accent"]}">metrics + spend feed the next change</text>')
    body = f'''<g font-family="{SANS}">
<text x="30" y="52" font-size="24" font-weight="650" fill="{t["text"]}">How the work fits together</text>
<text x="1170" y="52" text-anchor="end" font-family="{MONO}" font-size="15" fill="{t["muted"]}">every box is code in a public repo</text>
{"".join(f)}
{cards}
</g>'''
    return svg(W, H, "How the work fits together", MAP_DESC, body, FLOW_STYLE, t)


def infra_map_m(t):
    W = 800
    cw, ch, gap = 680, 200, 46
    x, y0 = 92, 110
    H = y0 + 6 * ch + 5 * gap + 40
    cards, f = [], []
    ac = t["muted"]
    for i in range(6):
        y = y0 + i * (ch + gap)
        cards.append(stage_card(t, i, x, y, cw, ch, 34, 28, 21))
        if i < 5:
            xm = x + cw / 2
            f.append(f'<path class="flow" stroke="{ac}" d="M{xm} {y + ch + 6} V{y + ch + gap - 8}"/>' + head(xm, y + ch + gap - 8, "d", ac))
    ytop, ybot = y0 + ch / 2, y0 + 5 * (ch + gap) + ch / 2
    f.append(f'<path class="flow" stroke="{t["accent"]}" d="M{x - 6} {ybot} H46 V{ytop} H{x - 10}"/>' + head(x - 10, ytop, "r", t["accent"]))
    body = f'''<g font-family="{SANS}">
<text x="40" y="70" font-size="38" font-weight="650" fill="{t["text"]}">How the work fits together</text>
{"".join(f)}
{"".join(cards)}
</g>'''
    return svg(W, H, "How the work fits together", MAP_DESC, body, FLOW_STYLE, t)


# ----------------------------------------------------------------------------- repo cards
def glyph_k8s_chart(t, x, y):
    return (f'<path d="{hexpath(x, y, 30)}" fill="none" stroke="{t["accent2"]}" stroke-width="2.4"/>'
            f'<polyline points="{x - 17},{y + 9} {x - 7},{y - 2} {x + 2},{y + 5} {x + 16},{y - 12}" fill="none" stroke="{t["accent"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


def glyph_logs(t, x, y):
    lines = "".join(f'<line x1="{x - 32}" y1="{y - 14 + k * 10}" x2="{x - 8 - (k % 2) * 7}" y2="{y - 14 + k * 10}" stroke="{t["muted"]}" stroke-width="3" stroke-linecap="round"/>' for k in range(4))
    return (lines + f'<circle cx="{x + 12}" cy="{y - 2}" r="12" fill="none" stroke="{t["accent2"]}" stroke-width="3"/>'
            f'<line x1="{x + 21}" y1="{y + 7}" x2="{x + 31}" y2="{y + 17}" stroke="{t["accent2"]}" stroke-width="3.4" stroke-linecap="round"/>')


def glyph_cost(t, x, y):
    bars = "".join(f'<rect x="{x - 34 + k * 13}" y="{y + 18 - h}" width="9" height="{h}" rx="2" fill="{c}"/>'
                   for k, (h, c) in enumerate([(34, t["muted"]), (26, t["muted"]), (16, t["accent"]), (10, t["accent"])]))
    return bars + (f'<circle cx="{x + 24}" cy="{y - 8}" r="12" fill="none" stroke="{t["accent2"]}" stroke-width="2.6"/>'
                   f'<path d="M{x + 24} {y - 15} V{y - 8} L{x + 29} {y - 4}" fill="none" stroke="{t["accent2"]}" stroke-width="2.6" stroke-linecap="round"/>')


def glyph_app_db(t, x, y):
    return (f'<rect x="{x - 34}" y="{y - 20}" width="30" height="38" rx="5" fill="none" stroke="{t["accent2"]}" stroke-width="2.6"/>'
            f'<line x1="{x - 28}" y1="{y - 9}" x2="{x - 10}" y2="{y - 9}" stroke="{t["accent2"]}" stroke-width="2.4"/>'
            f'<line x1="{x}" y1="{y}" x2="{x + 6}" y2="{y}" stroke="{t["muted"]}" stroke-width="2.4"/>'
            f'<ellipse cx="{x + 22}" cy="{y - 14}" rx="13" ry="5" fill="none" stroke="{t["accent"]}" stroke-width="2.6"/>'
            f'<path d="M{x + 9} {y - 14} V{y + 12} A13 5 0 0 0 {x + 35} {y + 12} V{y - 14}" fill="none" stroke="{t["accent"]}" stroke-width="2.6"/>')


REPOS = [
    ("eks-observability-terraform", glyph_k8s_chart, "in progress",
     ["Prometheus and Grafana on EKS from one Terraform",
      "codebase across workspaces. CI on GitHub Actions",
      "and GitLab CI via OIDC; AWS Budgets guardrails."],
     ["EKS", "Prometheus", "Grafana", "OIDC", "GitLab CI"]),
    ("aws-os-eks-logs-terraform", glyph_logs, "tflint · checkov",
     ["VPC + EKS; every pod's logs shipped by a Fluent Bit",
      "DaemonSet (IRSA, no passwords) to OpenSearch,",
      "with SAML sign-in through Microsoft Entra ID."],
     ["EKS", "Fluent Bit", "OpenSearch", "IRSA", "SAML"]),
    ("cost-optimisation-terraform", glyph_cost, "tested in CI",
     ["Scheduled stop/start of tagged EC2 and RDS via",
      "EventBridge + Lambda; IAM scoped to the tag.",
      "AWS Budgets and anomaly alerts over SNS."],
     ["Lambda", "EventBridge", "Budgets", "pytest + moto", "tf test"]),
    ("azure-java-terraform", glyph_app_db, "approval-gated deploy",
     ["Spring Boot (Java 17) on App Service, PostgreSQL",
      "Flexible, secrets in Key Vault via managed identity.",
      "OIDC deploy: plan → approval → apply → smoke test."],
     ["App Service", "PostgreSQL", "Key Vault", "OIDC", "Azure DevOps"]),
]


def repo_card(t, idx):
    name, glyph, status, lines, tags = REPOS[idx]
    W, H = 600, 300
    c = t["ramp"][[2, 1, 0, 3][idx]]
    desc = "".join(f'<text x="30" y="{126 + k * 29}" font-size="19" fill="{t["text"]}">{esc(s)}</text>' for k, s in enumerate(lines))
    chip_svg, _ = chips(30, 220, tags, t, size=14, h=30, gap=8, maxx=W - 24)
    body = f'''<path d="M0 16 A16 16 0 0 1 16 0 H{W - 16} A16 16 0 0 1 {W} 16 V6 H0 Z" fill="{c}"/>
<rect x="0" y="0" width="{W}" height="6" rx="3" fill="{c}"/>
<g font-family="{SANS}">
{glyph(t, W - 64, 62)}
<text x="30" y="52" font-family="{MONO}" font-size="14" fill="{t["muted"]}">18-ashish-sharma /</text>
<text x="30" y="86" font-family="{MONO}" font-size="25" font-weight="700" fill="{t["accent2"]}">{esc(name)}</text>
{desc}
{chip_svg}
<circle cx="36" cy="276" r="5" fill="{c}"/>
<text x="50" y="281" font-family="{MONO}" font-size="14" fill="{t["muted"]}">{esc(status)}</text>
<text x="{W - 30}" y="281" text-anchor="end" font-family="{MONO}" font-size="14" fill="{t["accent2"]}">view repo →</text>
</g>'''
    return svg(W, H, name, " ".join(lines) + " Tech: " + ", ".join(tags) + ".", body, "", t)


MOBILE_TAG = ["Prometheus + Grafana on EKS", "Pod logs → OpenSearch + SSO",
              "EC2/RDS stop-start, Budgets", "App Service + PostgreSQL"]


def repo_card_m(t, idx):
    """Narrow screens show the cards two-up at ~160 px, so this variant keeps only big text."""
    name, glyph, status, lines, tags = REPOS[idx]
    W, H = 600, 300
    c = t["ramp"][[2, 1, 0, 3][idx]]
    head_, tail = name.rsplit("-terraform", 1)[0], "-terraform"
    body = f'''<rect x="0" y="0" width="{W}" height="10" rx="5" fill="{c}"/>
<g font-family="{SANS}">
<text x="34" y="104" font-family="{MONO}" font-size="44" font-weight="700" fill="{t["accent2"]}">{esc(head_)}</text>
<text x="34" y="156" font-family="{MONO}" font-size="44" font-weight="700" fill="{t["muted"]}">{tail}</text>
<text x="34" y="232" font-size="35" font-weight="500" fill="{t["text"]}">{esc(MOBILE_TAG[idx])}</text>
</g>'''
    return svg(W, H, name, " ".join(lines) + " Tech: " + ", ".join(tags) + ".", body, "", t)


# ----------------------------------------------------------------------------- certifications
CERTS = [
    ("aws", "AWS Certified DevOps Engineer", "Professional", "Amazon Web Services"),
    ("k8s", "Certified Kubernetes Administrator", "CKA", "CNCF · The Linux Foundation"),
    ("k8s", "Certified Kubernetes Security Specialist", "CKS", "CNCF · The Linux Foundation"),
    ("gpu", "NVIDIA-Certified Associate", "AI Infrastructure and Operations", "NVIDIA"),
]
CERT_DESC = ("Certifications: AWS Certified DevOps Engineer – Professional (Amazon Web Services); Certified Kubernetes "
             "Administrator, CKA, and Certified Kubernetes Security Specialist, CKS (CNCF and The Linux Foundation); "
             "NVIDIA-Certified Associate: AI Infrastructure and Operations (NVIDIA).")


def cert_icon(t, kind, x, y, s):
    """Simple marks drawn here, not vendor logos."""
    if kind == "aws":
        return (f'<path d="{hexpath(x, y - s * .22, s * .5)}" fill="none" stroke="{t["text"]}" stroke-width="{s * .1:.1f}"/>'
                f'<path d="M{x - s * .95} {y + s * .35} Q{x} {y + s * 1.0} {x + s * .95} {y + s * .35}" fill="none" stroke="#f0883e" stroke-width="{s * .15:.1f}" stroke-linecap="round"/>'
                f'<path d="M{x + s * .55} {y + s * .2} L{x + s * .98} {y + s * .32} L{x + s * .78} {y + s * .7}" fill="none" stroke="#f0883e" stroke-width="{s * .13:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "k8s":
        spokes = "".join(f'<line x1="{x}" y1="{y}" x2="{x + s * .62 * math.cos(math.radians(a)):.1f}" y2="{y + s * .62 * math.sin(math.radians(a)):.1f}"/>'
                         for a in range(-90, 270, 51))
        return (f'<path d="{hexpath(x, y, s, -90)}" fill="#326ce5"/>'
                f'<g stroke="#ffffff" stroke-width="{s * .1:.1f}" stroke-linecap="round" fill="none"><circle cx="{x}" cy="{y}" r="{s * .42:.1f}"/>{spokes}</g>')
    pins = ""
    for k in range(3):
        px = x - s * .45 + k * s * .45
        pins += (f'<line x1="{px:.1f}" y1="{y - s:.1f}" x2="{px:.1f}" y2="{y - s * .7:.1f}" stroke="#76b900" stroke-width="{s * .1:.1f}" stroke-linecap="round"/>'
                 f'<line x1="{px:.1f}" y1="{y + s * .7:.1f}" x2="{px:.1f}" y2="{y + s:.1f}" stroke="#76b900" stroke-width="{s * .1:.1f}" stroke-linecap="round"/>')
    return (f'<rect x="{x - s * .7}" y="{y - s * .7}" width="{s * 1.4}" height="{s * 1.4}" rx="{s * .2}" fill="none" stroke="#76b900" stroke-width="{s * .13:.1f}"/>'
            + pins + f'<rect x="{x - s * .3}" y="{y - s * .3}" width="{s * .6}" height="{s * .6}" rx="{s * .08}" fill="#76b900"/>')


def certs(t):
    W, H = 1200, 270
    cw, ch = 555, 100
    out = []
    for i, (kind, l1, l2, issuer) in enumerate(CERTS):
        x = 30 + (i % 2) * (cw + 30)
        y = 30 + (i // 2) * (ch + 20)
        line = {"aws": f"{l1} – {l2}", "k8s": f"{l1} ({l2})", "gpu": f"{l1}:"}[kind]
        sub = f"{l2} · {issuer}" if kind == "gpu" else issuer
        out.append(f'''<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>
{cert_icon(t, kind, x + 50, y + 50, 24)}
<text x="{x + 96}" y="{y + 44}" font-size="19" font-weight="650" fill="{t["text"]}">{esc(line)}</text>
<text x="{x + 96}" y="{y + 72}" font-family="{MONO}" font-size="14" fill="{t["muted"]}">{esc(sub)}</text>''')
    return svg(W, H, "Certifications", CERT_DESC, f'<g font-family="{SANS}">{"".join(out)}</g>', "", t)


def certs_m(t):
    W = 800
    ch, gap = 150, 20
    H = 28 + 4 * ch + 3 * gap + 28
    out = []
    for i, (kind, l1, l2, issuer) in enumerate(CERTS):
        y = 28 + i * (ch + gap)
        out.append(f'''<rect x="28" y="{y}" width="{W - 56}" height="{ch}" rx="14" fill="{t["panel"]}" stroke="{t["border"]}"/>
{cert_icon(t, kind, 96, y + ch / 2, 34)}
<text x="160" y="{y + 52}" font-size="29" font-weight="650" fill="{t["text"]}">{esc(l1)}</text>
<text x="160" y="{y + 90}" font-size="27" font-weight="500" fill="{t["accent2"]}">{esc(l2)}</text>
<text x="160" y="{y + 126}" font-family="{MONO}" font-size="21" fill="{t["muted"]}">{esc(issuer)}</text>''')
    return svg(W, H, "Certifications", CERT_DESC, f'<g font-family="{SANS}">{"".join(out)}</g>', "", t)


# ----------------------------------------------------------------------------- avatar (not used by the README)
def avatar(t):
    W = 500
    parts = []
    for k in range(6):
        a = math.radians(60 * k - 90)
        x, y = 250 + 190 * math.cos(a), 250 + 190 * math.sin(a)
        parts.append(f'<line x1="{250 + 132 * math.cos(a):.1f}" y1="{250 + 132 * math.sin(a):.1f}" x2="{250 + 166 * math.cos(a):.1f}" y2="{250 + 166 * math.sin(a):.1f}" stroke="{t["border"]}" stroke-width="3"/>')
        parts.append(f'<path d="{hexpath(x, y, 24, -90)}" fill="{t["panel"]}" stroke="{t["ramp"][k]}" stroke-width="3.5"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}" role="img" aria-label="AS">
<rect width="{W}" height="{W}" fill="{t["bg"]}"/>
{"".join(parts)}
<path d="{hexpath(250, 250, 128, -90)}" fill="{t["panel"]}" stroke="{t["accent2"]}" stroke-width="5"/>
<text x="250" y="282" text-anchor="middle" font-family="{SANS}" font-size="104" font-weight="700" letter-spacing="-2" fill="{t["text"]}">AS</text>
<rect x="200" y="304" width="100" height="7" rx="3.5" fill="{t["accent"]}"/>
</svg>
'''


if __name__ == "__main__":
    for mode, t in THEMES.items():
        files = {
            f"banner-{mode}.svg": banner(t), f"banner-m-{mode}.svg": banner_m(t),
            f"numbers-{mode}.svg": numbers(t), f"numbers-m-{mode}.svg": numbers_m(t),
            f"infra-map-{mode}.svg": infra_map(t), f"infra-map-m-{mode}.svg": infra_map_m(t),
            f"certs-{mode}.svg": certs(t), f"certs-m-{mode}.svg": certs_m(t),
        }
        for i, (name, *_rest) in enumerate(REPOS):
            files[f"card-{name}-{mode}.svg"] = repo_card(t, i)
            files[f"card-m-{name}-{mode}.svg"] = repo_card_m(t, i)
        for fn, content in files.items():
            (OUT / fn).write_text(content)
    if len(sys.argv) > 2:
        pathlib.Path(sys.argv[2]).write_text(avatar(THEMES["dark"]))
    print("ok")
