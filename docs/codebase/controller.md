# Autonomy Controller

> **Architectural Layer:** L8 Autonomy  
> **Source Directory:** `src/controller`  
> **File Count:** 8 source files  

Execution stage transitions, halting criteria, loop detection, and progress monitoring.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [dependencies.rs](#src-controller-dependencies-rs) | 821 | `ControllerDependencies` | Subsystem component |
| [error.rs](#src-controller-error-rs) | 46 | `ControllerError` | Subsystem component |
| [halting.rs](#src-controller-halting-rs) | 189 | `HaltEvaluation, ControllerHaltReason` | Subsystem component |
| [harness.rs](#src-controller-harness-rs) | 461 | `MockContextCompiler, MockControllerHarness, MockEscalationChannel` | Subsystem component |
| [loop_detector.rs](#src-controller-loop_detector-rs) | 164 | `LoopDetector, LoopSignature` | Subsystem component |
| [mod.rs](#src-controller-mod-rs) | 2520 | `AutonomyController` | Subsystem component |
| [progress.rs](#src-controller-progress-rs) | 232 | `ControllerProgress, LoopStage` | Subsystem component |
| [stage.rs](#src-controller-stage-rs) | 368 | `StageOutcome` | Subsystem component |

---

### `src/controller/dependencies.rs` {#src-controller-dependencies-rs}

- **Source Link:** [`src/controller/dependencies.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/controller/dependencies.rs)
- **Lines of Code:** 821 (34147 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (1):** `ControllerDependencies`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn planner(&self) -> &Arc<dyn PlanService>;
// pub
fn scheduler(&self) -> &Arc<dyn WorkScheduler>;
// pub
fn policy(&self) -> &Arc<dyn PolicyGate>;
// pub
fn context(&self) -> &Arc<dyn ContextCompiler>;
// pub
fn dispatcher(&self) -> &Arc<dyn WorkerDispatcher>;
// pub
fn verifier(&self) -> &Arc<dyn VerificationEngine>;
// pub
fn recovery(&self) -> &Arc<dyn RecoveryEngine>;
// pub
fn escalation(&self) -> &Arc<dyn EscalationChannel>;
// pub
fn transaction_manager(&self) -> Option<&Arc<SqliteTransactionManager>>;
// pub
fn execution_run_repo(&self) -> Option<&Arc<dyn ExecutionRunRepository>>;
// pub
fn mission_repo(&self) -> Option<&Arc<dyn MissionRepository>>;
// pub
fn report_generator(&self) -> Option<&Arc<crate::report::ReportGenerator>>;
// pub
fn workspace_root(&self) -> Option<&std::path::Path>;
// pub
fn approval_coordinator(&self,) -> Option<&Arc<crate::policy::approval::ApprovalCoordinator>>;
// pub
fn checkpoint_manager(&self,) -> Option<&Arc<crate::checkpoint::manager::CheckpointManager>>;
```

---

### `src/controller/error.rs` {#src-controller-error-rs}

- **Source Link:** [`src/controller/error.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/controller/error.rs)
- **Lines of Code:** 46 (1324 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Enums (1):** `ControllerError`

#### Key Functions & Signatures (1 shown)
```rust
// private
fn test_error_formatting();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_error_formatting`

---

### `src/controller/halting.rs` {#src-controller-halting-rs}

- **Source Link:** [`src/controller/halting.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/controller/halting.rs)
- **Lines of Code:** 189 (6446 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (1):** `HaltEvaluation`
- **Enums (1):** `ControllerHaltReason`

#### Key Functions & Signatures (7 shown)
```rust
// pub
fn precedence_rank(&self) -> u8;
// pub
fn resolve_primary(conditions: &[ControllerHaltReason]) -> Option<ControllerHaltReason>;
// pub
fn new(conditions: Vec<ControllerHaltReason>) -> Option<Self>;
// private
fn test_precedence_ranking();
// private
fn test_resolve_primary_safety_invariants();
// private
fn test_halt_evaluation_audit();
// private
fn test_precedence_rank_ordering_strictly_monotonic();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_precedence_ranking`, `test_resolve_primary_safety_invariants`, `test_halt_evaluation_audit`, `test_precedence_rank_ordering_strictly_monotonic`

---

### `src/controller/harness.rs` {#src-controller-harness-rs}

- **Source Link:** [`src/controller/harness.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/controller/harness.rs)
- **Lines of Code:** 461 (14063 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (9):** `MockContextCompiler`, `MockControllerHarness`, `MockEscalationChannel`, `MockPlanService`, `MockPolicyGate`, `MockRecoveryEngine`, `MockVerificationEngine`, `MockWorkScheduler`, `MockWorkerDispatcher`

#### Key Functions & Signatures (15 shown)
```rust
// private
async fn has_valid_plan(&self, _mission_id: MissionId) -> Result<bool, PlanError>;
// private
async fn generate_initial_plan(&self, _req: PlanRequest) -> Result<PlanResponse, PlanError>;
// private
async fn replan(&self, req: ReplanRequest) -> Result<ReplanResponse, PlanError>;
// private
fn default() -> Self;
// private
async fn find_ready_work(&self,
        _mission_id: MissionId,) -> Result<ReadyWorkResponse, SchedulerError>;
// private
async fn is_work_complete(&self, _mission_id: MissionId) -> Result<bool, SchedulerError>;
// private
async fn mark_task_started(&self,
        task_id: TaskId,
        agent_id: AgentId,) -> Result<(), SchedulerError>;
// private
fn default() -> Self;
// private
async fn evaluate(&self, req: PolicyEvaluationRequest) -> Result<PolicyDecision, PolicyError>;
// private
fn policy_hash(&self) -> Option<String>;
// private
fn default() -> Self;
// private
async fn compile_context(&self,
        req: ContextCompilationRequest,) -> Result<CompiledContext, ContextError>;
// private
fn default() -> Self;
// private
async fn allocate_worker(&self,
        task_id: TaskId,
        _mission_id: MissionId,
        _capabilities: &[String;
// private
async fn dispatch_work(&self,
        req: WorkExecutionRequest,) -> Result<WorkExecutionHandle, ExecutionError>;
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_mock_controller_harness_happy_path`

---

### `src/controller/loop_detector.rs` {#src-controller-loop_detector-rs}

- **Source Link:** [`src/controller/loop_detector.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/controller/loop_detector.rs)
- **Lines of Code:** 164 (5063 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (2):** `LoopDetector`, `LoopSignature`

#### Key Functions & Signatures (9 shown)
```rust
// pub
fn new(capacity: usize, repetition_threshold: usize) -> Self;
// pub
fn record(&mut self, signature: LoopSignature) -> bool;
// pub
fn clear(&mut self);
// pub
fn signatures(&self) -> &VecDeque<LoopSignature>;
// private
fn default() -> Self;
// private
fn test_loop_detected_at_threshold();
// private
fn test_progress_advancement_resets_loop_count();
// private
fn test_sliding_window_capacity_bound();
// private
fn test_loop_detector_clear_and_eviction_semantics();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_loop_detected_at_threshold`, `test_progress_advancement_resets_loop_count`, `test_sliding_window_capacity_bound`, `test_loop_detector_clear_and_eviction_semantics`

---

### `src/controller/mod.rs` {#src-controller-mod-rs}

- **Source Link:** [`src/controller/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/controller/mod.rs)
- **Lines of Code:** 2520 (121500 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (1):** `AutonomyController`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(mission_id: MissionId,
        mode: AutonomyMode,
        dependencies: ControllerDependencies,
        event_bu;
// pub
fn with_max_cycles(mut self, max_cycles: Option<u64>) -> Self;
// pub
fn with_mission_objective(mut self, objective: impl Into<String>) -> Self;
// pub
fn with_workspace_root(mut self, root: impl Into<std::path::PathBuf>) -> Self;
// pub
fn with_pause_token(mut self, pause_token: CancellationToken) -> Self;
// pub
fn with_policy_role(mut self, role: crate::state_machine::agent::AgentRole) -> Self;
// pub
fn with_step_history(mut self,
        history: Vec<crate::kernel::seams::context::StepRecordDto>,) -> Self;
// pub
fn with_upstream_context(mut self,
        context: crate::kernel::seams::planner::UpstreamPlanContext,) -> Self;
// pub
fn effective_workspace_root(&self) -> Option<&std::path::Path>;
// private
fn task_policy_request(&self,
        task_id: TaskId,) -> Result<PolicyEvaluationRequest, ControllerError>;
// private
async fn authorize_recovery_mutation(&self,
        task_id: TaskId,
        tool_action: &str,
        target_paths: Ve;
// private
async fn authorize_recovery_git(&self,
        task_id: TaskId,
        tool_action: &str,
        workspace: std::path:;
// private
async fn emit_event(&self, event_type: EventType);
// pub
async fn set_autonomy_mode(&mut self,
        new_mode: AutonomyMode,) -> Result<(), ControllerError>;
// pub
async fn step(&mut self) -> Result<StageOutcome, ControllerError>;
```

#### Unit Verification (7 inline tests)
Tests defined within module:
`test_single_stage_step`, `test_full_cycle_tick_and_event_publishing`, `test_cancellation_halts_run`, `test_pre_cancelled_run`, `test_step_when_cancelled_returns_halt`, `test_max_cycles_exceeded_halts`, `test_set_autonomy_mode_cycle_boundary`

---

### `src/controller/progress.rs` {#src-controller-progress-rs}

- **Source Link:** [`src/controller/progress.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/controller/progress.rs)
- **Lines of Code:** 232 (7216 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (1):** `ControllerProgress`
- **Enums (1):** `LoopStage`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn name(&self) -> &'static str;
// pub
fn is_first(&self) -> bool;
// pub
fn is_last(&self) -> bool;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// pub
fn new() -> Self;
// pub
fn advance_stage(&mut self, next: LoopStage);
// pub
fn increment_cycle(&mut self);
// pub
fn record_idle(&mut self);
// pub
fn reset_idle(&mut self);
// pub
fn record_failure(&mut self);
// pub
fn record_recovery(&mut self);
// private
fn default() -> Self;
// private
fn test_loop_stage_properties();
// private
fn test_controller_progress_lifecycle();
// private
fn test_loop_stage_first_last_and_all_names();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_loop_stage_properties`, `test_controller_progress_lifecycle`, `test_loop_stage_first_last_and_all_names`, `test_controller_progress_serde_roundtrip_complete`

---

### `src/controller/stage.rs` {#src-controller-stage-rs}

- **Source Link:** [`src/controller/stage.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/controller/stage.rs)
- **Lines of Code:** 368 (14007 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Enums (1):** `StageOutcome`

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn advance(stage: LoopStage) -> Self;
// pub
fn skip_to(stage: LoopStage) -> Self;
// pub
fn yield_now() -> Self;
// pub
fn yield_for(d: Duration) -> Self;
// pub
fn halt(reason: ControllerHaltReason) -> Self;
// pub
fn validate_transition(from: LoopStage,
        outcome: &StageOutcome,) -> Result<(), ControllerError>;
// private
fn test_valid_transitions();
// private
fn test_invalid_transitions();
// private
fn test_stage_outcome_helper_constructors();
// private
fn test_validate_transition_exhaustive_rejects_illegal_leaps();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_valid_transitions`, `test_invalid_transitions`, `test_stage_outcome_helper_constructors`, `test_validate_transition_exhaustive_rejects_illegal_leaps`

---
