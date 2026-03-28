---
name: observability
description: Investigate LMS/backend incidents using logs and traces
always: true
---

When user asks "What went wrong?", "Check system health", or similar incident questions:

Investigation flow (always in this order):
1. Run `mcp_obs_logs_error_count` for a fresh narrow window (default 10 minutes, or 2 minutes for cron checks).
2. Run `mcp_obs_logs_search` scoped to LMS/backend errors:
   `_time:<window>m service.name:"Learning Management Service" severity:ERROR`
3. Extract a recent `trace_id` from matching logs when available.
4. Run `mcp_obs_traces_get` for that trace ID.
5. Return one concise explanation:
   - what failed
   - in which service/operation
   - log evidence (event/severity)
   - trace evidence (where in request path the failure appears)

Rules:
- Prefer newest evidence only; ignore stale older incidents when answering.
- Do not dump raw JSON unless explicitly requested.
- If DB failure is present but API response looks like 404 "Items not found", explicitly mention this mismatch as a likely failure-path handling bug.
