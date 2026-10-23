# Core Design Principles & Runtime Authority

M31A was constructed from the ground up under 10 non-negotiable architectural invariants detailed in `AGENTS.md` and enforced by automated tests in `tests/architecture_invariants.rs`.

## The 10 Architectural Invariants

### 1. Single Crate Architecture
M31A is intentionally built as a single Rust crate (`m31a`). It does not use a Cargo workspace. Domain boundaries are enforced using Rust module visibility (`pub(crate)`) and clear architectural layering (L0 through L9).

### 2. Pure Rust Core
The core runtime, CLI, TUI, scheduler, policy engine, and tests require only the Rust toolchain (Rust 1.85+, edition 2024) and platform C libraries (SQLite via SQLx). No external runtime interpreters (Python, Node.js) or local GPU drivers are required.

### 3. Policy Supremacy
Every external side effect—filesystem modifications, command executions, git worktrees, network egress—**must** pass through the Layer 1 Policy Gate. There are no bypasses for "internal" tools, test harnesses, or system agents.

### 4. TUI is a Pure Projection
The Ratatui terminal user interface (cockpit) is strictly a read-only projection over SQLite database state and asynchronous tokio broadcast event streams. The TUI never maintains authoritative execution state. If the terminal crashes or is resized, runtime execution is completely unaffected.

### 5. Never Fake Success
M31A rejects mock returns, TODO-only implementations, or silent fallbacks. Unimplemented or blocked execution paths return explicit, strongly typed errors. A present-but-invalid configuration is a fatal startup exit (Exit Code 2), never a silent fallback to defaults.

### 6. Completion Requires Evidence
No mission, task, or execution run can transition to `Succeeded` based on an LLM claiming "I have completed the task." Completion requires deterministic execution evidence: passing compiler checks, passing test suites, and cryptographic SHA-256 artifact verification against pre-execution repository baselines.

### 7. Bounded Retries & Execution
Every loop, retry counter, background process, and memory allocation is strictly bounded. The decommissioned token budget system has been replaced by concrete runtime limits:
- Maximum steps per agent role (default: 20-30 steps)
- Step stall timeouts (default: 60-90 seconds)
- Task wall-clock timeouts (default: 300-900 seconds)
- Action failure thresholds (default: 3 consecutive failures trigger diagnostic recovery)
- Global and per-mission job concurrency caps

### 8. Real, Non-Blocking Cancellation
All asynchronous operations and supervised processes support instantaneous cancellation via Tokio `CancellationToken` and POSIX signal escalation (SIGINT → SIGTERM → SIGKILL).

### 9. External Data is Untrusted
All data entering the runtime from the outside world—prompt inputs, repository contents, model responses, web search results—is treated as untrusted. Payloads pass through strict sanitization, UTF-8 normalization, and trust boundaries before context compilation.

### 10. Downward Dependency Discipline
Architectural layers (L0 Kernel through L9 CLI/TUI) depend downward only:
- Lower layers (e.g. L1 Security) may **never** import or depend on higher layers (e.g. L8 Autonomy, L9 CLI).
- Upward communication occurs exclusively via asynchronous event publishing or typed trait interfaces.
