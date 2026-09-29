"""every manifest parses, the plugin versions agree, and the registry entry fits its limits."""
import json, pathlib, sys

root = pathlib.Path(__file__).resolve().parent.parent
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
load(".agents/plugins/marketplace.json")
cursor = load(".cursor-plugin/plugin.json")
gemini = load("gemini-extension.json")
server = load("server.json")
mcp = load(".mcp.json")

versions = {p: m.get("version") for p, m in
            [("claude", claude), ("codex", codex), ("cursor", cursor), ("gemini", gemini)]}
if len(set(versions.values())) != 1:
    bad.append(f"plugin versions disagree: {versions}")

url = "https://innernet.live/api/mcp"
if mcp.get("mcpServers", {}).get("innernet", {}).get("url") != url:
    bad.append(".mcp.json: innernet url is not " + url)
if gemini.get("mcpServers", {}).get("innernet", {}).get("httpUrl") != url:
    bad.append("gemini-extension.json: innernet httpUrl is not " + url)
if [r.get("url") for r in server.get("remotes", [])] != [url]:
    bad.append("server.json: remotes should be exactly " + url)
if len(server.get("description", "")) > 100:
    bad.append("server.json: description is over 100 characters")

for skill in (root / "skills").glob("*/SKILL.md"):
    if not skill.read_text().startswith("---\nname:"):
        bad.append(f"{skill.relative_to(root)}: missing frontmatter")

if bad:
    print("\n".join(bad))
    sys.exit(1)
print(f"ok — {versions['claude']} everywhere, registry {server.get('version')}")
