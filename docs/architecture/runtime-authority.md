# Runtime Authority & State Machine

The core architectural invariant of M31A is: **The model proposes. The runtime decides.**

## Authoritative vs Projected State

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       AUTHORITATIVE STATE (Layer 0)                         │
│   SQLite Database  •  FsArtifactStore  •  StorageLayout  •  Git Commits     │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Async Event Stream & SQLx Queries
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PROJECTED READ-ONLY STATE (Layer 9)                      │
│   Ratatui Cockpit Surfaces  •  CLI Stdout / JSON  •  TUI Viewports          │
└─────────────────────────────────────────────────────────────────────────────┘
```

The LLM is a stateless reasoning engine. It does not own execution state, task graphs, or verification results.
- **Authoritative State**: Stored in SQLite tables (`execution_runs`, `tasks`, `checkpoints`, `artifacts`, `verification_checks`).
- **Projected State**: Rendered in the Ratatui cockpit or CLI output. A crash or termination of the TUI has zero effect on the validity of authoritative database records.

## State Transition Matrices

M31A enforces formal state transition matrices in `src/state_machine/`:

### ExecutionRun Status Transitions
`Pending → Starting → Running → Paused (or Failed, Cancelled) → Succeeded`
A transition to `Succeeded` requires proof of passing verification checks in SQLite.

### Task Status Transitions
`Pending → Blocked (dependencies) → Ready → Dispatched → Executing → Verifying → Succeeded (or Failed)`
