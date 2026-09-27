<p align="center"><img src="assets/icon.png" alt="innernet" width="96" height="96"></p>

# innernet

the memory your AI tools share. innernet keeps one versioned memory for every
project you work on and for you — what you're building, what you decided and
why, what's in motion — and every tool you connect (Claude, ChatGPT, Codex,
Cursor, any MCP client) reads and writes that same memory. open a project in
Claude and the conversation picks up where your other tools left off.

this plugin brings that memory into Claude: the innernet connector plus two
skills that tell Claude when and how to use it.

## what's inside

- **innernet connector** — the remote MCP server at `https://innernet.live/api/mcp`.
  you sign in once through innernet's own OAuth page in your browser.
- **innernet skill** — find the project you're talking about, load it, answer
  from the part of the memory that matters, save decisions back, keep the
  project's task list current, and remember durable things about you that you
  choose to share.
- **innernet-handoff skill** — "where did I leave off?" at the start of a
  session, and a short handoff note at the end, so the next tool continues.

## use it

**claude.ai · cowork** — customize → plugins → add, then connect innernet from
the plugin's connectors tab and sign in.

**claude code**

```
/plugin marketplace add your-innernet/claude-plugin
/plugin install innernet@innernet
```

you need a free account at [innernet.live](https://innernet.live). never paste
an api key into a chat — the sign-in handles it.

try:

- "load my innernet project context"
- "what did we decide about pricing? check innernet"
- "where did I leave off?"
- "hand off — save my progress"

## data

- the plugin runs nothing on your machine: no scripts, hooks, or local servers.
  it is two markdown skills and one connector entry.
- the only destination is innernet.live. Claude sends the connector what a
  tool call carries — a project name, your question, or the text you ask it to
  save — and innernet returns what your memory holds. nothing is read from
  Claude's own memory, chat history, or files.
- saves are written to your innernet account, versioned, and visible on your
  dashboard; you can edit or delete any of it there. personal memory is gated
  by disclosure levels you set, and private facts are never returned to an AI.
- tools that change data ask before running, and the skills tell Claude to say
  what it saved.

privacy policy — https://innernet.live/privacy · terms — https://innernet.live/terms

## support

docs — https://innernet.live/docs/connect · email — yours@innernet.live

MIT licensed.
