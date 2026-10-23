# Runtime Subsystem Manuals Overview

M31A contains 20 dedicated architectural subsystems. These manuals provide deep architectural explanations of their internal mechanics, authority ownership, data flows, and tested invariants.

## Subsystem Catalog

| Subsystem | Primary Module | Core Functionality |
|---|---|---|
| [Application Startup](startup-lifecycle) | `src/main.rs`, `src/init/` | Panic hooks, storage migration, configuration bootstrapping |
| [Configuration Engine](configuration) | `src/config/` | 8-tier precedence engine, canonical defaults, schema validation |
| [CLI & Dispatch](cli-dispatcher) | `src/cli/` | Clap hierarchy, exit code taxonomy, runtime command routing |
| [Sessions & Runtime](sessions-runtime) | `src/runtime.rs`, `src/interaction/` | `AppRuntime` composition root, interactive session persistence |
| [Agent Pool & Registry](agent-registry) | `src/agent/` | 18 built-in agent roles, supervisor, adaptive replanning |
| [Model & Providers](model-provider) | `src/model/` | NVIDIA NIM provider, SSE stream accumulator, token metrics |
| [Context & Prompts](context-prompts) | `src/context/`, `src/prompt/` | Context compaction, prompt reference catalog, token budgeting |
| [Planning & Scheduling](planning-dag) | `src/planning/`, `src/dag/` | Task decomposition, CPM critical path, cycle validation |
| [Capabilities & Tools](capabilities-tools) | `src/capability/`, `src/tools/` | 28 core tools, extended tools, provider abstraction |
| [Policy & Approvals](policy-approvals) | `src/policy/` | 4 policy decisions, multi-layer rules, interactive approvals |
| [Filesystem & Repo](filesystem-repo) | `src/repo/`, `src/change/` | AST symbol extraction, repo search, workspace mutation |
| [Process Supervision](process-sandboxing) | `src/process/`, `src/sandbox/` | PID recycling protection, spool capture, signal escalation |
| [Git & Attribution](git-attribution) | `src/git/` | Worktree isolation, commit trailers, attribution ledger |
| [Verification & Nyquist](verification-nyquist) | `src/verification/` | 7-tier verification hierarchy, evidence snapshot matching |
| [Events & Telemetry](events-telemetry) | `src/events/`, `src/telemetry/` | Broadcast event bus, distributed tracing spans |
| [Persistence & Migrations](persistence-migrations) | `src/persistence/` | SQLite WAL connection pool, migrations 001-032 |
| [Checkpoints & Recovery](checkpoints-recovery) | `src/checkpoint/` | Two-phase commit protocol, crash recovery scanner |
| [Ratatui TUI Cockpit](tui-ratatui) | `src/tui/` | 62-file terminal cockpit, read-only projection, streaming |
| [Deployment Channels](deployment-channels) | `src/deployment/` | Compile-time channel isolation (`production` vs `development`) |
