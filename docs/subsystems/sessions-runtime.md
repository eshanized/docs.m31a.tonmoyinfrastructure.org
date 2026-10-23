# Subsystem: Sessions & Runtime Core

The `AppRuntime` struct in `src/runtime.rs` is the authoritative composition root.

## Composition Root Responsibilities

`AppRuntime` encapsulates:
- SQLite persistence pool (`SqlitePool`)
- Event distribution bus (`Arc<BroadcastEventBus>`)
- Resolved configuration (`Arc<ResolvedConfiguration>`)
- Model provider (`Arc<dyn ModelProvider>`)
- Capability & Tool catalogs (`Arc<CapabilityRegistry>`, `Arc<ToolRegistry>`)
- Policy engine (`Arc<EffectivePolicy>`)

It provides high-level application methods:
- `execute_run(prompt, profile, ...)`
- `pause_execution(run_id)`
- `resume_execution(run_id)`
- `cancel_execution(run_id, reason)`
