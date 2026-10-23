# Agent Subsystem

> **Architectural Layer:** L4 Agents  
> **Source Directory:** `src/agent`  
> **File Count:** 17 source files  

Agent roles, lifecycle, supervisor, runner, adaptive replanning, and delegation.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [action.rs](#src-agent-action-rs) | 735 | `ActionExecutionRecord, ActionUserOption, DiagnosticRecord` | Canonical Action/Outcome Protocol (Issue 21, ACT-01..04).  "The model ... |
| [adaptive.rs](#src-agent-adaptive-rs) | 568 | `AdaptiveReplanOutcome, AdaptiveReplanRequest, AssumptionInvalidationReport` | Adaptive Execution, Recovery &amp; Replanning Subsystem.  "The model p... |
| [delegation.rs](#src-agent-delegation-rs) | 179 | `DelegationContract, DelegationHierarchyRecord, DelegationOutcome` | Typed multi-agent delegation contracts and runtime delegation protocol... |
| [dispatcher.rs](#src-agent-dispatcher-rs) | 1204 | `ProductionWorkerDispatcher, TestModelCaller` | Production WorkerDispatcher implementing the Autonomy Controller consu... |
| [engine.rs](#src-agent-engine-rs) | 2495 | `AgentEngine, StructuredToolResult, AgentEngineState` | Canonical Continuous Interactive Coding-Agent Engine.  "The model prop... |
| [envelope.rs](#src-agent-envelope-rs) | 187 | `CapabilityEnvelope, CapabilityIntersectionError` | Role capability envelopes and task-assignment capability intersection ... |
| [events.rs](#src-agent-events-rs) | 174 | `Functions/Traits` | Agent lifecycle event publishers (D-15).  Emits first-class typed doma... |
| [handoff.rs](#src-agent-handoff-rs) | 292 | `AgentHandoffArbiter, HandoffProposal, HandoffRecord` | Dual-path agent handoff protocol and runtime handoff arbitration (AGT-... |
| [intent.rs](#src-agent-intent-rs) | 1407 | `AssumptionInvalidation, FormedTask, IntentAssumption` | First-class Intent Understanding &amp; Adaptive Task Formation.  # Arc... |
| [intent_repository.rs](#src-agent-intent_repository-rs) | 186 | `SqliteIntentRepository` | Durable persistence for Intent State.  Provides `SqliteIntentRepositor... |
| [mod.rs](#src-agent-mod-rs) | 62 | `Functions/Traits` | Agent Runtime Subsystem.  Owns specialized bounded agent execution, ro... |
| [model_policy.rs](#src-agent-model_policy-rs) | 1409 | `ModelPolicy, ProviderModelCaller, RoutedModelCaller` | Model selection policy and ModelCaller seam trait (D-04, AGT-05).  Enf... |
| [profile.rs](#src-agent-profile-rs) | 240 | `AgentProfile, ContextPolicy, ProfileOverride` | Canonical 8 role profiles, 10-field AgentProfile contract, and SHA-256... |
| [registry.rs](#src-agent-registry-rs) | 530 | `InferenceRule, RoleDefinition, RoleRegistry` | Open role registry: existence and metadata authority for agent roles. ... |
| [builtins.rs](#src-agent-registry-builtins-rs) | 606 | `Functions/Traits` | Subsystem component |
| [runner.rs](#src-agent-runner-rs) | 1990 | `ActionRequest, ActionResult, AgentStepRecord` | Seam-driven bounded step execution loop (AGT-05, D-03, D-06).  Execute... |
| [supervisor.rs](#src-agent-supervisor-rs) | 579 | `ExecutionActivityTracker, FailureEvidence, WorkerSupervisor` | Supervised async worker lifecycle, panic containment, and dual timeout... |

---

### `src/agent/action.rs` {#src-agent-action-rs}

- **Source Link:** [`src/agent/action.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/action.rs)
- **Lines of Code:** 735 (29207 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Canonical Action/Outcome Protocol (Issue 21, ACT-01..04).  "The model proposes. The runtime decides."  Provides the strongly typed runtime protocol bridging: - Model proposals - AgentEngine / WorkerRunner - Task scheduler - Workflow execution - Tool governance and sandbox - Verification hierarchy - Telemetry and TUI projection

#### Types & Trait Declarations
- **Structs (3):** `ActionExecutionRecord`, `ActionUserOption`, `DiagnosticRecord`
- **Enums (3):** `ActionParseError`, `AgentAction`, `AgentObservation`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn name(&self) -> &'static str;
// pub
fn try_from_tool_call(call: &crate::model::types::ModelToolCall,) -> Result<Self, ActionParseError>;
// pub
fn from_tool_call(call: &crate::model::types::ModelToolCall,) -> Result<Self, ActionParseError>;
// pub
fn from_model_proposal(proposal: &crate::model::types::ModelProposal,) -> Result<Vec<Self>, ActionParseError>;
// pub
fn is_success(&self) -> bool;
// pub
fn output_text(&self) -> String;
// pub
fn error_text(&self) -> Option<String>;
// pub
fn duration_ms(&self) -> u64;
```

---

### `src/agent/adaptive.rs` {#src-agent-adaptive-rs}

- **Source Link:** [`src/agent/adaptive.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/adaptive.rs)
- **Lines of Code:** 568 (21839 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Adaptive Execution, Recovery &amp; Replanning Subsystem.  "The model proposes. The runtime decides."  Provides canonical runtime structures and algorithms for: - Structured diagnostic evidence flow from execution - Evidence-based stagnation and loop detection across workspace mutations - Adaptive strategy transitions between TaskShapes - Plan-aware replanning with task completion preservation - Assumption invalidation propagation to dependent work - Dynamic unknown tracking during execution - Finite runtime-owned execution budgets - Multi-class failure categorization

#### Types & Trait Declarations
- **Structs (8):** `AdaptiveReplanOutcome`, `AdaptiveReplanRequest`, `AssumptionInvalidationReport`, `DiagnosticEvidence`, `ExecutionObservation`, `StallDetector`, `StrategyTransitionRecord`, `SubagentFailureEvidence`
- **Enums (3):** `ExecutionFailureCategory`, `FingerprintComparison`, `StallEvaluation`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(tool_name: impl Into<String>,
        failure_class: FailureClassification,
        error_summary: impl Into<Stri;
// pub
fn with_target(mut self, target: impl Into<String>) -> Self;
// pub
fn with_detailed_output(mut self, output: impl Into<String>) -> Self;
// pub
fn with_exit_code(mut self, code: i32) -> Self;
// pub
fn with_affected_files(mut self, files: Vec<String>) -> Self;
// pub
fn with_policy_denial(mut self, is_denial: bool) -> Self;
// pub
fn with_category(mut self, category: ExecutionFailureCategory) -> Self;
// pub
fn with_subagent_failure(mut self, failure: SubagentFailureEvidence) -> Self;
// pub
fn is_retryable(&self) -> bool;
// pub
fn compare_workspace_fingerprints(previous: &str, current: &str) -> FingerprintComparison;
// pub
fn new() -> Self;
// pub
fn with_max_failures(mut self, max: usize) -> Self;
// pub
fn evaluate_proposal(&self,
        tool_name: &str,
        input_fingerprint: &str,
        current_workspace_fingerpr;
// pub
fn record_observation(&mut self, observation: ExecutionObservation);
// pub
fn clear(&mut self);
```

---

### `src/agent/delegation.rs` {#src-agent-delegation-rs}

- **Source Link:** [`src/agent/delegation.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/delegation.rs)
- **Lines of Code:** 179 (5759 bytes)

#### Primary Responsibility
Typed multi-agent delegation contracts and runtime delegation protocols (Issue 13).  Enforces bounded recursion depth, typed contract specifications, restricted capability envelopes, failure isolation, and parent-child audit trails.

#### Types & Trait Declarations
- **Structs (3):** `DelegationContract`, `DelegationHierarchyRecord`, `DelegationOutcome`
- **Enums (1):** `DelegationError`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn new(parent_role: impl Into<String>,
        target_role: impl Into<String>,
        subtask_title: impl Into<String>,;
// pub
fn with_max_depth(mut self, max_depth: usize) -> Self;
// pub
fn with_timeout_secs(mut self, secs: u64) -> Self;
// pub
fn with_parent_agent_id(mut self, agent_id: AgentId) -> Self;
// pub
fn validate(&self) -> Result<(), DelegationError>;
// private
fn test_delegation_validation_success();
// private
fn test_delegation_depth_limit();
// private
fn test_self_delegation_rejected();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_delegation_validation_success`, `test_delegation_depth_limit`, `test_self_delegation_rejected`

---

### `src/agent/dispatcher.rs` {#src-agent-dispatcher-rs}

- **Source Link:** [`src/agent/dispatcher.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/dispatcher.rs)
- **Lines of Code:** 1204 (51076 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Production WorkerDispatcher implementing the Autonomy Controller consumer seam (AGT-04, AGT-05, D-05).  Provides deterministic worker allocation with capability intersection, supervised async job dispatch, and terminal outcome collection.

#### Types & Trait Declarations
- **Structs (2):** `ProductionWorkerDispatcher`, `TestModelCaller`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn new_with_roots(workspace_root: impl Into<std::path::PathBuf>,
        storage_root: impl Into<std::path::PathBuf>,) -;
// pub
fn new_with_roots_and_config(workspace_root: impl Into<std::path::PathBuf>,
        storage_root: impl Into<std::path::P;
// pub
fn new_with_workspace(workspace_root: impl Into<std::path::PathBuf>) -> Self;
// pub
fn capability_registry(&self) -> &Arc<CapabilityRegistry>;
// pub
fn policy_gate(&self) -> &Arc<dyn PolicyGate>;
// pub
fn dispatcher_autonomy_mode(&self) -> AutonomyMode;
// pub
fn runtime_timeout_secs(&self) -> u64;
// pub
fn effective_wall_timeout_secs(&self, profile_wall_secs: u64) -> u64;
// pub
fn model_caller(&self) -> &Arc<dyn ModelCaller>;
// pub
fn dispatcher_workspace_root(&self) -> &std::path::Path;
// pub
fn db_pool(&self) -> Option<&sqlx::SqlitePool>;
// pub
fn dispatcher_approval_coordinator(&self) -> Option<&Arc<ApprovalCoordinator>>;
// pub
fn from_shared_authorities(workspace_root: std::path::PathBuf,
        capability_registry: Arc<CapabilityRegistry>,
   ;
// pub
fn with_replan_authority(mut self,
        replan_authority: Arc<crate::recovery::ReplanAuthority>,) -> Self;
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_allocate_worker_success`, `test_allocate_worker_rejects_out_of_envelope`, `test_dispatch_and_collect_result`, `test_dispatch_fails_closed_without_provider`

---

### `src/agent/engine.rs` {#src-agent-engine-rs}

- **Source Link:** [`src/agent/engine.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/engine.rs)
- **Lines of Code:** 2495 (103953 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Canonical Continuous Interactive Coding-Agent Engine.  "The model proposes. The runtime decides."  Provides the primary continuous interactive coding loop: ```text User Intent (minimal) ↓ AgentEngine (run_continuous) ↓ IntentState (inject into system prompt) ↓ Model Turn (understand intent via tools) ↓ Tool Calls / AskUser / Complete ↓ Runtime Authorization (PolicyGate &amp; Approval) ↓ Tool Execution (ToolPipelineRunner) ↓ Tool Results (Structured Evidence) ↓ IntentState update (persist enrichment) ↓ Next Agent Turn (Fresh Context with IntentState) ↓ Model ... ```  `IntentState` is integrated as a first-class field on `AgentEngine`.

#### Types & Trait Declarations
- **Structs (2):** `AgentEngine`, `StructuredToolResult`
- **Enums (2):** `AgentEngineState`, `AgentTurnOutcome`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(session_id: SessionId,
        workspace_root: PathBuf,
        session_repo: SqliteSessionRepository,
        mo;
// pub
fn with_autonomy_mode(mut self, mode: AutonomyMode) -> Self;
// pub
fn with_denied_tools(mut self, denied: Vec<String>) -> Self;
// pub
fn denied_tools(&self) -> &[String];
// pub
fn tool_authority_scope(&self) -> crate::tools::filter::ToolAuthorityScope;
// private
fn rebind_scoped_role_tools(mut self) -> Self;
// pub
fn with_role_authority(mut self, role: AgentRole) -> Self;
// pub
fn with_agent_identity(mut self, agent_id: AgentId) -> Self;
// pub
fn with_active_task(mut self, task_id: TaskId) -> Self;
// pub
fn bind_execution_identity(mut self,
        mission_id: Option<MissionId>,
        task_id: Option<TaskId>,
        age;
// pub
fn with_model_caller(mut self, caller: Arc<dyn ModelCaller>) -> Self;
// pub
fn capability_registry(&self) -> &Arc<CapabilityRegistry>;
// pub
fn with_execution_run_repo(mut self,
        execution_run_repo: crate::persistence::sqlite::repositories::SqliteExecuti;
// pub
fn with_scope_repos(mut self,
        mission_repo: crate::persistence::sqlite::repositories::SqliteMissionRepository,
 ;
// pub
fn pipeline_runner(&self) -> &Arc<ToolPipelineRunner>;
```

---

### `src/agent/envelope.rs` {#src-agent-envelope-rs}

- **Source Link:** [`src/agent/envelope.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/envelope.rs)
- **Lines of Code:** 187 (7599 bytes)

#### Primary Responsibility
Role capability envelopes and task-assignment capability intersection logic (AGT-04, D-02).  Enforces compile-time and runtime boundaries on agent actions, guaranteeing that task requirements cannot exceed role privilege envelopes.

#### Types & Trait Declarations
- **Structs (1):** `CapabilityEnvelope`
- **Enums (1):** `CapabilityIntersectionError`

#### Key Functions & Signatures (11 shown)
```rust
// pub
fn read_only(allowed: impl IntoIterator<Item = impl Into<String>>) -> Self;
// pub
fn workspace_write(allowed: impl IntoIterator<Item = impl Into<String>>) -> Self;
// pub
fn full_workspace(allowed: impl IntoIterator<Item = impl Into<String>>) -> Self;
// pub
fn network_read(allowed: impl IntoIterator<Item = impl Into<String>>) -> Self;
// pub
fn calculate_eligible_capabilities(task_capabilities: &[CapabilityRequirement],
    role_envelope: &CapabilityEnvelope,);
// private
fn test_read_only_envelope_rejects_write();
// private
fn test_read_only_envelope_rejects_shell();
// private
fn test_workspace_write_envelope_allows_write_and_shell();
// private
fn test_out_of_envelope_capability_fails_closed();
// private
fn test_empty_task_requirements_succeed();
// private
fn test_network_read_envelope();
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_read_only_envelope_rejects_write`, `test_read_only_envelope_rejects_shell`, `test_workspace_write_envelope_allows_write_and_shell`, `test_out_of_envelope_capability_fails_closed`, `test_empty_task_requirements_succeed`, `test_network_read_envelope`

---

### `src/agent/events.rs` {#src-agent-events-rs}

- **Source Link:** [`src/agent/events.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/events.rs)
- **Lines of Code:** 174 (4538 bytes)

#### Primary Responsibility
Agent lifecycle event publishers (D-15).  Emits first-class typed domain events (AgentSpawned, AgentStarted, AgentStepCompleted, AgentHandoffRecorded, AgentCompleted, AgentFailed, AgentCancelled) to EventBus. High-frequency telemetry (heartbeats, token chunks) is kept out of durable events.

#### Key Functions & Signatures (7 shown)
```rust
// pub
async fn emit_agent_spawned(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    agent_id: AgentId;
// pub
async fn emit_agent_started(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    agent_id: AgentId;
// pub
async fn emit_agent_step_completed(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    agent_id: ;
// pub
async fn emit_agent_handoff_recorded(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    handoff_;
// pub
async fn emit_agent_completed(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    agent_id: Agent;
// pub
async fn emit_agent_failed(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    agent_id: AgentId,;
// pub
async fn emit_agent_cancelled(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    agent_id: Agent;
```

---

### `src/agent/handoff.rs` {#src-agent-handoff-rs}

- **Source Link:** [`src/agent/handoff.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/handoff.rs)
- **Lines of Code:** 292 (10155 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Dual-path agent handoff protocol and runtime handoff arbitration (AGT-06, D-13, D-14).  Enforces bounded mid-task delegation (MAX_DELEGATION_DEPTH = 2), task-boundary transitions, durable SQLite persistence, and post-commit EventBus emission.

#### Types & Trait Declarations
- **Structs (4):** `AgentHandoffArbiter`, `HandoffProposal`, `HandoffRecord`, `InMemoryHandoffRepo`
- **Enums (1):** `HandoffError`
- **Traits (1):** `AgentHandoffRepository`

#### Key Functions & Signatures (12 shown)
```rust
// private
fn from(err: sqlx::Error) -> Self;
// private
fn from(err: serde_json::Error) -> Self;
// private
async fn insert_handoff(&self, record: &HandoffRecord) -> Result<(), HandoffError>;
// private
async fn find_by_mission(&self,
        mission_id: MissionId,) -> Result<Vec<HandoffRecord>, HandoffError>;
// private
async fn find_by_task(&self, task_id: TaskId) -> Result<Vec<HandoffRecord>, HandoffError>;
// pub
fn new(event_bus: Arc<dyn EventBus>) -> Self;
// pub
async fn evaluate_and_record_handoff(&self,
        repo: &R,
        mission_id: MissionId,
        proposal: HandoffPr;
// private
async fn insert_handoff(&self, record: &HandoffRecord) -> Result<(), HandoffError>;
// private
async fn find_by_mission(&self,
            mission_id: MissionId,) -> Result<Vec<HandoffRecord>, HandoffError>;
// private
async fn find_by_task(&self, task_id: TaskId) -> Result<Vec<HandoffRecord>, HandoffError>;
// private
async fn test_arbiter_records_handoff_and_emits_event();
// private
async fn test_arbiter_rejects_excessive_delegation_depth();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_arbiter_records_handoff_and_emits_event`, `test_arbiter_rejects_excessive_delegation_depth`

---

### `src/agent/intent.rs` {#src-agent-intent-rs}

- **Source Link:** [`src/agent/intent.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/intent.rs)
- **Lines of Code:** 1407 (52873 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
First-class Intent Understanding &amp; Adaptive Task Formation.  # Architecture  `IntentState` is the single canonical representation of what the agent understands about the user's request at any point during a session.  It is NOT a competing engine — it is a composable capability integrated into `AgentEngine`. The model populates intent state via structured tool calls; the runtime persists, validates, and injects the relevant fragment into each model turn's context.  ## Lifecycle  ```text UserIntent (raw text) ↓ IntentState::initial_from_prompt  ← only sets raw_prompt + timestamp ↓  (model turn with repository tools) IntentState (enriched by model-proposed facts) ↓  (unknowns discovered from evidence) IntentUnknown::from_evidence     ← runtime asserts evidence source ↓  (consequential decision identified) IntentDecision (AskUser → user answers → decision resolved) ↓  (model infers safe facts from repo) IntentAssumption with provenance ↓  (adaptive task formation) TaskShape selected by model, constrained by runtime ↓ AgentEngine execution

#### Types & Trait Declarations
- **Structs (9):** `AssumptionInvalidation`, `FormedTask`, `IntentAssumption`, `IntentDecision`, `IntentFact`, `IntentState`, `IntentUnknown`, `ResearchResult`, `SteeringConstraint`
- **Enums (7):** `DecisionResolution`, `DecisionStatus`, `FactOrigin`, `FormedTaskStatus`, `IntentError`, `TaskShape`, `UnknownResolution`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn trust_level(&self) -> TrustLevel;
// pub
fn epistemic_status(&self) -> EpistemicStatus;
// pub
fn to_provenance(&self, actor: impl Into<String>) -> Provenance;
// pub
fn from_evidence(id: impl Into<String>,
        description: impl Into<String>,
        criticality: Criticality,
      ;
// pub
fn is_resolved(&self) -> bool;
// pub
fn resolve(&mut self, resolution: UnknownResolution);
// pub
fn is_valid(&self) -> bool;
// pub
fn invalidate(&mut self, contradiction: AssumptionInvalidation);
// pub
fn is_pending(&self) -> bool;
// pub
fn resolve(&mut self, resolution: DecisionResolution);
// pub
fn requires_planning(&self) -> bool;
// pub
fn parse_strategy_name(input: &str) -> Option<Self>;
// pub
fn requires_user_input(&self) -> bool;
// pub
fn new(id: impl Into<String>,
        title: impl Into<String>,
        description: impl Into<String>,
        shape: T;
// pub
fn with_replacement(mut self, original_task_id: impl Into<String>) -> Self;
```

#### Unit Verification (10 inline tests)
Tests defined within module:
`test_initial_intent_state`, `test_add_evidence_backed_unknown`, `test_fabricated_unknown_rejected`, `test_resolve_unknown`, `test_steering_invalidates_assumption`, `test_task_invalidation_preserves_completed`, `test_context_fragment_renders_steering`, `test_serde_roundtrip`, `test_fact_origin_trust_levels`, `test_task_shape_properties`

---

### `src/agent/intent_repository.rs` {#src-agent-intent_repository-rs}

- **Source Link:** [`src/agent/intent_repository.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/intent_repository.rs)
- **Lines of Code:** 186 (6582 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
Durable persistence for Intent State.  Provides `SqliteIntentRepository` for storing, loading, and versioning `IntentState` in the session database.  Design: - `session_intent_state`: single mutable row per session (current state). - `intent_state_versions`: append-only audit log of every version. - `intent_decision_records`: dedicated decision lifecycle table.

#### Types & Trait Declarations
- **Structs (1):** `SqliteIntentRepository`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn new(pool: SqlitePool) -> Self;
// pub
async fn save(&self, state: &IntentState) -> Result<(), sqlx::Error>;
// pub
async fn load(&self, session_id: SessionId) -> Result<Option<IntentState>, sqlx::Error>;
// pub
async fn record_decision(&self,
        session_id: SessionId,
        decision: &IntentDecision,) -> Result<(), sqlx::E;
// pub
async fn list_versions(&self, session_id: SessionId) -> Result<Vec<i64>, sqlx::Error>;
// private
fn parse_session_id(session_str: &str) -> Result<Vec<u8>, sqlx::Error>;
```

---

### `src/agent/mod.rs` {#src-agent-mod-rs}

- **Source Link:** [`src/agent/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/mod.rs)
- **Lines of Code:** 62 (2401 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Agent Runtime Subsystem.  Owns specialized bounded agent execution, role profiles, fresh context compilation, worker supervision, handoff arbitration, and completion gating.

---

### `src/agent/model_policy.rs` {#src-agent-model_policy-rs}

- **Source Link:** [`src/agent/model_policy.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/model_policy.rs)
- **Lines of Code:** 1409 (54739 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Model selection policy and ModelCaller seam trait (D-04, AGT-05).  Enforces that the runtime deterministically selects models based on declared policy and hard requirements with ordered fallback. LLMs cannot select their own model or role.

#### Types & Trait Declarations
- **Structs (6):** `ModelPolicy`, `ProviderModelCaller`, `RoutedModelCaller`, `StepBudget`, `StepLimitExceeded`, `TestCircuitMockProvider`
- **Traits (1):** `ModelCaller`

#### Key Functions & Signatures (15 shown)
```rust
// private
async fn call_model(&self, context: &str) -> Result<ModelProposal, String>;
// private
async fn call_model_cancellable(&self,
        context: &str,
        cancellation: &CancellationToken,) -> Result<Model;
// private
async fn call_model_with_context(&self,
        compiled: &CompiledContext,
        cancellation: &CancellationToken,) -;
// private
async fn call_model_cancellable_with_usage(&self,
        context: &str,
        cancellation: &CancellationToken,) -> R;
// private
async fn call_model_with_context_and_usage(&self,
        compiled: &CompiledContext,
        cancellation: &Cancellatio;
// private
async fn call_model_with_context_and_usage_streaming(&self,
        compiled: &CompiledContext,
        cancellation: &C;
// private
async fn call_model_tool_free_cancellable_with_usage(&self,
        context: &str,
        cancellation: &CancellationTo;
// private
async fn call_model_tool_free_cancellable(&self,
        context: &str,
        cancellation: &CancellationToken,) -> Re;
// private
async fn call_model_with_invocation(&self,
        invocation: &crate::runtime_authorities::ModelInvocation,
        can;
// private
async fn bound_catalog_snapshot(&self) -> Option<crate::model::catalog::ModelCatalog>;
// private
fn model_name(&self) -> String;
// private
fn provider_name(&self) -> String;
// private
fn bind_role_tools(&self,
        _role: &crate::state_machine::agent::AgentRole,
        _tools: Vec<serde_json::Value>;
// pub
fn new(provider: std::sync::Arc<P>,
        model_name: impl Into<String>,
        tools: Vec<serde_json::Value>,) -> Se;
// private
fn model_name(&self) -> String;
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_step_budget_metering_and_admission`, `test_routed_caller_records_circuit_outcomes`, `test_routed_caller_waits_out_live_cooldown_on_resolve`, `arbitrary_model_does_not_fabricate_capabilities`

---

### `src/agent/profile.rs` {#src-agent-profile-rs}

- **Source Link:** [`src/agent/profile.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/profile.rs)
- **Lines of Code:** 240 (9857 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Canonical 8 role profiles, 10-field AgentProfile contract, and SHA-256 fingerprinting (AGT-01, AGT-02, D-01).  Every agent in M31A operates under an immutable strongly typed profile that explicitly specifies its role, bounds, capability envelope, context policy, and instructions.

#### Types & Trait Declarations
- **Structs (4):** `AgentProfile`, `ContextPolicy`, `ProfileOverride`, `TerminationPolicy`
- **Enums (1):** `ProfileOverrideError`

#### Key Functions & Signatures (7 shown)
```rust
// pub
fn fingerprint(&self) -> String;
// pub
fn built_in(role: AgentRole) -> Self;
// pub
fn apply_override(&self, ovr: ProfileOverride) -> Result<Self, ProfileOverrideError>;
// private
fn test_all_roles_have_valid_profiles();
// private
fn test_profile_override_step_ceiling_enforcement();
// private
fn test_profile_override_instruction_augmentation();
// private
fn test_profile_override_rejects_empty_instruction();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_all_roles_have_valid_profiles`, `test_profile_override_step_ceiling_enforcement`, `test_profile_override_instruction_augmentation`, `test_profile_override_rejects_empty_instruction`

---

### `src/agent/registry.rs` {#src-agent-registry-rs}

- **Source Link:** [`src/agent/registry.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/registry.rs)
- **Lines of Code:** 530 (20562 bytes)

#### Primary Responsibility
Open role registry: existence and metadata authority for agent roles.  ## Authority model  ```text role definition (built-in data or registered extension) ↓ RoleRegistry (existence authority: resolve / profile_for / infer) ↓ generic consumers (dispatcher, planner, compiler, verification, scheduler) ```  `AgentRole` is pure identity. Everything behavioral — prompt binding, capability envelope, verification defaults, lifecycle stage, concurrency limit, inference triggers — lives in [`RoleDefinition`] records. Adding a role registers a definition; no core `match` arm needs to learn that the role exists.  ## Safety  The registry declares *intended* envelopes; it never authorizes side effects. Enforcement stays in Rust runtime authority:  - dispatch-time envelope intersection (`calculate_eligible_capabilities`); - per-tool policy evaluation in the tool pipeline; - sandbox construction from the validated `sandbox_policy` set; - step ceilings via `AgentProfile::apply_override`.  Registration validates internal consistency (flags match the envelope,

#### Types & Trait Declarations
- **Structs (3):** `InferenceRule`, `RoleDefinition`, `RoleRegistry`
- **Enums (1):** `RoleError`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn with_builtins() -> Self;
// pub
fn global() -> &'static RwLock<RoleRegistry>;
// pub
fn global_builtin_ids_csv() -> String;
// pub
fn global_available_roles_csv() -> String;
// pub
fn register(&mut self, def: RoleDefinition) -> Result<(), RoleError>;
// pub
fn register_inference_rule(&mut self,
        capability: impl Into<String>,
        role: &AgentRole,) -> Result<(), Ro;
// pub
fn resolve(&self, id: &AgentRole) -> Option<&RoleDefinition>;
// pub
fn contains(&self, id: &AgentRole) -> bool;
// pub
fn profile_for(&self, id: &AgentRole) -> Result<AgentProfile, RoleError>;
// pub
fn infer_role_for_capabilities(&self, capabilities: &[String]) -> Option<AgentRole>;
// pub
fn first_writable_role(&self) -> Option<AgentRole>;
// pub
fn prompt_reference_for(&self, id: &AgentRole) -> PromptReference;
// pub
fn stage_for(&self, id: &AgentRole) -> Option<MissionStage>;
// pub
fn is_compatible(&self, role: &AgentRole, prompt_role: &AgentRole) -> bool;
// pub
fn read_only_flag(&self, id: &AgentRole) -> Option<bool>;
```

---

### `src/agent/registry/builtins.rs` {#src-agent-registry-builtins-rs}

- **Source Link:** [`src/agent/registry/builtins.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/registry/builtins.rs)
- **Lines of Code:** 606 (19496 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Internal implementation file.

#### Key Functions & Signatures (12 shown)
```rust
// private
fn model_policy(min_context_tokens: usize, temperature_millicelsius: u32) -> ModelPolicy;
// private
fn context_policy(default_max_tokens: usize, reserved: usize, threshold: u8) -> ContextPolicy;
// private
fn termination_policy(stall: u64, wall: u64, failures: u32) -> TerminationPolicy;
// private
fn read_caps(caps: &[&str]) -> CapabilityEnvelope;
// private
fn write_caps(caps: &[&str]) -> CapabilityEnvelope;
// private
fn full_caps(caps: &[&str]) -> CapabilityEnvelope;
// private
fn cap(id: &str, mode: CapabilityAccessMode) -> CapabilityRequirement;
// private
fn builtin_def(id: &str,
    description: &str,
    prompt_version: u32,
    stage: MissionStage,
    researcher_class: ;
// private
fn core_roles() -> Vec<RoleDefinition>;
// private
fn specialized_research_roles() -> Vec<RoleDefinition>;
// private
fn governance_roles() -> Vec<RoleDefinition>;
// pub(super)
fn builtin_role_definitions() -> Vec<RoleDefinition>;
```

---

### `src/agent/runner.rs` {#src-agent-runner-rs}

- **Source Link:** [`src/agent/runner.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/runner.rs)
- **Lines of Code:** 1990 (91480 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Seam-driven bounded step execution loop (AGT-05, D-03, D-06).  Executes bounded agent steps where 1 step equals 1 model turn cycle (model request + validation + action execution). Tool calls are metered independently, and cancellation is evaluated at step boundaries.

#### Types & Trait Declarations
- **Structs (7):** `ActionRequest`, `ActionResult`, `AgentStepRecord`, `FailingDispatcher`, `MockActionDispatcher`, `MockModelCaller`, `WorkerRunner`
- **Traits (1):** `ActionDispatcher`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn with_prompt_provenance(mut self,
        prov: crate::prompt::provenance::PromptInvocationProvenance,) -> Self;
// pub
fn compute_action_fingerprint(tool_name: &str, params: &serde_json::Value) -> String;
// pub
fn canonicalize_json_for_fingerprint(val: &serde_json::Value) -> String;
// private
async fn dispatch(&self, action: &ActionRequest) -> Result<ActionResult, String>;
// private
async fn dispatch_action(&self,
        action: &crate::agent::action::AgentAction,) -> Result<crate::agent::action::Age;
// pub
fn validate_workspace_path(workspace_root: &std::path::Path,
    raw_path: &str,) -> Result<std::path::PathBuf, String>;
// pub
fn extract_all_action_paths(tool_name: &str, params: &serde_json::Value) -> Vec<String>;
// pub
fn new(mission_id: MissionId,
        agent_id: AgentId,
        task_id: TaskId,
        profile: AgentProfile,
       ;
// pub
fn new_isolated_test(mission_id: MissionId,
        agent_id: AgentId,
        task_id: TaskId,
        profile: AgentPr;
// pub
fn with_workspace_root(mut self, root: impl Into<std::path::PathBuf>) -> Self;
// pub
fn with_pause_token(mut self, token: tokio_util::sync::CancellationToken) -> Self;
// pub
fn with_target_surface(mut self, surface: crate::kernel::change::ChangeSurface) -> Self;
// pub
fn with_context_compiler(mut self, compiler: Arc<dyn ContextCompiler>) -> Self;
// pub
fn with_prompt_ref(mut self, prompt_ref: crate::prompt::PromptReference) -> Self;
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_runner_executes_action_then_completion`, `test_runner_rejects_premature_completion_without_mutations`, `test_runner_step_budget_exhaustion`, `test_runner_step_boundary_cancellation`, `test_runner_rejects_repeated_failing_action`

---

### `src/agent/supervisor.rs` {#src-agent-supervisor-rs}

- **Source Link:** [`src/agent/supervisor.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/agent/supervisor.rs)
- **Lines of Code:** 579 (21518 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Supervised async worker lifecycle, panic containment, and dual timeouts (AGT-05, D-05, D-07, D-08).  Owns async worker execution inside Tokio tasks, guaranteeing that worker thread panics are converted into structured failure evidence without crashing the M31A process, and that cancellation and timeouts await confirmed worker termination (Law 8).

#### Types & Trait Declarations
- **Structs (3):** `ExecutionActivityTracker`, `FailureEvidence`, `WorkerSupervisor`
- **Enums (3):** `AgentOutcome`, `ExecutionActivity`, `FailureClass`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn is_success(&self) -> bool;
// private
fn default() -> Self;
// pub
fn new(last_progress_at: Arc<RwLock<DateTime<Utc>>>) -> Self;
// pub
async fn mark_idle(&self);
// pub
async fn mark_inference_start(&self);
// pub
async fn mark_tool_start(&self, tool_name: &str);
// pub
async fn touch(&self);
// pub
async fn record_token_usage(&self, usage: &crate::model::types::TokenUsage);
// pub
async fn total_token_usage(&self) -> crate::model::types::TokenUsage;
// pub
async fn current_activity(&self) -> ExecutionActivity;
// pub
fn last_progress_handle(&self) -> Arc<RwLock<DateTime<Utc>>>;
// pub
fn new(agent_id: AgentId,
        task_id: TaskId,
        cancellation_token: CancellationToken,
        stall_timeout:;
// pub
fn progress_tracker(&self) -> Arc<RwLock<DateTime<Utc>>>;
// pub
fn activity_tracker(&self) -> Arc<ExecutionActivityTracker>;
// pub
async fn touch_progress(&self);
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_supervisor_normal_success`, `test_supervisor_panic_containment`, `test_supervisor_cooperative_cancellation`, `test_supervisor_stall_detection`, `test_supervisor_wall_clock_timeout`, `test_supervisor_inference_active_tolerates_slow_inference`

---
