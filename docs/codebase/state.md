# Authoritative State Management

> **Architectural Layer:** L8 State  
> **Source Directory:** `src/state`  
> **File Count:** 15 source files  

Execution run state, session state, task state, and SQLite projection.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [agent.rs](#src-state-agent-rs) | 131 | `Agent` | Agent aggregate model |
| [completion.rs](#src-state-completion-rs) | 159 | `CompletionContext, CompletionGate, CompletionGateError` | Authority classification (D3): this gate is a NON-AUTHORITATIVE local ... |
| [execution_run.rs](#src-state-execution_run-rs) | 173 | `ExecutionRun` | ExecutionRun aggregate model.  Canonical top-level execution entity ow... |
| [execution_run_service.rs](#src-state-execution_run_service-rs) | 307 | `ExecutionRunService` | ExecutionRun orchestration service coordinating lifecycle, transitions... |
| [fork.rs](#src-state-fork-rs) | 181 | `ForkInputs, ForkParent` | Shared fork-input resolution for Mission and ExecutionRun. |
| [intake.rs](#src-state-intake-rs) | 220 | `MissionIntake, NormalizedIntake, IntakeValidationError` | Subsystem component |
| [lifecycle.rs](#src-state-lifecycle-rs) | 236 | `LifecycleEntity` | Shared lifecycle behavior for Mission and ExecutionRun aggregates. |
| [mission.rs](#src-state-mission-rs) | 173 | `Mission` | Mission aggregate model (D-01, D-02, D-03, D-04, D-15). |
| [mission_service.rs](#src-state-mission_service-rs) | 378 | `MissionService` | Legacy Mission orchestration service adapter.  # Architecture Authorit... |
| [mod.rs](#src-state-mod-rs) | 33 | `Functions/Traits` | State module - authoritative domain state models (KRN-02)  Per D-14, s... |
| [policy_context.rs](#src-state-policy_context-rs) | 89 | `PolicyContext` | Policy context for execution authorization and sandbox profiles. |
| [recovery.rs](#src-state-recovery-rs) | 262 | `StateReconstructionEngine, CrashClassification` | Crash recovery classification and state reconstruction engine (MSN-05,... |
| [replay.rs](#src-state-replay-rs) | 140 | `ReplayError` | Shared error types for deterministic aggregate event replay. |
| [session.rs](#src-state-session-rs) | 176 | `Session, SessionState` | Session aggregate model (MSN-05, CONTEXT.md §43). |
| [task.rs](#src-state-task-rs) | 265 | `Task, BlockingReason` | Task aggregate model |

---

### `src/state/agent.rs` {#src-state-agent-rs}

- **Source Link:** [`src/state/agent.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state/agent.rs)
- **Lines of Code:** 131 (4119 bytes)

#### Primary Responsibility
Agent aggregate model

#### Types & Trait Declarations
- **Structs (1):** `Agent`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn new(id: AgentId, mission_id: MissionId, role: String) -> Self;
// pub
fn with_runtime_details(mut self,
        task_id: Option<TaskId>,
        profile_fingerprint: String,
        max_step;
// pub
fn update_status(&mut self, new_status: AgentState);
// pub
fn record_step_consumed(&mut self);
// pub
fn complete(&mut self, status: AgentState);
// private
fn test_agent_construction();
// private
fn test_agent_status_update();
// private
fn test_agent_serde_roundtrip();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_agent_construction`, `test_agent_status_update`, `test_agent_serde_roundtrip`

---

### `src/state/completion.rs` {#src-state-completion-rs}

- **Source Link:** [`src/state/completion.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state/completion.rs)
- **Lines of Code:** 159 (6046 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Authority classification (D3): this gate is a NON-AUTHORITATIVE local control-flow projection. It evaluates six in-memory booleans for early local decisions (intake gating, report scaffolding) and MUST NEVER emit final completion. The durable, authoritative completion decision belongs SOLELY to `EvidenceCompletionGate` (`verification/gate.rs`), which decides over persisted verification evidence and records the decision in `completion_gate_decisions` / the mission-task repositories.  ```text EvidenceCompletionGate → completion decision → mission/task repository (authoritative; persists; may veto) state::CompletionGate → local boolean projection (advisory only; never completes a mission) ```  Any caller treating `CompletionGate::can_complete` / `evaluate` as final completion is a defect. Mission/task/session code must consult the evidence gate; integrity tests prove that a satisfied local context alone cannot complete anything durable.

#### Types & Trait Declarations
- **Structs (2):** `CompletionContext`, `CompletionGate`
- **Enums (1):** `CompletionGateError`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn all_satisfied() -> Self;
// pub
fn evaluate(context: &CompletionContext) -> Result<(), Vec<CompletionGateError>>;
// pub
fn can_complete(context: &CompletionContext) -> bool;
// private
fn test_completion_gate_all_satisfied();
// private
fn test_completion_gate_empty_context_accumulates_all_errors();
// private
fn test_completion_gate_single_failure();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_completion_gate_all_satisfied`, `test_completion_gate_empty_context_accumulates_all_errors`, `test_completion_gate_single_failure`

---

### `src/state/execution_run.rs` {#src-state-execution_run-rs}

- **Source Link:** [`src/state/execution_run.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state/execution_run.rs)
- **Lines of Code:** 173 (5902 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
ExecutionRun aggregate model.  Canonical top-level execution entity owning the execution lifecycle, state transitions, and event replay watermarks.

#### Types & Trait Declarations
- **Structs (1):** `ExecutionRun`

#### Key Functions & Signatures (9 shown)
```rust
// pub
fn new(id: ExecutionRunId, objective: String) -> Self;
// pub
fn from_normalized(id: ExecutionRunId, normalized: NormalizedIntake) -> Self;
// pub
fn update_status(&mut self, new_status: ExecutionRunState);
// pub
fn update_watermark(&mut self, sequence: u64);
// pub
fn apply(&mut self,
        envelope: &crate::events::envelope::EventEnvelope,) -> Result<(), ReplayError>;
// private
fn test_execution_run_construction();
// private
fn test_execution_run_status_update();
// private
fn test_execution_run_watermark_update();
// private
fn test_execution_run_serde_roundtrip();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_execution_run_construction`, `test_execution_run_status_update`, `test_execution_run_watermark_update`, `test_execution_run_serde_roundtrip`

---

### `src/state/execution_run_service.rs` {#src-state-execution_run_service-rs}

- **Source Link:** [`src/state/execution_run_service.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state/execution_run_service.rs)
- **Lines of Code:** 307 (9917 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
ExecutionRun orchestration service coordinating lifecycle, transitions, and persistence boundaries.

#### Types & Trait Declarations
- **Structs (1):** `ExecutionRunService`

#### Key Functions & Signatures (9 shown)
```rust
// pub
fn new(transaction_manager: Arc<SqliteTransactionManager>,
        run_repo: Arc<SqliteExecutionRunRepository>,
        ;
// pub
async fn create_run(&self,
        intake: MissionIntake,
        default_workspace: &Path,) -> Result<ExecutionRun, M31;
// pub
async fn create_direct_run(&self,
        objective: String,
        workspace_root: PathBuf,
        mode: AutonomyMode;
// pub
async fn transition_run(&self,
        id: ExecutionRunId,
        target_state: ExecutionRunState,
        actor: &str,;
// pub
async fn fork_run(&self,
        parent_id: ExecutionRunId,
        overrides: Option<MissionIntake>,
        default_wo;
// pub
async fn get(&self, id: ExecutionRunId) -> Result<Option<ExecutionRun>, M31AError>;
// pub
async fn list(&self) -> Result<Vec<ExecutionRun>, M31AError>;
// private
async fn setup_test_service() -> (ExecutionRunService, Arc<SqliteExecutionRunRepository>);
// private
async fn test_create_and_transition_run();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_create_and_transition_run`

---

### `src/state/fork.rs` {#src-state-fork-rs}

- **Source Link:** [`src/state/fork.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state/fork.rs)
- **Lines of Code:** 181 (6749 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Shared fork-input resolution for Mission and ExecutionRun.

#### Types & Trait Declarations
- **Structs (2):** `ForkInputs`, `ForkParent`

#### Key Functions & Signatures (5 shown)
```rust
// pub(crate)
fn resolve_fork_inputs(parent: ForkParent<'_>,
    overrides: Option<MissionIntake>,
    default_workspace: &Path,) -> R;
// private
fn parent(constraints: &'a [String],
        requirements: &'a [String],
        success_criteria: &'a [String],
       ;
// private
fn overrides(objective: &str,
        constraints: Vec<String>,
        success_criteria: Vec<String>,) -> MissionIntake;
// private
fn fork_without_overrides_copies_parent_specification();
// private
fn empty_override_lists_inherit_while_nonempty_lists_replace();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`fork_without_overrides_copies_parent_specification`, `empty_override_lists_inherit_while_nonempty_lists_replace`

---

### `src/state/intake.rs` {#src-state-intake-rs}

- **Source Link:** [`src/state/intake.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state/intake.rs)
- **Lines of Code:** 220 (7475 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (2):** `MissionIntake`, `NormalizedIntake`
- **Enums (1):** `IntakeValidationError`

#### Key Functions & Signatures (11 shown)
```rust
// pub
fn new(objective: impl Into<String>) -> Self;
// pub
fn validate(&self) -> Result<(), IntakeValidationError>;
// private
fn validate_path_safety(path: &Path) -> Result<(), IntakeValidationError>;
// pub
fn normalize(&self,
        default_workspace: &Path,) -> Result<NormalizedIntake, IntakeValidationError>;
// pub
fn generate_mission_intake_schema() -> serde_json::Value;
// private
fn test_intake_minimal_valid();
// private
fn test_intake_rejects_unknown_fields();
// private
fn test_intake_rejects_empty_objective();
// private
fn test_intake_rejects_path_traversal();
// private
fn test_intake_normalize();
// private
fn test_generate_mission_intake_schema();
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_intake_minimal_valid`, `test_intake_rejects_unknown_fields`, `test_intake_rejects_empty_objective`, `test_intake_rejects_path_traversal`, `test_intake_normalize`, `test_generate_mission_intake_schema`

---

### `src/state/lifecycle.rs` {#src-state-lifecycle-rs}

- **Source Link:** [`src/state/lifecycle.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state/lifecycle.rs)
- **Lines of Code:** 236 (7586 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Shared lifecycle behavior for Mission and ExecutionRun aggregates.

#### Types & Trait Declarations
- **Enums (1):** `LifecycleEntity`

#### Key Functions & Signatures (9 shown)
```rust
// private
fn label(self) -> &'static str;
// pub(crate)
fn update_status(status: &mut ExecutionRunState,
    started_at: &mut Option<DateTime<Utc>>,
    completed_at: &mut Opti;
// pub(crate)
fn update_watermark(last_applied_sequence: &mut u64,
    updated_at: &mut DateTime<Utc>,
    sequence: u64,);
// pub(crate)
fn enforce_completion_gate(next_state: ExecutionRunState,
    context: Option<&CompletionContext>,
    entity: Lifecycle;
// pub(crate)
fn prepare_transition(current_state: ExecutionRunState,
    target_state: ExecutionRunState,
    mission_id: MissionId,
;
// pub(crate)
fn event_for_transition(mission_id: MissionId,
    previous_state: ExecutionRunState,
    next_state: ExecutionRunState,;
// private
fn event_for_transition_preserves_entity_specific_failure_reasons();
// private
fn prepare_transition_preserves_entity_specific_shortcuts();
// private
fn paused_to_executing_emits_resume_event();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`event_for_transition_preserves_entity_specific_failure_reasons`, `prepare_transition_preserves_entity_specific_shortcuts`, `paused_to_executing_emits_resume_event`

---

### `src/state/mission.rs` {#src-state-mission-rs}

- **Source Link:** [`src/state/mission.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state/mission.rs)
- **Lines of Code:** 173 (6057 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Mission aggregate model (D-01, D-02, D-03, D-04, D-15).

#### Types & Trait Declarations
- **Structs (1):** `Mission`

#### Key Functions & Signatures (9 shown)
```rust
// pub
fn new(id: MissionId, objective: String) -> Self;
// pub
fn from_normalized(id: MissionId, normalized: NormalizedIntake) -> Self;
// pub
fn update_status(&mut self, new_status: MissionState);
// pub
fn update_watermark(&mut self, sequence: u64);
// pub
fn apply(&mut self,
        envelope: &crate::events::envelope::EventEnvelope,) -> Result<(), ReplayError>;
// private
fn test_mission_construction();
// private
fn test_mission_status_update();
// private
fn test_mission_watermark_update();
// private
fn test_mission_serde_roundtrip();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_mission_construction`, `test_mission_status_update`, `test_mission_watermark_update`, `test_mission_serde_roundtrip`

---

### `src/state/mission_service.rs` {#src-state-mission_service-rs}

- **Source Link:** [`src/state/mission_service.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state/mission_service.rs)
- **Lines of Code:** 378 (13360 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Legacy Mission orchestration service adapter.  # Architecture Authority Notice Canonical runtime execution lifecycle authority is `ExecutionRunService` and `SqliteExecutionRunRepository`. This `MissionService` aggregate is maintained strictly as a backwards-compatibility adapter for legacy tests and workflows. All new production execution transitions must pass through `ExecutionRunService`.

#### Types & Trait Declarations
- **Structs (1):** `MissionService`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn new(transaction_manager: Arc<SqliteTransactionManager>,
        mission_repo: Arc<SqliteMissionRepository>,
        e;
// pub
async fn create_mission(&self,
        intake: MissionIntake,
        default_workspace: &Path,) -> Result<Mission, M31A;
// pub
async fn transition_mission(&self,
        id: MissionId,
        target_state: MissionState,
        actor: &str,
     ;
// pub
async fn fork_mission(&self,
        parent_id: MissionId,
        overrides: Option<MissionIntake>,
        default_wor;
// private
async fn setup_test_service() -> (
        MissionService,
        Arc<SqliteMissionRepository>,
        tempfile::TempD;
// private
async fn test_create_mission_happy_path();
// private
async fn test_transition_mission_with_completion_gate();
// private
async fn test_fork_mission_immutability();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_create_mission_happy_path`, `test_transition_mission_with_completion_gate`, `test_fork_mission_immutability`

---

### `src/state/mod.rs` {#src-state-mod-rs}

- **Source Link:** [`src/state/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state/mod.rs)
- **Lines of Code:** 33 (1101 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
State module - authoritative domain state models (KRN-02)  Per D-14, state/ owns authoritative domain state models. Per D-11, these models persist current state while an append-only transition log captures audit/replay data.

---

### `src/state/policy_context.rs` {#src-state-policy_context-rs}

- **Source Link:** [`src/state/policy_context.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state/policy_context.rs)
- **Lines of Code:** 89 (2719 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Policy context for execution authorization and sandbox profiles.

#### Types & Trait Declarations
- **Structs (1):** `PolicyContext`

#### Key Functions & Signatures (5 shown)
```rust
// pub
fn standard() -> Self;
// pub
fn for_profile(profile_name: &str) -> Result<Self, crate::config::ConfigError>;
// private
fn default() -> Self;
// private
fn test_policy_context_standard();
// private
fn test_policy_context_serde_roundtrip();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_policy_context_standard`, `test_policy_context_serde_roundtrip`

---

### `src/state/recovery.rs` {#src-state-recovery-rs}

- **Source Link:** [`src/state/recovery.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state/recovery.rs)
- **Lines of Code:** 262 (9696 bytes)

#### Primary Responsibility
Crash recovery classification and state reconstruction engine (MSN-05, EVT-04, D-14, D-15, D-17).

#### Types & Trait Declarations
- **Structs (1):** `StateReconstructionEngine`
- **Enums (1):** `CrashClassification`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn new(mission_repo: Arc<M>, event_repo: Arc<E>) -> Self;
// pub
async fn classify(&self, mission_id: MissionId) -> Result<CrashClassification, M31AError>;
// pub
async fn reconstruct(&self, mission_id: MissionId) -> Result<Mission, M31AError>;
// private
async fn test_recovery_safe_to_resume_when_equal();
// private
async fn test_recovery_needs_repair_and_replays_events();
// private
async fn test_recovery_fails_closed_on_corrupt_watermark();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_recovery_safe_to_resume_when_equal`, `test_recovery_needs_repair_and_replays_events`, `test_recovery_fails_closed_on_corrupt_watermark`

---

### `src/state/replay.rs` {#src-state-replay-rs}

- **Source Link:** [`src/state/replay.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state/replay.rs)
- **Lines of Code:** 140 (4704 bytes)

#### Primary Responsibility
Shared error types for deterministic aggregate event replay.

#### Types & Trait Declarations
- **Enums (1):** `ReplayError`

#### Key Functions & Signatures (3 shown)
```rust
// pub(crate)
fn apply_lifecycle_event(status: &mut ExecutionRunState,
    started_at: &mut Option<DateTime<Utc>>,
    completed_at: &;
// private
fn started_event_updates_status_start_time_and_watermark();
// private
fn completed_event_marks_terminal_timestamp();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`started_event_updates_status_start_time_and_watermark`, `completed_event_marks_terminal_timestamp`

---

### `src/state/session.rs` {#src-state-session-rs}

- **Source Link:** [`src/state/session.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state/session.rs)
- **Lines of Code:** 176 (5514 bytes)

#### Primary Responsibility
Session aggregate model (MSN-05, CONTEXT.md §43).

#### Types & Trait Declarations
- **Structs (1):** `Session`
- **Enums (1):** `SessionState`

#### Key Functions & Signatures (14 shown)
```rust
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn new(id: SessionId) -> Self;
// pub
fn for_run(id: SessionId, run_id: ExecutionRunId) -> Self;
// pub
fn for_mission(id: SessionId, mission_id: MissionId) -> Self;
// pub
fn new_with_mission(id: SessionId, mission_id: MissionId) -> Self;
// pub
fn attach_run(&mut self, run_id: ExecutionRunId);
// pub
fn close(&mut self);
// pub
fn fail(&mut self);
// pub
fn update_metadata(&mut self, metadata: serde_json::Value);
// private
fn test_standalone_session_construction();
// private
fn test_session_for_run_and_mission();
// private
fn test_session_close();
// private
fn test_session_serde_roundtrip();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_standalone_session_construction`, `test_session_for_run_and_mission`, `test_session_close`, `test_session_serde_roundtrip`

---

### `src/state/task.rs` {#src-state-task-rs}

- **Source Link:** [`src/state/task.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state/task.rs)
- **Lines of Code:** 265 (9705 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Task aggregate model

#### Types & Trait Declarations
- **Structs (1):** `Task`
- **Enums (1):** `BlockingReason`

#### Key Functions & Signatures (14 shown)
```rust
// pub
fn new(id: TaskId, mission_id: MissionId, title: String) -> Self;
// pub
fn update_status(&mut self, new_status: TaskState);
// pub
fn canonical_run_id(&self) -> ExecutionRunId;
// pub
fn can_retry(&self) -> bool;
// pub
fn record_retry(&mut self);
// pub
fn set_blocked(&mut self, reason: BlockingReason);
// pub
fn set_result(&mut self, result: TaskResult);
// pub
fn mark_started(&mut self);
// pub
fn mark_completed(&mut self, result: TaskResult);
// private
fn test_task_construction();
// private
fn test_task_status_update();
// private
fn test_task_retry_lifecycle();
// private
fn test_task_blocking_and_results();
// private
fn test_task_serde_roundtrip();
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_task_construction`, `test_task_status_update`, `test_task_retry_lifecycle`, `test_task_blocking_and_results`, `test_task_serde_roundtrip`

---
