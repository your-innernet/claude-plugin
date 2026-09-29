"""the package is not done until this holds.

every manifest parses, the plugin versions agree, every url is the one door, the
listing fits each directory's caps, and the skills name only tools the live
server serves (read from https://innernet.live/api/v1). pass --offline to skip
that last, networked check.
"""
import json, pathlib, re, sys, urllib.request

root = pathlib.Path(__file__).resolve().parent.parent
URL = "https://innernet.live/api/mcp"
bad = []


def load(p):
    try:
        return json.loads((root / p).read_text())
    except Exception as e:
        bad.append(f"{p}: {e}")
        return {}


claude = load(".claude-plugin/plugin.json")
load(".claude-plugin/marketplace.json")
codex = load(".codex-plugin/plugin.json")
market = load(".agents/plugins/marketplace.json")
cursor = load(".cursor-plugin/plugin.json")
gemini = load("gemini-extension.json")
server = load("server.json")
mcp = load(".mcp.json")

# one version for every plugin manifest
versions = {"claude": claude.get("version"), "codex": codex.get("version"),
            "cursor": cursor.get("version"), "gemini": gemini.get("version")}
if len(set(versions.values())) != 1:
    bad.append(f"plugin versions disagree: {versions}")
for name, m in [("claude", claude), ("codex", codex), ("cursor", cursor), ("gemini", gemini)]:
    if m.get("name") != "innernet":
        bad.append(f"{name}: name must stay 'innernet' (install commands depend on it)")

# one door, url only — sign-in is OAuth, never a key in a file
entry = mcp.get("mcpServers", {}).get("innernet", {})
if entry.get("url") != URL or entry.get("type", "http") != "http" or "command" in entry:
    bad.append(f".mcp.json: innernet must be {{type: http, url: {URL}}}")
if gemini.get("mcpServers", {}).get("innernet", {}).get("httpUrl") != URL:
    bad.append(f"gemini-extension.json: innernet httpUrl must be {URL}")
if [r.get("url") for r in server.get("remotes", [])] != [URL]:
    bad.append(f"server.json: remotes must be exactly {URL}")
for p in [".mcp.json", "gemini-extension.json", "server.json"]:
    if re.search(r"innernet_[0-9a-f]{8}|Bearer", (root / p).read_text()):
        bad.append(f"{p}: carries a credential")

# the registry entry
if len(server.get("description", "")) > 100:
    bad.append("server.json: description is over 100 characters")
if not re.fullmatch(r"\d+\.\d+\.\d+", str(server.get("version", ""))):
    bad.append("server.json: version is not x.y.z")

# the codex / chatgpt listing and its caps
iface = codex.get("interface", {})
for k in ["displayName", "shortDescription", "longDescription", "developerName", "category",
          "websiteURL", "privacyPolicyURL", "termsOfServiceURL"]:
    if not iface.get(k):
        bad.append(f"codex interface.{k} is missing")
for k in ["websiteURL", "privacyPolicyURL", "termsOfServiceURL"]:
    if not str(iface.get(k, "")).startswith("https://innernet.live"):
        bad.append(f"codex interface.{k} is not on innernet.live")
if len(iface.get("displayName", "")) > 30:
    bad.append("codex interface.displayName is over 30 characters")
if len(iface.get("longDescription", "")) > 2000:
    bad.append("codex interface.longDescription is over 2000 characters")
prompts = iface.get("defaultPrompt", [])
if len(prompts) > 3 or any(len(p) > 128 for p in prompts):
    bad.append("codex interface.defaultPrompt: at most 3, each at most 128 characters")
assets = [iface.get("composerIcon"), iface.get("logo"), *iface.get("screenshots", [])]
for a in assets + [f"./{cursor.get('logo', '')}"]:
    if not a or not re.fullmatch(r"\./assets/[^/]+\.png", a) or not (root / a).is_file():
        bad.append(f"asset missing or not a ./assets/*.png: {a}")
for name, m in [("codex", codex), ("cursor", cursor)]:
    for k in ["skills", "mcpServers"]:
        v = m.get(k)
        if isinstance(v, str) and (not v.startswith("./") or not (root / v).exists()):
            bad.append(f"{name}.{k} points at a missing path: {v}")
plug = next((p for p in market.get("plugins", []) if p.get("name") == "innernet"), {})
if plug.get("source", {}).get("path") != "./" or not plug.get("policy", {}).get("authentication"):
    bad.append(".agents/plugins/marketplace.json: innernet must be listed at ./ with a policy")

# skills
skills = sorted(d for d in (root / "skills").iterdir() if d.is_dir())
if {d.name for d in skills} < {"innernet", "innernet-handoff"}:
    bad.append("skills: innernet and innernet-handoff must both ship")
named = set()
for d in skills:
    md = (d / "SKILL.md").read_text()
    fm = re.match(r"^---\n([\s\S]*?)\n---\n", md)
    if not fm or not re.search(rf"^name: {re.escape(d.name)}$", fm.group(1), re.M):
        bad.append(f"{d.name}: frontmatter name must be the folder name")
    desc = re.search(r"^description: (.+)$", fm.group(1), re.M).group(1) if fm else ""
    if len(desc) < 40 or not re.search(r"\bUse (when|at)\b", desc):
        bad.append(f"{d.name}: description must say when to use it")
    if not re.search(r"never ask[^.]*paste", md, re.I):
        bad.append(f"{d.name}: must tell the model never to ask for a pasted key")
    yaml = (d / "agents" / "openai.yaml").read_text() if (d / "agents" / "openai.yaml").exists() else ""
    for want in ['type: "mcp"', 'value: "innernet"', 'transport: "streamable_http"', f'url: "{URL}"']:
        if want not in yaml:
            bad.append(f"{d.name}/agents/openai.yaml: missing {want}")
    named |= set(re.findall(r"\binnernet_[a-z_]+\b", md + (root / "GEMINI.md").read_text()))

# the skills name only tools the live server serves
if "--offline" not in sys.argv:
    try:
        with urllib.request.urlopen("https://innernet.live/api/v1", timeout=20) as r:
            served = set(re.findall(r"\binnernet_[a-z_]+\b", r.read().decode()))
        missing = sorted(named - served)
        if not served:
            bad.append("api/v1 listed no tools")
        elif missing:
            bad.append(f"skills name tools the server does not serve: {missing}")
    except Exception as e:
        bad.append(f"could not read https://innernet.live/api/v1: {e}")

if bad:
    print("\n".join(bad))
    sys.exit(1)
print(f"ok — plugin {versions['claude']} everywhere, registry {server.get('version')}, "
      f"{len(named)} tools named by the skills")
