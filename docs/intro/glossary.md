# Glossary & Core Concepts

Authoritative definitions of core terminology used across the M31A platform.

### Agent Role
A specialized LLM prompt and policy profile with constrained capabilities. Examples: `planner`, `implementer`, `verifier`, `reviewer`, `diagnostician`, `architect`.

### Autonomy Mode
The operational posture of the runtime controlling approval requirements. M31A implements 5 modes: `Safe`, `Plan`, `Assisted`, `Autonomous`, and `Unattended`.

### Capability
A typed system interface (e.g. `fs.read`, `process.exec`, `git.commit`) that tools must acquire to perform work.

### Checkpoint
A durable, content-addressed snapshot of execution state, workspace files, and artifact ledger entries committed atomically to SQLite.

### ExecutionRun
The canonical root orchestrator entity representing an autonomous task execution from intake to completion (consolidated in database migrations 030-032).

### FsArtifactStore
Content-addressed filesystem storage located in platform directories (`~/.local/share/m31a/artifacts`) storing generated diffs, test logs, and review summaries.

### Nyquist Gate
The evidence-backed completion gate enforcing that no task or execution run may transition to `Succeeded` without deterministic verification evidence.

### Policy Gate
The Layer 1 security evaluator intercepting all tool calls and classifying them into `Allow`, `Deny`, `Ask`, or `Escalate`.

### Ratatui Cockpit
The high-performance interactive terminal user interface projecting live execution state.

### Worktree Isolation
A dedicated Git worktree branch (`m31a/run/...`) created for an execution run to ensure experiments never corrupt the operator's working branch.
