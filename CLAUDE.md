# Claude Code Project Instructions

## Debugging Protocol
When a fix attempt fails, try a fundamentally different approach rather than variations of the same solution. After 2 failed attempts, escalate: say "I've tried two approaches without success. Let me step back — can you share more context about when this started, or should I try a completely different strategy like [alternative approach]?"

## Windows/WSL Environment
This project runs on Windows with WSL. Always use forward slashes in paths. Before any shell command, confirm whether Git Bash or WSL bash is appropriate. Avoid `npx` commands that assume Unix. If a path error occurs, check backslash vs forward slash before anything else.

## API Error Handling
When encountering 403/401/429 API errors, immediately check API key validity and rate limits before attempting any code changes. Do not proceed with implementation until API access is confirmed. Ask the user to verify the key is set and the quota is not exhausted.

## MCP Server Troubleshooting
If an MCP server fails to connect, check in order:
1. Is the server installed and in PATH?
2. Are there network or firewall issues?
3. Try a minimal test connection before complex operations.

If all three checks fail, stop and report clearly rather than spending the session on workarounds.

## Environment Pre-Check
Before starting any debugging session, confirm:
- Windows/WSL mode in use
- Relevant API keys configured and valid
- All required MCP servers connected

## Batch Related Changes
Group related fixes into a single request. Do not address UI issues, path issues, or API issues one at a time — gather the full picture first, then fix together.

## Brain Switching Protocol（主副脑切换协议）

This project uses two Claude Code instances:
- **主脑 (Main Brain)**: Official Claude Pro plan terminal — for planning, security review, architecture decisions
- **副脑 (Worker Brain)**: GLM-5 worker terminal (start_worker.bat) — for implementation, research, compounding

### Mandatory handoff steps

**Before switching FROM main brain TO worker:**
1. Run `/handoff` skill — this writes `docs/session-notes.md`
2. Confirm the file was written before switching terminals

**When worker brain takes over:**
1. Run `/resume` skill — this reads `docs/session-notes.md` and confirms context
2. Do not start work until Step 4 output is confirmed by user

### What each brain handles

| Task | Brain |
|------|-------|
| SP:writing-plans (complex requirements) | 主脑 |
| CE:/deepen-plan (research agents) | 副脑 |
| SP:subagent-driven-development (all sub-agents) | 副脑 |
| SP:test-driven-development | 副脑 |
| security-sentinel review | 主脑 |
| architecture-strategist review | 主脑 |
| style/performance/simplicity reviewers | 副脑 |
| SP:verification-before-completion | 副脑 |
| CE:/workflows:compound (Phase 7) | 主脑 (reads full session history) |
| All debugging phases 1-4 | 副脑 |

### Key rule
The filesystem is the only shared state between the two brains.
Every important decision made by main brain MUST be written to a file before switching.
