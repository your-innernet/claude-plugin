# innernet — the Claude plugin

the memory your AI tools share. innernet keeps one versioned memory for every
project you work on and for you — what you're building, what you decided and
why, what's in motion — and every tool you connect (Claude, ChatGPT, Codex,
Cursor, any MCP client) reads and writes the same memory.

this plugin brings that memory into Claude: one remote MCP server and two skills.
nothing runs on your machine.

```
.claude-plugin/plugin.json   the manifest
.mcp.json                    the innernet MCP server — https://innernet.live/api/mcp (OAuth sign-in)
skills/innernet/             load a project · answer from a slice · save what's worth keeping · remember you
skills/innernet-handoff/     where you left off — read at the start, written at the end
```

## install

**claude code**

```
/plugin marketplace add your-innernet/claude-plugin
/plugin install innernet@innernet
```

**claude.ai · claude desktop** — customize → plugins → add → upload plugin, and
pick the release zip. then connect innernet from the plugin's connectors tab.

the first call opens the innernet sign-in in your browser. you need a free
account at [innernet.live](https://innernet.live). never paste an api key into
a chat — the sign-in handles it.

## try

- `load my innernet project context`
- `what did we decide about pricing? check innernet`
- `where did I leave off?`
- `hand off — save my progress`

## links

- docs — https://innernet.live/docs/connect
- privacy — https://innernet.live/privacy
- terms — https://innernet.live/terms
- support — yours@innernet.live

MIT licensed.
