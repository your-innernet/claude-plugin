# innernet

innernet is connected as an MCP server. it holds the user's versioned memory: one
context map per project, a personal memory about the user, and each project's task
list. every AI tool they use reads and writes the same memory.

- a project comes up → `innernet_list_projects`, then `innernet_load_project { slug }`
  and follow its `capture_protocol`.
- a specific question → `innernet_context { slug, intent }` with the ask verbatim.
  if it holds nothing, say so.
- a decision worth keeping → `innernet_save_context`. when it replaces something,
  replace it in the body and add one dated line under `## history`.
- something durable about the user → `innernet_self_capture`, and say you noted it.
- "where did I leave off?" → `innernet_handoff_read`; at the end → `innernet_handoff_write`.

say in a few words what you saved. if innernet asks for sign-in, the user signs in
in their browser — never ask them to paste an api key or token into the chat.
