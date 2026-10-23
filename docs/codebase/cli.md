# CLI & Dispatch Layer

> **Architectural Layer:** L9 CLI / Interface  
> **Source Directory:** `src/cli`  
> **File Count:** 6 source files  

Clap 4 argument hierarchy, output formatters, exit codes, and runtime command dispatch.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [args.rs](#src-cli-args-rs) | 505 | `AgentArgs, ArtifactArgs, CapabilityArgs` | Clap 4 CLI Command &amp; Argument Hierarchy (CLI-01, CLI-02). |
| [dispatch.rs](#src-cli-dispatch-rs) | 2301 | `CliDispatcher, CliOutput, CliError` | Shared Runtime Application Command Dispatch Layer (CLI-01, CLI-04, D-1... |
| [doctor.rs](#src-cli-doctor-rs) | 541 | `DeploymentProbe, DoctorReport, DoctorRunner` | Modular Doctor Environment Diagnostics Probes (CLI-01, D-20). |
| [exit_codes.rs](#src-cli-exit_codes-rs) | 68 | `M31aExitCode` | Stable Documented Exit Code Taxonomy (CLI-03, D-18). |
| [mod.rs](#src-cli-mod-rs) | 17 | `Functions/Traits` | CLI Command Suite &amp; Application Runtime Interface (CLI-01–CLI-04). |
| [output.rs](#src-cli-output-rs) | 89 | `NdjsonStreamWriter, TerminalFrame, CliStreamMessage` | NDJSON Streaming Output &amp; Envelope Formatting (CLI-02, D-18). |

---

### `src/cli/args.rs` {#src-cli-args-rs}

- **Source Link:** [`src/cli/args.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/cli/args.rs)
- **Lines of Code:** 505 (13952 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Clap 4 CLI Command &amp; Argument Hierarchy (CLI-01, CLI-02).

#### Types & Trait Declarations
- **Structs (19):** `AgentArgs`, `ArtifactArgs`, `CapabilityArgs`, `CheckpointArgs`, `Cli`, `ConfigArgs`, `DeploymentArgs`, `DoctorArgs`, `EvalArgs`, `ExecutionArgs`, `InitArgs`, `PolicyArgs`, `RollbackArgs`, `RunArgs`, `SessionArgs`, `TaskArgs`, `TelemetryArgs`, `UpdateArgs`, `VersionArgs`
- **Enums (13):** `AgentCommands`, `ArtifactCommands`, `CapabilityCommands`, `CheckpointCommands`, `Commands`, `ConfigCommands`, `EvalCommands`, `ExecutionCommands`, `OutputFormat`, `PolicyCommands`, `SessionCommands`, `TaskCommands`, `TelemetryCommands`

---

### `src/cli/dispatch.rs` {#src-cli-dispatch-rs}

- **Source Link:** [`src/cli/dispatch.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/cli/dispatch.rs)
- **Lines of Code:** 2301 (100944 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Shared Runtime Application Command Dispatch Layer (CLI-01, CLI-04, D-18).

#### Types & Trait Declarations
- **Structs (2):** `CliDispatcher`, `CliOutput`
- **Enums (2):** `CliError`, `RuntimeCommand`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn success(text: impl Into<String>, data: serde_json::Value) -> Self;
// pub
fn with_exit_code(mut self, code: i32) -> Self;
// private
fn from(r: crate::telemetry::TelemetryInspectionReport) -> Self;
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_policy_gate(mut self, gate: Arc<dyn PolicyGate>) -> Self;
// pub
fn with_capabilities(mut self, reg: Arc<CapabilityRegistry>) -> Self;
// pub
fn with_event_bus(mut self, bus: Arc<BroadcastEventBus>) -> Self;
// pub
fn with_pool(mut self, pool: SqlitePool) -> Self;
// pub
fn with_mission_repo(mut self, repo: Arc<dyn MissionRepository>) -> Self;
// pub
fn with_execution_run_repo(mut self, repo: Arc<dyn ExecutionRunRepository>) -> Self;
// pub
fn with_checkpoint_manager(mut self, mgr: Arc<CheckpointManager>) -> Self;
// pub
fn with_artifact_store(mut self, store: Arc<dyn ArtifactStore>) -> Self;
// pub
fn with_approval_coordinator(mut self, coord: Arc<ApprovalCoordinator>) -> Self;
// pub
fn with_runtime(mut self, rt: Arc<crate::runtime::AppRuntime>) -> Self;
```

---

### `src/cli/doctor.rs` {#src-cli-doctor-rs}

- **Source Link:** [`src/cli/doctor.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/cli/doctor.rs)
- **Lines of Code:** 541 (18069 bytes)

#### Primary Responsibility
Modular Doctor Environment Diagnostics Probes (CLI-01, D-20).

#### Types & Trait Declarations
- **Structs (11):** `DeploymentProbe`, `DoctorReport`, `DoctorRunner`, `EnvironmentProbe`, `GitProbe`, `ModelsProbe`, `NetworkMcpProbe`, `PlatformProbe`, `ProbeResult`, `SandboxProbe`, `StorageProbe`
- **Enums (2):** `ProbeCategory`, `ProbeStatus`
- **Traits (1):** `DoctorProbe`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// pub
fn ok(category: ProbeCategory,
        name: impl Into<String>,
        message: impl Into<String>,) -> Self;
// pub
fn warning(category: ProbeCategory,
        name: impl Into<String>,
        message: impl Into<String>,
        remedia;
// pub
fn error(category: ProbeCategory,
        name: impl Into<String>,
        message: impl Into<String>,
        remediati;
// private
fn category(&self) -> ProbeCategory;
// private
fn name(&self) -> &str;
// private
async fn check(&self) -> ProbeResult;
// private
fn category(&self) -> ProbeCategory;
// private
fn name(&self) -> &str;
// private
async fn check(&self) -> ProbeResult;
// private
fn category(&self) -> ProbeCategory;
// private
fn name(&self) -> &str;
// private
async fn check(&self) -> ProbeResult;
// private
fn category(&self) -> ProbeCategory;
// private
fn name(&self) -> &str;
```

---

### `src/cli/exit_codes.rs` {#src-cli-exit_codes-rs}

- **Source Link:** [`src/cli/exit_codes.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/cli/exit_codes.rs)
- **Lines of Code:** 68 (2189 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Stable Documented Exit Code Taxonomy (CLI-03, D-18).

#### Types & Trait Declarations
- **Enums (1):** `M31aExitCode`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn as_i32(self) -> i32;
// pub
fn description(&self) -> &'static str;
// private
fn from(code: M31aExitCode) -> Self;
// private
fn from(val: i32) -> Self;
```

---

### `src/cli/mod.rs` {#src-cli-mod-rs}

- **Source Link:** [`src/cli/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/cli/mod.rs)
- **Lines of Code:** 17 (599 bytes)

#### Primary Responsibility
CLI Command Suite &amp; Application Runtime Interface (CLI-01–CLI-04).

---

### `src/cli/output.rs` {#src-cli-output-rs}

- **Source Link:** [`src/cli/output.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/cli/output.rs)
- **Lines of Code:** 89 (2370 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
NDJSON Streaming Output &amp; Envelope Formatting (CLI-02, D-18).

#### Types & Trait Declarations
- **Structs (2):** `NdjsonStreamWriter`, `TerminalFrame`
- **Enums (1):** `CliStreamMessage`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn new(writer: W) -> Self;
// pub
fn emit(&mut self, message: &CliStreamMessage) -> io::Result<()>;
// pub
fn is_sealed(&self) -> bool;
```

---
