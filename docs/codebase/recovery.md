# Recovery & Replanning

> **Architectural Layer:** L7 Recovery  
> **Source Directory:** `src/recovery`  
> **File Count:** 5 source files  

Differential replanning, failure diagnosis, and automated remediation.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [adapter.rs](#src-recovery-adapter-rs) | 503 | `ProductionRecoveryEngine` | Subsystem component |
| [budget.rs](#src-recovery-budget-rs) | 1038 | `BackoffConfig, RecoveryAttemptRecord, RecoveryBudgetTracker` | Layered Recovery Budget Tracker &amp; Durable Audit Store (FLC-02, FLC... |
| [classifier.rs](#src-recovery-classifier-rs) | 357 | `FailureClassifier` | 15-Class Failure Classifier with Deterministic Rules Engine and Tier 7... |
| [mod.rs](#src-recovery-mod-rs) | 22 | `Functions/Traits` | Failure Controller, Layered Recovery, and Replanning Subsystem.  Provi... |
| [replan.rs](#src-recovery-replan-rs) | 447 | `DifferentialReplanEngine, DifferentialReplanOutcome, DifferentialReplanRequest` | Differential DAG Replanning Engine with Task Completion Preservation (... |

---

### `src/recovery/adapter.rs` {#src-recovery-adapter-rs}

- **Source Link:** [`src/recovery/adapter.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/recovery/adapter.rs)
- **Lines of Code:** 503 (20685 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (1):** `ProductionRecoveryEngine`

#### Key Functions & Signatures (12 shown)
```rust
// private
fn default() -> Self;
// pub
fn new(pool: Option<SqlitePool>) -> Self;
// pub
fn with_components(classifier: FailureClassifier,
        budget_tracker: RecoveryBudgetTracker,
        pool: Option<Sq;
// pub
fn with_diagnostician(mut self, diagnostician: Arc<ModelDiagnostician>) -> Self;
// pub
fn budget_tracker(&self) -> &RecoveryBudgetTracker;
// pub
fn classifier(&self) -> &FailureClassifier;
// pub
fn diagnostician(&self) -> &ModelDiagnostician;
// private
async fn classify_failure(&self,
        req: FailureClassificationRequest,) -> Result<FailureClassification, RecoveryEr;
// private
async fn determine_recovery(&self,
        req: RecoveryStrategyRequest,) -> Result<RecoveryAction, RecoveryError>;
// private
async fn test_determine_recovery_retries_compiler_error_without_structured_fix();
// private
async fn test_determine_recovery_replans_on_budget_exhaustion();
// private
async fn test_determine_recovery_aborts_non_retryable_failure();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_determine_recovery_retries_compiler_error_without_structured_fix`, `test_determine_recovery_replans_on_budget_exhaustion`, `test_determine_recovery_aborts_non_retryable_failure`

---

### `src/recovery/budget.rs` {#src-recovery-budget-rs}

- **Source Link:** [`src/recovery/budget.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/recovery/budget.rs)
- **Lines of Code:** 1038 (40240 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
Layered Recovery Budget Tracker &amp; Durable Audit Store (FLC-02, FLC-05, D-06).  Enforces class-specific retry caps layered strictly under global task and mission recovery ceilings. Deterministically non-retryable classes (`Permission`, `Policy`) have zero retry budget. Transient failures calculate bounded exponential backoff with jitter and honor `Retry-After`. Every attempt is recorded in the SQLite `recovery_attempts` table prior to executing state transitions.

#### Types & Trait Declarations
- **Structs (4):** `BackoffConfig`, `RecoveryAttemptRecord`, `RecoveryBudgetTracker`, `SemanticFailureSignature`
- **Enums (2):** `AttemptStrategyClassification`, `BudgetEvaluation`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn new(failure_class: FailureClassification,
        target_domain: impl Into<String>,
        normalized_error: impl In;
// pub
fn is_equivalent(&self, other: &Self) -> bool;
// pub
fn normalize_error_message(err: &str) -> String;
// pub
fn extract_target_domain(err_msg: &str, affected_files: &[String]) -> String;
// pub
fn compute_mutation_fingerprint(proposal: &crate::kernel::change::ChangeProposal) -> String;
// private
fn default() -> Self;
// pub
fn new(task_retry_ceiling: usize, mission_retry_ceiling: usize) -> Self;
// pub
fn with_backoff_config(mut self, config: BackoffConfig) -> Self;
// pub
fn with_circuit_breaker_threshold(mut self, threshold: usize) -> Self;
// pub
fn classify_attempt(&self,
        task_id: TaskId,
        fingerprint: &str,) -> AttemptStrategyClassification;
// pub
fn classify_attempt_with_mission(&self,
        mission_id: Option<MissionId>,
        task_id: TaskId,
        fingerpr;
// pub
fn record_attempt_fingerprint(&self, task_id: TaskId, fingerprint: impl Into<String>);
// pub
fn record_mission_attempt_fingerprint(&self,
        mission_id: MissionId,
        task_id: TaskId,
        fingerprint;
// pub
fn record_failure_signature(&self, mission_id: MissionId, sig: SemanticFailureSignature);
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_non_retryable_evaluations`, `test_class_budget_exhaustion`, `test_exponential_backoff_calculation`, `test_retry_intelligence_and_repeated_attempt_rejection`

---

### `src/recovery/classifier.rs` {#src-recovery-classifier-rs}

- **Source Link:** [`src/recovery/classifier.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/recovery/classifier.rs)
- **Lines of Code:** 357 (13497 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
15-Class Failure Classifier with Deterministic Rules Engine and Tier 7 Fallback (FLC-01, D-05).  Evaluates exit codes, compiler/test outputs, sandbox rejections, and policy denials against high-precedence deterministic rules across all 15 specification failure classes: Transient, Timeout, Permission, Policy, Environment, Dependency, Compilation, Test, ToolContract, Model, Context, ResourceLimit, RepositoryState, Architecture, Unknown. Ambiguous or unclassified errors fall back to the Tier 7 Model-Based Diagnostician.

#### Types & Trait Declarations
- **Structs (1):** `FailureClassifier`

#### Key Functions & Signatures (7 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_diagnostician(diagnostician: ModelDiagnostician) -> Self;
// pub
fn classify_deterministic(exit_code: Option<i32>,
        error_msg: &str,) -> FailureClassification;
// pub
async fn classify(&self, exit_code: Option<i32>, error_msg: &str) -> FailureClassification;
// private
fn test_all_15_deterministic_classes();
// private
async fn test_tier_7_diagnostician_fallback();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_all_15_deterministic_classes`, `test_tier_7_diagnostician_fallback`

---

### `src/recovery/mod.rs` {#src-recovery-mod-rs}

- **Source Link:** [`src/recovery/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/recovery/mod.rs)
- **Lines of Code:** 22 (845 bytes)

#### Primary Responsibility
Failure Controller, Layered Recovery, and Replanning Subsystem.  Provides deterministic failure classification, layered class-specific recovery budgets with exponential backoff and SQLite audit, differential DAG replanning with task completion preservation, ReplanScope classification, and ReplanningTrigger provenance tracking.

---

### `src/recovery/replan.rs` {#src-recovery-replan-rs}

- **Source Link:** [`src/recovery/replan.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/recovery/replan.rs)
- **Lines of Code:** 447 (16575 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Differential DAG Replanning Engine with Task Completion Preservation (FLC-04, D-08).  Triggered by `RecoveryAction::Replan` on invalidated assumptions, repeated failures, architectural changes, or state drift. Preserves verified completed tasks (`TaskState::Completed`) whose semantic fingerprints remain unchanged, retaining their success state without re-execution. Cancels or supersedes invalidated tasks and applies validated differential DAG updates into revision N+1 of the `TaskGraph`, recording the complete transaction in SQLite `recovery_attempts`. Key capabilities: - Accepts `ReplanningTrigger` in the request for provenance tracking. - Classifies each replan as `Local`, `Partial`, or `Full` scope before execution. - Exposes `classify_scope` as a pure function for pre-replan analysis.

#### Types & Trait Declarations
- **Structs (4):** `DifferentialReplanEngine`, `DifferentialReplanOutcome`, `DifferentialReplanRequest`, `ReplanAuthority`
- **Enums (1):** `ReplanScope`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn classify_scope(new_task_count: usize, old_task_count: usize) -> ReplanScope;
// pub
fn new(pool: SqlitePool) -> Self;
// pub
async fn execute_replan(&self,
        old_graph: &TaskGraph,
        req: DifferentialReplanRequest,) -> Result<Differe;
// pub
fn new(pool: SqlitePool, event_bus: Option<Arc<dyn crate::events::EventBus>>) -> Self;
// pub
async fn execute_replan(&self,
        req: DifferentialReplanRequest,) -> Result<DifferentialReplanOutcome, M31AError>;
// pub
async fn execute_candidate_plan_replan(&self,
        mission_id: MissionId,
        failed_task_id: Option<TaskId>,
   ;
// pub
async fn execute_replan_action(&self,
        mission_id: MissionId,
        reason: &str,
        tasks_to_supersede: &;
// private
fn test_classify_scope_no_baseline();
// private
fn test_classify_scope_zero_new();
// private
fn test_classify_scope_one_new();
// private
fn test_classify_scope_partial();
// private
fn test_classify_scope_full_equal();
// private
fn test_classify_scope_full_exceeds();
```

#### Unit Verification (7 inline tests)
Tests defined within module:
`test_classify_scope_no_baseline`, `test_classify_scope_zero_new`, `test_classify_scope_one_new`, `test_classify_scope_partial`, `test_classify_scope_full_equal`, `test_classify_scope_full_exceeds`, `test_scope_display`

---
