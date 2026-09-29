#!/usr/bin/env bash
# Publish innernet to the official MCP Registry (registry.modelcontextprotocol.io).
#
# Prereqs (one-time):
#   1. The verification file must be live:
#      https://innernet.live/.well-known/mcp-registry-auth
#      (served by apps/web/app/.well-known/mcp-registry-auth/route.ts — deploy first)
#   2. Ed25519 key at ~/.innernet/keys/mcp-registry-ed25519.seed.hex
#      (generated once; the public half is embedded in the well-known route)
#
# Re-run on every server.json version bump.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! command -v mcp-publisher >/dev/null 2>&1; then
  echo "installing mcp-publisher…"
  if command -v brew >/dev/null 2>&1; then
    brew install mcp-publisher
  else
    curl -L "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/').tar.gz" | tar xz mcp-publisher
    sudo mv mcp-publisher /usr/local/bin/
  fi
fi

SEED_FILE="$HOME/.innernet/keys/mcp-registry-ed25519.seed.hex"
[ -f "$SEED_FILE" ] || { echo "missing $SEED_FILE — see the README (releasing)"; exit 1; }

echo "verifying the well-known file is live…"
curl -fsS https://innernet.live/.well-known/mcp-registry-auth | grep -q 'MCPv1' \
  || { echo "https://innernet.live/.well-known/mcp-registry-auth is not live — deploy first"; exit 1; }

mcp-publisher login http --domain innernet.live --private-key "$(cat "$SEED_FILE")"
mcp-publisher publish

echo
echo "verify: curl 'https://registry.modelcontextprotocol.io/v0.1/servers?search=live.innernet'"
