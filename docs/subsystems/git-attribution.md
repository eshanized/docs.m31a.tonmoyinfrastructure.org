# Subsystem: Git Worktrees & Attribution

Isolates changes and guarantees audit provenance (`src/git/`).

## Git Worktree Isolation

Runs execute in dedicated worktrees under `.m31a/worktrees/run-<id>/` on branch `m31a/run/<id>`.

## Commit Trailers

Commits include structured provenance trailers:
```text
M31A-Execution-Run: 01924b12-9c48-7fa0-a110-38491823901a
M31A-Agent-Role: implementer
M31A-Model: meta/llama-3.2-11b-vision-instruct
M31A-Verification-Id: 01924b12-9d10-7aa1-b204-129038192301
```
