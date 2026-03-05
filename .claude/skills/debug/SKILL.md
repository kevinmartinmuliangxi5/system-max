---
name: debug
description: Systematic debugging assistant for this Windows/WSL project. Use when encountering errors, broken features, API failures, or unexpected behavior. Triggers on "debug", "fix this error", "why is this failing", "broken", or any error message.
argument-hint: [error description or paste error message]
---

# Debug Skill

Systematic debugging for this Windows/WSL Python/React project.

## Step 1: Environment Check (always first)

Before touching code, confirm:
- Shell context: Git Bash, WSL, or cmd/PowerShell?
- Paths: forward slashes or backslashes in the error?
- API keys: if auth error (401/403/429), verify key and quota before any code change
- MCP servers: if MCP-related, check installation and PATH

## Step 2: Classify the Error

| Type | Signals | First Action |
|------|---------|--------------|
| Environment | Path errors, `command not found`, wrong shell | Fix env before code |
| Auth/API | 401, 403, 429 | Confirm key validity first |
| Logic | Wrong output, assertion fails | Read the relevant file |
| Config | Missing env var, wrong JSON | Check config files |
| MCP | Server won't connect | Check install → PATH → firewall |

## Step 3: Two-Strike Rule

- **Attempt 1**: Apply minimal fix based on error classification
- **Attempt 2**: If attempt 1 fails, try a fundamentally different approach (not a variation)
- **After 2 failures**: Stop. Ask user for more context or propose a completely different strategy. Do not try a third variation of the same approach.

## Step 4: Fix Sequence

1. Read the failing file first — never propose changes to unread code
2. Apply the minimal change needed
3. Verify the fix resolves the root cause, not just the symptom
4. If touching Windows paths: always use forward slashes, quote paths with spaces

## Windows/WSL Checklist

- [ ] Paths use forward slashes (`/`)
- [ ] Shell command uses correct interpreter (WSL `bash` vs Git Bash)
- [ ] `npx` commands verified to work on Windows
- [ ] Environment variables set in the correct shell profile

## API Error Checklist

- [ ] Key is present in `.env` or environment
- [ ] Key has not expired
- [ ] Rate limit / quota not exceeded
- [ ] Correct endpoint URL (no trailing slash issues)

## Output Format

After each attempt, report:
```
Attempt N: [what was tried]
Result: [success / failed — reason]
Next: [different strategy OR ask user for context]
```
