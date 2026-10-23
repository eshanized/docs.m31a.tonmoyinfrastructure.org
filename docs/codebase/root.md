# Root Application & Runtime

> **Architectural Layer:** L0-L9 Composition  
> **Source Directory:** `src/`  
> **File Count:** 6 source files  

main.rs, lib.rs, error taxonomy, and authoritative AppRuntime composition root.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [error.rs](#src-error-rs) | 191 | `M31AError` | Top-level error type hierarchy for M31A.  Uses `thiserror` for domain/... |
| [lib.rs](#src-lib-rs) | 49 | `Functions/Traits` | M31 Autonomous (M31A) - Rust-native autonomous software-engineering ru... |
| [main.rs](#src-main-rs) | 589 | `CliOverrides` | M31 Autonomous (M31A) - Main Entry Point.  "The model proposes. The ru... |
| [runtime.rs](#src-runtime-rs) | 7015 | `AppRuntime, AssemblyForwarderGuard, GenesisExecutionOutcome` | Production Composition Root &amp; Application Runtime (PRD §01, SYS-01... |
| [runtime_authorities.rs](#src-runtime_authorities-rs) | 966 | `AutonomyPrecedence, CredentialResolution, ModelInvocation` | Single canonical runtime authority set (wiring remediation v0.1.1).  "... |
| [startup_progress.rs](#src-startup_progress-rs) | 364 | `StageTimer, StartupProgressReporter, StartupStageUpdate` | Structured startup-stage tracing and bounded progress protocol (P0).  ... |

---

### `src/error.rs` {#src-error-rs}

- **Source Link:** [`src/error.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/error.rs)
- **Lines of Code:** 191 (6131 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Top-level error type hierarchy for M31A.  Uses `thiserror` for domain/public error classification and `anyhow` for application glue.

#### Types & Trait Declarations
- **Enums (1):** `M31AError`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn transition(msg: impl Into<String>) -> Self;
// pub
fn persistence(msg: impl Into<String>) -> Self;
// pub
fn cancellation(msg: impl Into<String>) -> Self;
// pub
fn validation(msg: impl Into<String>) -> Self;
// pub
fn invalid_input(msg: impl Into<String>) -> Self;
// pub
fn not_found(msg: impl Into<String>) -> Self;
// pub
fn reconstruction(msg: impl Into<String>) -> Self;
// pub
fn integrity(msg: impl Into<String>) -> Self;
// pub
fn checkpoint(msg: impl Into<String>) -> Self;
// pub
fn internal(msg: impl Into<String>) -> Self;
// private
fn test_transition_error();
// private
fn test_persistence_error();
// private
fn test_cancellation_error();
// private
fn test_validation_error();
// private
fn test_not_found();
```

#### Unit Verification (10 inline tests)
Tests defined within module:
`test_transition_error`, `test_persistence_error`, `test_cancellation_error`, `test_validation_error`, `test_not_found`, `test_internal_error_from_string`, `test_internal_error_from_anyhow`, `test_error_trait_source`, `test_string_variants_have_no_source`, `test_error_chain_works`

---

### `src/lib.rs` {#src-lib-rs}

- **Source Link:** [`src/lib.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/lib.rs)
- **Lines of Code:** 49 (924 bytes)

#### Primary Responsibility
M31 Autonomous (M31A) - Rust-native autonomous software-engineering runtime.  Core principle: The model proposes. The runtime decides.

---

### `src/main.rs` {#src-main-rs}

- **Source Link:** [`src/main.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/main.rs)
- **Lines of Code:** 589 (24032 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
M31 Autonomous (M31A) - Main Entry Point.  "The model proposes. The runtime decides." (PRD §01, CLI-01, CLI-04)

#### Types & Trait Declarations
- **Structs (1):** `CliOverrides`

#### Key Functions & Signatures (3 shown)
```rust
// private
async fn main() -> Result<(), Box<dyn std::error::Error>>;
// private
fn spawn_runtime_assembly(pool: sqlx::SqlitePool,
    workspace_root: PathBuf,
    event_bus: Arc<BroadcastEventBus>,
  ;
// private
async fn run_tui_or_fallback(_dispatcher: CliDispatcher,
    workspace_root: PathBuf,
    event_bus: Arc<BroadcastEventB;
```

---

### `src/runtime.rs` {#src-runtime-rs}

- **Source Link:** [`src/runtime.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/runtime.rs)
- **Lines of Code:** 7015 (320135 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Production Composition Root &amp; Application Runtime (PRD §01, SYS-01, BLK-01, F-01).  "The model proposes. The runtime decides."  Central runtime assembling all real production subsystems: - SQLite ACID storage &amp; migrations - Bounded BroadcastEventBus - Telemetry streaming forwarder (.m31a/telemetry) - FsArtifactStore (.m31a/artifacts) - EffectivePolicy &amp; approval escalation - WorktreeManager with Git isolation - Deterministic ReportGenerator (.m31a/reports) - StartupCrashRecoveryScanner - AutonomyController 12-stage closed loop

#### Types & Trait Declarations
- **Structs (4):** `AppRuntime`, `AssemblyForwarderGuard`, `GenesisExecutionOutcome`, `MissionExecutionSummary`
- **Enums (2):** `GitFinalizationSummary`, `PlanningChoice`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn from_flags(plan: bool, no_plan: bool) -> Option<Self>;
// pub
fn prompt_question() -> &'static str;
// pub
fn is_explicit_refusal(text: &str) -> bool;
// pub
fn is_plan_governance_command(text: &str) -> bool;
// pub
fn is_explicit_planning_request(text: &str) -> bool;
// pub
fn resolve_for_request(raw_text: &str,
        explicit: Option<PlanningChoice>,
        stored: Option<PlanningChoice>,;
// pub
fn resolve_for_request_with_workspace(raw_text: &str,
        workspace_root: Option<&std::path::Path>,
        explicit;
// pub
fn classify_request_intent(raw_text: &str,
        workspace_root: Option<&std::path::Path>,) -> Option<PlanningChoice>;
// pub
fn as_str(self) -> &'static str;
// pub
fn from_str_loose(s: &str) -> Option<Self>;
// pub
fn to_upstream_plan_context(&self,
        prompt: &str,) -> crate::kernel::seams::planner::UpstreamPlanContext;
// pub
async fn new(workspace_root: impl Into<PathBuf>) -> Result<Self, M31AError>;
// pub
async fn from_pool_and_workspace(pool: SqlitePool,
        workspace_root: PathBuf,
        event_bus: Arc<BroadcastEven;
// pub
async fn from_pool_workspace_and_config(pool: SqlitePool,
        workspace_root: PathBuf,
        event_bus: Arc<Broadc;
// pub
async fn from_pool_workspace_and_config_with_progress(pool: SqlitePool,
        workspace_root: PathBuf,
        event_b;
```

---

### `src/runtime_authorities.rs` {#src-runtime_authorities-rs}

- **Source Link:** [`src/runtime_authorities.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/runtime_authorities.rs)
- **Lines of Code:** 966 (41097 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Single canonical runtime authority set (wiring remediation v0.1.1).  "The model proposes. The runtime decides."  This module is the answer to the split-brain audit (`docs/audits/WIRING-AUDIT-v0.1.1.md`): exactly ONE authoritative instance of each runtime-critical authority per runtime scope, composed ONCE at the production composition root (`AppRuntime::from_pool_workspace_and_config`) and consumed downstream by reference.  ```text configuration ↓ RuntimeAuthorities (this module: ONE per runtime scope) ↓ derived runtime services (controller, dispatcher, engines, coordinators) ↓ execution engines/controllers ↓ tool/model/policy/approval execution (single governance decision per action) ```  Mutation rule: authorities are immutable as a set. Reconfiguration builds a COMPLETE new set (`reconfigured`) and swaps it atomically; partial `with_*` mutation of related authorities is forbidden because it forks derived state (stale model schemas, stale catalog locks, stale policy bindings).

#### Types & Trait Declarations
- **Structs (6):** `AutonomyPrecedence`, `CredentialResolution`, `ModelInvocation`, `ModelInvocationContext`, `RuntimeAuthorities`, `RuntimeBinding`
- **Enums (2):** `CredentialSource`, `ModelInvocationKind`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn is_tool_free_by_default(&self) -> bool;
// pub
fn new(role: AgentRole,
        invocation_kind: ModelInvocationKind,
        autonomy_mode: AutonomyMode,) -> Self;
// pub
fn with_mission_id(mut self, mission_id: MissionId) -> Self;
// pub
fn with_task_id(mut self, task_id: TaskId) -> Self;
// pub
fn with_agent_id(mut self, agent_id: AgentId) -> Self;
// pub
fn requires_tool_free(&self) -> bool;
// pub
fn new(prompt: crate::prompt::EffectivePrompt,
        prompt_ref: crate::prompt::PromptReference,
        role: AgentRo;
// pub
fn with_mission_id(mut self, mission_id: MissionId) -> Self;
// pub
fn with_task_id(mut self, task_id: TaskId) -> Self;
// pub
fn with_agent_id(mut self, agent_id: AgentId) -> Self;
// pub
fn invocation_context(&self) -> ModelInvocationContext;
// pub
fn require_provenance(&self,) -> Result<&crate::prompt::provenance::PromptInvocationProvenance, String>;
// pub
fn is_legacy_structured_prompt(context: &str) -> bool;
// pub
fn from_profile_name(profile: Option<&str>) -> AutonomyMode;
// pub
fn from_config(config: &ResolvedConfiguration) -> AutonomyMode;
```

---

### `src/startup_progress.rs` {#src-startup_progress-rs}

- **Source Link:** [`src/startup_progress.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/startup_progress.rs)
- **Lines of Code:** 364 (13159 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Structured startup-stage tracing and bounded progress protocol (P0).  The 30s assembly deadline previously produced only `Runtime assembly timed out after 30.0s (deadline exceeded)` with no indication of the unfinished operation. This module provides:  - Stable stage names consumed by `tracing` and the TUI. - A small typed progress update carried over a bounded [`tokio::sync::watch`] channel (single latest value, never an unbounded event queue). - Timing helpers that record start/completion/elapsed per stage.  Layering: this is a low-level (L0/L8) progress type. The TUI (L9) consumes it as a projection; the runtime (L8) produces it. Lower layers never depend on TUI state.  No credentials or secret configuration values are ever included in updates or trace fields.

#### Types & Trait Declarations
- **Structs (3):** `StageTimer`, `StartupProgressReporter`, `StartupStageUpdate`
- **Enums (1):** `StageStatus`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn as_str(self) -> &'static str;
// private
fn default() -> Self;
// pub
fn new(seq: u64, stage: &str, message: impl Into<String>) -> Self;
// pub
fn with_recovery_counts(mut self, completed: usize, total: usize) -> Self;
// pub
fn progress_channel() -> (
    tokio::sync::watch::Sender<StartupStageUpdate>,
    tokio::sync::watch::Receiver<StartupS;
// pub
fn tracing_only(workspace: &str, channel: &str) -> Self;
// pub
fn with_live_channel(sender: tokio::sync::watch::Sender<StartupStageUpdate>,
        workspace: &str,
        channel: &;
// pub
fn report_stage(&mut self, stage: &str, message: impl Into<String>);
// pub
fn report_stage_with_counts(&mut self,
        stage: &str,
        message: impl Into<String>,
        completed: usize;
// pub
fn report_complete(&mut self, stage: &str, elapsed: Duration, detail: impl Into<String>);
// pub
fn report_warning(&mut self, stage: &str, detail: impl Into<String>);
// pub
fn report_failure(&mut self, stage: &str, elapsed: Duration, detail: impl Into<String>);
// pub
fn start(reporter: &'a mut StartupProgressReporter, stage: &'static str) -> Self;
// pub
fn elapsed(&self) -> Duration;
// pub
fn started_at(&self) -> Instant;
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`progress_channel_holds_latest_value_only`, `reporter_without_live_channel_never_panics`, `recovery_counts_are_real_not_hardcoded`

---
