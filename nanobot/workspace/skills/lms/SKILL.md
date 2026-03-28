---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

Use LMS MCP tools (`lms_*`) for live backend data.

Strategy:
- For requests about scores, pass rates, completion, groups, timeline, top learners, or health, use the matching `lms_*` tool.
- If a lab-specific metric is requested and lab is missing, call `lms_labs` first.
- If multiple labs exist, ask the user to choose one lab.
- Use lab title as default label/value unless tool output provides a better stable identifier.
- Let shared `structured-ui` decide presentation on supported channels.

Response rules:
- Keep answers concise.
- Format rates as percentages and counts as integers.
- Distinguish live backend results from unknown/unavailable data.

When asked "what can you do?":
- Explain available LMS capabilities via `lms_*` tools.
- Mention limitations clearly if backend/tool access is unavailable.
