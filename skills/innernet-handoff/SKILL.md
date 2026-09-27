---
name: innernet-handoff
description: Pick up where the last session left off, and leave the next one a note. Use at the start of work on a project the user keeps in innernet, when they ask "where did I leave off", and at the end of a working session or when they say "hand off", "wrap up", or "save my progress".
---

Every innernet project has a handoff channel: a short, living "where I left off"
note, distinct from the project's maintained status. It is written by whichever
tool worked last and read by whichever tool works next — so a session started here
continues one started in Codex, Claude, or Cursor.

## at the start of a session

1. `innernet_list_projects` → the slug (or use the one the user names).
2. `innernet_handoff_read { slug }` and present it back to the user in chat, as
   "where you left off" — do not read it silently. Then continue from there.
3. If the note names open work, offer to pick it up.

## at the end of a session (or on "hand off" / "wrap up")

1. `innernet_handoff_write { slug, content }` — rewrite the note with THIS session's
   working context: what shipped, what is next, gotchas. Keep the template header
   line; keep it short and scratch-like. Every write is kept in history, so nothing is lost.
2. If the session changed what the project IS — a decision, a direction, a shipped
   piece — save that with `innernet_save_context` as well (the present, with one
   dated `## history` line for what it superseded). The handoff is scratch; the map is memory.
3. Anything the user still owes themselves: `innernet_task_create`.

## carry it quietly

Reproduce the note in chat when reading it; otherwise do not narrate the bookkeeping.
If innernet asks for authentication, the user signs in in their browser through the
plugin's connection. Never ask them to paste an API key or token into the chat.
