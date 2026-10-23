# Request Dispatch & Composition Root

Understanding how CLI commands, interactive inputs, and background jobs enter the M31A runtime.

## The Composition Root: `AppRuntime`

`src/runtime.rs` contains the authoritative composition root: `AppRuntime`.
It wires together:
- `SqlitePool` (Persistence)
- `BroadcastEventBus` (Event distribution)
- `ResolvedConfiguration` (Authoritative config)
- `NvidiaProvider` (Model reasoning)
- `CapabilityRegistry` & `ToolRegistry` (Side-effect interfaces)
- `EffectivePolicy` (Security evaluation)
- `Scheduler` & `ExecutionEngine` (Work scheduling)

## Command Flow

```text
Operator Input (CLI / TUI)
       │
       ▼
clap::Parser / TuiInput
       │
       ▼
CliDispatcher::dispatch() ──► RuntimeCommand::RunExecution
                                        │
                                        ▼
                               AppRuntime::execute_run()
                                        │
                                        ▼
                               WorkerDispatcher / TaskGraph
```

All interactions normalize into typed `RuntimeCommand` variants (`src/cli/dispatch.rs`), guaranteeing identical semantics whether invoked from the CLI or TUI.
