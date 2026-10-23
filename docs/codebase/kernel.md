# Kernel Core & Seams

> **Architectural Layer:** L0 Kernel  
> **Source Directory:** `src/kernel`  
> **File Count:** 16 source files  

Core seams, architectural invariants, cancellation tokens, hashes, and memory boundaries.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [cancellation.rs](#src-kernel-cancellation-rs) | 172 | `MissionRuntime` | Cancellation token hierarchy (KRN-04)  Per KRN-04 and RESEARCH.md Patt... |
| [change.rs](#src-kernel-change-rs) | 591 | `ChangeProposal, ChangeProposalId, ChangeProvenanceRecord` | Canonical change proposal contracts and software modification primitiv... |
| [hash.rs](#src-kernel-hash-rs) | 33 | `Functions/Traits` | Cryptographic hashing primitives (L0 Kernel).  Provides canonical SHA-... |
| [invariants.rs](#src-kernel-invariants-rs) | 375 | `RuntimeInvariants` | Runtime invariant assertions (KRN-05)  Per D-18, kernel/ owns only cro... |
| [memory.rs](#src-kernel-memory-rs) | 665 | `EngineeringAssumption, EngineeringDecision, EngineeringMemorySnapshot` | Canonical kernel domain types for Long-Horizon Engineering Memory.  Ke... |
| [mod.rs](#src-kernel-mod-rs) | 34 | `Functions/Traits` | Kernel module - cross-cutting runtime invariants and lifecycle concern... |
| [plan.rs](#src-kernel-plan-rs) | 876 | `CandidatePlan, CandidatePlanAssumption, CandidateTask` | Canonical executable candidate plan contracts and verification primiti... |
| [context.rs](#src-kernel-seams-context-rs) | 525 | `CompiledContext, ContextCompilationContract, ContextCompilationRequest` | Subsystem component |
| [escalation.rs](#src-kernel-seams-escalation-rs) | 213 | `EscalationRequest, EscalationRequestId, PendingEscalation` | Subsystem component |
| [execution.rs](#src-kernel-seams-execution-rs) | 336 | `WorkExecutionHandle, WorkExecutionRequest, WorkExecutionResult` | Subsystem component |
| [mod.rs](#src-kernel-seams-mod-rs) | 55 | `Functions/Traits` | Neutral cross-layer seam contracts (AD-007).  This module defines the ... |
| [planner.rs](#src-kernel-seams-planner-rs) | 857 | `PlanRequest, PlanResponse, ReplanRequest` | Subsystem component |
| [policy.rs](#src-kernel-seams-policy-rs) | 364 | `PolicyDecisionContract, PolicyEvaluationRequest, PolicyDecision` | Subsystem component |
| [recovery.rs](#src-kernel-seams-recovery-rs) | 275 | `FailureClassificationRequest, RecoveryStrategyRequest, FailureClassification` | Subsystem component |
| [scheduler.rs](#src-kernel-seams-scheduler-rs) | 133 | `ReadyWorkResponse, WorkItem, SchedulerError` | Subsystem component |
| [verifier.rs](#src-kernel-seams-verifier-rs) | 58 | `TaskVerificationRequest, CompletionGateOutcome, VerificationError` | Subsystem component |

---

### `src/kernel/cancellation.rs` {#src-kernel-cancellation-rs}

- **Source Link:** [`src/kernel/cancellation.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/kernel/cancellation.rs)
- **Lines of Code:** 172 (4985 bytes)
- **Runtime Properties:** 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Cancellation token hierarchy (KRN-04)  Per KRN-04 and RESEARCH.md Pattern 3, parent-child cancellation tokens for ownership chain propagation using tokio-util's CancellationToken.

#### Types & Trait Declarations
- **Structs (1):** `MissionRuntime`

#### Key Functions & Signatures (14 shown)
```rust
// pub
fn new() -> Self;
// pub
fn token(&self) -> &CancellationToken;
// pub
fn spawn_child(&self) -> CancellationToken;
// pub
fn is_cancelled(&self) -> bool;
// pub
fn shutdown(&self);
// private
fn default() -> Self;
// private
fn test_mission_runtime_new();
// private
fn test_spawn_child();
// private
fn test_parent_cancels_children();
// private
fn test_child_cancellation_isolated();
// private
fn test_is_cancelled_observable();
// private
async fn test_cancellation_propagation_in_select();
// private
async fn test_multiple_levels_of_children();
// private
async fn test_shutdown_cancels_all_descendants();
```

#### Unit Verification (8 inline tests)
Tests defined within module:
`test_mission_runtime_new`, `test_spawn_child`, `test_parent_cancels_children`, `test_child_cancellation_isolated`, `test_is_cancelled_observable`, `test_cancellation_propagation_in_select`, `test_multiple_levels_of_children`, `test_shutdown_cancels_all_descendants`

---

### `src/kernel/change.rs` {#src-kernel-change-rs}

- **Source Link:** [`src/kernel/change.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/kernel/change.rs)
- **Lines of Code:** 591 (17679 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Canonical change proposal contracts and software modification primitives.  Kernel-owned contracts defining implementation hypotheses, change surfaces, file preconditions, multi-file mutation proposals, and change provenance.  Core principle: The model proposes. The runtime decides. The model formulates change proposals; the runtime validates, authorizes, atomically applies, re-observes, verifies, and reviews them.

#### Types & Trait Declarations
- **Structs (9):** `ChangeProposal`, `ChangeProposalId`, `ChangeProvenanceRecord`, `ChangeSurface`, `DiffReviewReport`, `FileMutationProposal`, `FilePrecondition`, `ImplementationHypothesis`, `ReconciliationReport`
- **Enums (3):** `DiffReviewViolation`, `FileMutationOp`, `ReconciliationViolation`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn from_uuid(u: Uuid) -> Self;
// pub
fn as_bytes(&self) -> &[u8;
// private
fn default() -> Self;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// pub
fn new(problem: impl Into<String>,
        expected_cause: impl Into<String>,
        proposed_change: impl Into<String>;
// pub
fn with_affected_components(mut self, components: Vec<String>) -> Self;
// pub
fn new(required_files: Vec<String>) -> Self;
// pub
fn all_target_files(&self) -> Vec<String>;
// pub
fn contains_path(&self, path: &str) -> bool;
// pub
fn exists(path: impl Into<String>) -> Self;
// pub
fn exists_with_hash(path: impl Into<String>, expected_hash: impl Into<String>) -> Self;
// pub
fn must_not_exist(path: impl Into<String>) -> Self;
// pub
fn with_expected_symbols(mut self, symbols: Vec<String>) -> Self;
// pub
fn new(path: impl Into<String>,
        operation: FileMutationOp,
        rationale: impl Into<String>,) -> Self;
```

---

### `src/kernel/hash.rs` {#src-kernel-hash-rs}

- **Source Link:** [`src/kernel/hash.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/kernel/hash.rs)
- **Lines of Code:** 33 (962 bytes)

#### Primary Responsibility
Cryptographic hashing primitives (L0 Kernel).  Provides canonical SHA-256 digest computations and hex formatting shared across artifacts, release verification, dedup, and state hashing.

#### Key Functions & Signatures (2 shown)
```rust
// pub
fn sha256_hex(data: &[u8]) -> String;
// private
fn test_sha256_hex_known_vector();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_sha256_hex_known_vector`

---

### `src/kernel/invariants.rs` {#src-kernel-invariants-rs}

- **Source Link:** [`src/kernel/invariants.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/kernel/invariants.rs)
- **Lines of Code:** 375 (12630 bytes)

#### Primary Responsibility
Runtime invariant assertions (KRN-05)  Per D-18, kernel/ owns only cross-cutting runtime invariants. Per KRN-05, runtime invariants are enforced and directly tested.

#### Types & Trait Declarations
- **Structs (1):** `RuntimeInvariants`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn assert_task_not_blocked(&self, task_status: &TaskState);
// pub
fn assert_task_not_succeeded(&self, task_status: &TaskState);
// pub
fn assert_mission_not_completed(&self, mission_status: &MissionState);
// pub
fn assert_not_terminal(&self, task_status: &TaskState);
// pub
fn assert_side_effect_has_policy(&self, tool_name: &str, policy_decided: bool);
// pub
fn assert_task_not_blocked(task_status: &TaskState);
// pub
fn assert_task_not_succeeded(task_status: &TaskState);
// pub
fn assert_mission_not_completed(mission_status: &MissionState);
// pub
fn assert_not_terminal(task_status: &TaskState);
// pub
fn assert_side_effect_has_policy(tool_name: &str, policy_decided: bool);
// pub
fn is_protected_component(comp: &str) -> bool;
// pub
fn contains_protected_component(path: &std::path::Path) -> bool;
// pub
fn is_sensitive_or_credential_path(path: &std::path::Path) -> bool;
// pub
fn is_protected_or_sensitive_path(path: &std::path::Path) -> bool;
// private
fn test_assert_task_not_blocked_passes_for_valid_states();
```

#### Unit Verification (11 inline tests)
Tests defined within module:
`test_assert_task_not_blocked_passes_for_valid_states`, `test_assert_task_not_blocked_panics_for_blocked`, `test_assert_task_not_succeeded_passes_for_valid_states`, `test_assert_task_not_succeeded_panics_for_succeeded`, `test_assert_mission_not_completed_passes_for_valid_states`, `test_assert_mission_not_completed_panics_for_completed`, `test_assert_not_terminal_passes_for_non_terminal_states`, `test_assert_not_terminal_panics_for_terminal_states`, `test_assert_side_effect_has_policy_passes_when_true`, `test_assert_side_effect_has_policy_panics_when_false`...

---

### `src/kernel/memory.rs` {#src-kernel-memory-rs}

- **Source Link:** [`src/kernel/memory.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/kernel/memory.rs)
- **Lines of Code:** 665 (19809 bytes)

#### Primary Responsibility
Canonical kernel domain types for Long-Horizon Engineering Memory.  Kernel-owned pure domain models for: - Architectural Decisions - Epistemic Assumptions - Failure Diagnoses &amp; Attempt Memory - Durable Review Findings - Revision-Aware Verification Records  Subordinate to runtime state and repository reality.

#### Types & Trait Declarations
- **Structs (7):** `EngineeringAssumption`, `EngineeringDecision`, `EngineeringMemorySnapshot`, `FailureDiagnosisRecord`, `FileHashRecord`, `ReviewFindingRecord`, `VerificationRecord`
- **Enums (7):** `AssumptionStatus`, `DecisionStatus`, `MemoryScope`, `RepairStatus`, `ReviewFindingSeverity`, `ReviewFindingStatus`, `VerificationValidity`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn is_authoritative(&self) -> bool;
// pub
fn can_transition_to(&self, new_status: DecisionStatus) -> bool;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn as_str(&self) -> &'static str;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn new(id: impl Into<String>,
        scope: MemoryScope,
        title: impl Into<String>,
        context: impl Into<S;
// pub
fn with_mission_id(mut self, mission_id: MissionId) -> Self;
// pub
fn with_status(mut self, status: DecisionStatus) -> Self;
// pub
fn with_alternatives(mut self, alts: Vec<String>) -> Self;
// pub
fn with_consequences(mut self, cons: Vec<String>) -> Self;
// pub
fn with_linked_files(mut self, files: Vec<String>) -> Self;
// pub
fn with_linked_requirements(mut self, reqs: Vec<String>) -> Self;
// pub
fn as_str(&self) -> &'static str;
```

---

### `src/kernel/mod.rs` {#src-kernel-mod-rs}

- **Source Link:** [`src/kernel/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/kernel/mod.rs)
- **Lines of Code:** 34 (1341 bytes)
- **Runtime Properties:** 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Kernel module - cross-cutting runtime invariants and lifecycle concerns (D-18)  Per D-18, kernel/ owns cross-cutting runtime invariants, lifecycle concerns, and the neutral cross-layer seam contracts (AD-007).

---

### `src/kernel/plan.rs` {#src-kernel-plan-rs}

- **Source Link:** [`src/kernel/plan.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/kernel/plan.rs)
- **Lines of Code:** 876 (27735 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Canonical executable candidate plan contracts and verification primitives (PLN-01, PLN-05, D-01..D-04).  Kernel-owned contracts defining planner proposals, task identity, dependencies, capabilities, verification strategies, and resource estimates.  Core principle: The model proposes. The runtime decides. The planner produces candidate plan proposals; the runtime scheduler/DAG decides whether to materialize and execute them.

#### Types & Trait Declarations
- **Structs (8):** `CandidatePlan`, `CandidatePlanAssumption`, `CandidateTask`, `CandidateTaskKey`, `CapabilityRequirement`, `PlanRevisionRecord`, `ResourceEstimate`, `TaskResult`
- **Enums (5):** `CapabilityAccessMode`, `Helper`, `ReplanningTrigger`, `TaskRiskLevel`, `VerificationStrategy`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(summary: impl Into<String>) -> Self;
// pub
fn new(id: impl Into<String>) -> Self;
// pub
fn as_str(&self) -> &str;
// private
fn deref(&self) -> &Self::Target;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(s: &str) -> Self;
// private
fn from(s: String) -> Self;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn deserialize(deserializer: D) -> Result<Self, D::Error>
    where
        D: serde::Deserializer<'de>,;
// pub
fn new(id: impl Into<String>, mode: CapabilityAccessMode) -> Self;
// pub
fn validate(&self) -> Result<(), String>;
// pub
fn composite(strategies: Vec<VerificationStrategy>) -> Result<Self, String>;
// pub
fn depth(&self) -> usize;
// pub
fn strategy_name(&self) -> &'static str;
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_candidate_task_key_basic`, `test_capability_requirement_validation`, `test_verification_strategy_composite_depth_bound`, `test_resource_estimate_validation`, `test_candidate_plan_full_roundtrip_serde`

---

### `src/kernel/seams/context.rs` {#src-kernel-seams-context-rs}

- **Source Link:** [`src/kernel/seams/context.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/kernel/seams/context.rs)
- **Lines of Code:** 525 (18466 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (7):** `CompiledContext`, `ContextCompilationContract`, `ContextCompilationRequest`, `ContextSectionContract`, `OmittedEvidenceContract`, `SelectedEvidenceContract`, `StepRecordDto`
- **Enums (2):** `ContextError`, `PromptSelectionSource`
- **Traits (1):** `ContextCompiler`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(section_id: impl Into<String>,
        original_tokens: usize,
        final_tokens: usize,
        compaction_ac;
// pub
fn as_str(&self) -> &'static str;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(revision: u32,
        total_budget: usize,
        reserved_headroom: usize,
        compiled_tokens: usize,
   ;
// pub
fn with_evidence(mut self,
        selected: Vec<SelectedEvidenceContract>,
        omitted: Vec<OmittedEvidenceContract;
// pub
fn new(mission_id: MissionId, task_id: TaskId, max_tokens: usize) -> Self;
// pub
fn with_interactive_messages(mut self, messages: Vec<ChatMessage>) -> Self;
// pub
fn with_objectives(mut self,
        mission_obj: Option<String>,
        task_obj: Option<String>,) -> Self;
// pub
fn with_mission_objective(mut self, obj: impl Into<String>) -> Self;
// pub
fn with_task_objective(mut self, obj: impl Into<String>) -> Self;
// pub
fn with_task_description(mut self, desc: impl Into<String>) -> Self;
// pub
fn with_task_criteria(mut self, criteria: Vec<String>) -> Self;
// pub
fn with_task_requirement_keys(mut self, keys: Vec<String>) -> Self;
// pub
fn with_task_assumptions(mut self, assumptions: Vec<String>) -> Self;
// pub
fn with_upstream_charter(mut self, charter: impl Into<String>) -> Self;
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_context_dto_serde`

---

### `src/kernel/seams/escalation.rs` {#src-kernel-seams-escalation-rs}

- **Source Link:** [`src/kernel/seams/escalation.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/kernel/seams/escalation.rs)
- **Lines of Code:** 213 (6566 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (3):** `EscalationRequest`, `EscalationRequestId`, `PendingEscalation`
- **Enums (2):** `EscalationError`, `EscalationResponse`
- **Traits (1):** `EscalationChannel`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_uuid(uuid: Uuid) -> Self;
// private
fn default() -> Self;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn new(request: EscalationRequest, requested_at: DateTime<Utc>) -> Self;
// pub
fn evaluate_timeout(&self, now: DateTime<Utc>) -> bool;
// pub
fn resolve_timeout(&self) -> (PolicyDecision, EventType);
// private
async fn request_escalation(&self,
        req: EscalationRequest,) -> Result<EscalationRequestId, EscalationError>;
// private
async fn check_response(&self,
        id: EscalationRequestId,) -> Result<Option<EscalationResponse>, EscalationError>;
// private
fn test_escalation_request_id_display_and_parse();
// private
fn test_escalation_request_serde();
// private
fn test_pending_escalation_timeout_and_resolution();
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_escalation_request_id_display_and_parse`, `test_escalation_request_serde`, `test_pending_escalation_timeout_and_resolution`, `test_pending_escalation_without_timeout_never_expires`, `test_escalation_response_serde`

---

### `src/kernel/seams/execution.rs` {#src-kernel-seams-execution-rs}

- **Source Link:** [`src/kernel/seams/execution.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/kernel/seams/execution.rs)
- **Lines of Code:** 336 (11387 bytes)
- **Runtime Properties:** 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (3):** `WorkExecutionHandle`, `WorkExecutionRequest`, `WorkExecutionResult`
- **Enums (1):** `ExecutionError`
- **Traits (1):** `WorkerDispatcher`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn eq(&self, other: &Self) -> bool;
// pub
fn new(mission_id: MissionId,
        task_id: TaskId,
        agent_id: AgentId,
        context_id: impl Into<String>,;
// pub
fn with_objectives(mut self,
        mission_obj: Option<String>,
        task_obj: Option<String>,) -> Self;
// pub
fn with_mission_objective(mut self, obj: impl Into<String>) -> Self;
// pub
fn with_task_objective(mut self, obj: impl Into<String>) -> Self;
// pub
fn with_workspace_root(mut self, root: impl Into<PathBuf>) -> Self;
// pub
fn with_task_description(mut self, desc: impl Into<String>) -> Self;
// pub
fn with_task_description_opt(mut self, desc: Option<String>) -> Self;
// pub
fn with_task_criteria(mut self, criteria: Vec<String>) -> Self;
// pub
fn with_requirement_keys(mut self, keys: Vec<String>) -> Self;
// pub
fn with_task_assumptions(mut self, assumptions: Vec<String>) -> Self;
// pub
fn with_upstream_charter_opt(mut self, charter: Option<String>) -> Self;
// pub
fn with_upstream_architecture_opt(mut self, architecture: Option<String>) -> Self;
// pub
fn with_upstream_requirements(mut self, requirements: Vec<String>) -> Self;
// pub
fn with_upstream_assumptions(mut self, assumptions: Vec<String>) -> Self;
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_execution_dto_serde`

---

### `src/kernel/seams/mod.rs` {#src-kernel-seams-mod-rs}

- **Source Link:** [`src/kernel/seams/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/kernel/seams/mod.rs)
- **Lines of Code:** 55 (2164 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Neutral cross-layer seam contracts (AD-007).  This module defines the shared interface traits that lower-level subsystems (scheduler, agent, verification, policy, recovery, planning) implement and that the higher-level AutonomyController consumes.  Dependency direction: kernel::seams  ← depends on: ids, state, planning, context, model, prompt, events controller     ← depends on: kernel::seams  (downward only) scheduler      ← depends on: kernel::seams  (downward only) agent          ← depends on: kernel::seams  (downward only) verification   ← depends on: kernel::seams  (downward only) policy         ← depends on: kernel::seams  (downward only) recovery       ← depends on: kernel::seams  (downward only)  No module in kernel::seams imports from controller, scheduler impl, agent impl, verification impl, policy impl, or UI/CLI/TUI/persistence.

---

### `src/kernel/seams/planner.rs` {#src-kernel-seams-planner-rs}

- **Source Link:** [`src/kernel/seams/planner.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/kernel/seams/planner.rs)
- **Lines of Code:** 857 (30377 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (7):** `PlanRequest`, `PlanResponse`, `ReplanRequest`, `ReplanResponse`, `ResolvedRequestIntent`, `UpstreamPlanContext`, `UpstreamRoadmapPhase`
- **Enums (2):** `ObjectiveClassification`, `PlanError`
- **Traits (1):** `PlanService`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn is_read_only(self) -> bool;
// pub
fn expects_executable_tasks(self) -> bool;
// pub
fn new(raw_prompt: impl Into<String>,
        classification: ObjectiveClassification,
        is_mutation_forbidden: bo;
// pub
fn is_read_only(&self) -> bool;
// pub
fn with_constraint(mut self, constraint: impl Into<String>) -> Self;
// pub
fn with_ambiguity(mut self, ambiguity: impl Into<String>) -> Self;
// pub
fn new(mission_id: MissionId, objective: impl Into<String>) -> Self;
// pub
fn with_resolved_intent(mut self, intent: ResolvedRequestIntent) -> Self;
// pub
fn with_upstream_context(mut self, ctx: UpstreamPlanContext) -> Self;
// pub
fn with_classification(mut self,
        classification: impl Into<String>,
        is_read_only: bool,) -> Self;
// pub
fn with_mutation_forbidden(mut self, forbidden: bool) -> Self;
// pub
fn resolved_contract(&self) -> ResolvedRequestIntent;
// pub
fn extract_non_filename_tokens(text: &str) -> Vec<String>;
// pub
fn tokens_contain_word(tokens: &[String], word: &str) -> bool;
// pub
fn is_mutation_forbidden(objective: &str) -> bool;
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_plan_dto_serde`, `test_replan_dto_serde`

---

### `src/kernel/seams/policy.rs` {#src-kernel-seams-policy-rs}

- **Source Link:** [`src/kernel/seams/policy.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/kernel/seams/policy.rs)
- **Lines of Code:** 364 (12214 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (2):** `PolicyDecisionContract`, `PolicyEvaluationRequest`
- **Enums (3):** `PolicyDecision`, `PolicyError`, `ResolvedAction`
- **Traits (1):** `PolicyGate`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(mission_id: MissionId, task_id: TaskId, tool_or_action: impl Into<String>) -> Self;
// pub
fn with_agent_id(mut self, id: AgentId) -> Self;
// pub
fn with_role(mut self, role: AgentRole) -> Self;
// pub
fn with_autonomy_mode(mut self, mode: AutonomyMode) -> Self;
// pub
fn with_workspace(mut self, ws: PathBuf) -> Self;
// pub
fn with_target_paths(mut self, paths: Vec<PathBuf>) -> Self;
// pub
fn with_arguments(mut self, args: serde_json::Value) -> Self;
// pub
fn with_effective_risk(mut self, risk: impl Into<String>) -> Self;
// pub
fn with_authorization(mut self, id: impl Into<String>) -> Self;
// pub
fn with_policy_hash(mut self, hash: impl Into<String>) -> Self;
// pub
fn resolve_decision(mode: AutonomyMode,
    decision: PolicyDecision,
    reason: &str,
    has_escalation_channel: bool;
// pub
fn new(decision: PolicyDecision,
        matched_rule_id: Option<String>,
        matched_layer: Option<String>,
       ;
// private
async fn evaluate(&self, req: PolicyEvaluationRequest) -> Result<PolicyDecision, PolicyError>;
// private
async fn evaluate_record(&self,
        req: PolicyEvaluationRequest,) -> Result<(PolicyDecision, Option<PolicyDecisionC;
// private
fn policy_hash(&self) -> Option<String>;
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_policy_resolution_unattended_never_allows_ask`, `test_policy_resolution_all_five_modes`, `test_policy_request_and_decision_serde_roundtrip`

---

### `src/kernel/seams/recovery.rs` {#src-kernel-seams-recovery-rs}

- **Source Link:** [`src/kernel/seams/recovery.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/kernel/seams/recovery.rs)
- **Lines of Code:** 275 (8956 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (2):** `FailureClassificationRequest`, `RecoveryStrategyRequest`
- **Enums (3):** `FailureClassification`, `RecoveryAction`, `RecoveryError`
- **Traits (1):** `RecoveryEngine`

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn is_retryable(&self) -> bool;
// pub
fn default_retry_limit(&self) -> usize;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(mission_id: MissionId,
        task_id: TaskId,
        failure_class: FailureClassification,
        retry_count;
// pub
fn with_error_message(mut self, msg: impl Into<String>) -> Self;
// private
async fn classify_failure(&self,
        req: FailureClassificationRequest,) -> Result<FailureClassification, RecoveryEr;
// private
async fn determine_recovery(&self,
        req: RecoveryStrategyRequest,) -> Result<RecoveryAction, RecoveryError>;
// private
fn test_recovery_dto_serde();
// private
fn test_failure_classification_serde_all_15_classes();
// private
fn test_non_retryable_classes_have_zero_budget();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_recovery_dto_serde`, `test_failure_classification_serde_all_15_classes`, `test_non_retryable_classes_have_zero_budget`

---

### `src/kernel/seams/scheduler.rs` {#src-kernel-seams-scheduler-rs}

- **Source Link:** [`src/kernel/seams/scheduler.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/kernel/seams/scheduler.rs)
- **Lines of Code:** 133 (4331 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (2):** `ReadyWorkResponse`, `WorkItem`
- **Enums (1):** `SchedulerError`
- **Traits (1):** `WorkScheduler`

#### Key Functions & Signatures (9 shown)
```rust
// private
async fn materialize_plan(&self,
        _mission_id: MissionId,
        _plan: &CandidatePlan,) -> Result<TaskGraphId, ;
// private
async fn reconcile_plan(&self,
        mission_id: MissionId,
        plan: &CandidatePlan,) -> Result<TaskGraphId, Sche;
// private
async fn find_ready_work(&self,
        mission_id: MissionId,) -> Result<ReadyWorkResponse, SchedulerError>;
// private
async fn is_work_complete(&self, mission_id: MissionId) -> Result<bool, SchedulerError>;
// private
async fn mark_task_started(&self,
        task_id: TaskId,
        agent_id: AgentId,) -> Result<(), SchedulerError>;
// private
async fn mark_task_completed(&self,
        _task_id: TaskId,
        _result: Option<TaskResult>,) -> Result<(), Schedu;
// private
async fn mark_task_failed(&self,
        _task_id: TaskId,
        _error_message: String,
        _is_recoverable: bool;
// private
async fn mark_task_skipped(&self,
        _task_id: TaskId,
        _reason: String,) -> Result<(), SchedulerError>;
// private
fn test_work_item_serde();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_work_item_serde`

---

### `src/kernel/seams/verifier.rs` {#src-kernel-seams-verifier-rs}

- **Source Link:** [`src/kernel/seams/verifier.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/kernel/seams/verifier.rs)
- **Lines of Code:** 58 (1514 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (1):** `TaskVerificationRequest`
- **Enums (3):** `CompletionGateOutcome`, `VerificationError`, `VerificationOutcome`
- **Traits (1):** `VerificationEngine`

#### Key Functions & Signatures (3 shown)
```rust
// private
async fn verify_task(&self,
        req: TaskVerificationRequest,) -> Result<VerificationOutcome, VerificationError>;
// private
async fn verify_completion_gate(&self,
        mission_id: MissionId,) -> Result<CompletionGateOutcome, VerificationErro;
// private
fn test_verifier_dto_serde();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_verifier_dto_serde`

---
