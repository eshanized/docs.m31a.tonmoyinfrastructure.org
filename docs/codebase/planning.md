# Planning & Decomposition

> **Architectural Layer:** L5 Planning  
> **Source Directory:** `src/planning`  
> **File Count:** 15 source files  

Mission decomposition, strategy generation, plan revision, and candidate DAG creation.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [constraints.rs](#src-planning-constraints-rs) | 364 | `ConstraintDiscoveryEngine, RepositoryPlanEvidence, RepositoryConstraint` | Deterministic static repository constraint discovery engine (PLN-01, D... |
| [metrics.rs](#src-planning-metrics-rs) | 257 | `PlanQualityMetrics` | Plan quality metrics and telemetry for adaptive planning (PLN-22).  `P... |
| [mod.rs](#src-planning-mod-rs) | 44 | `Functions/Traits` | Planning subsystem module (PLN-01..PLN-05, PLN-22).  Owns candidate ta... |
| [frontmatter.rs](#src-planning-projections-frontmatter-rs) | 142 | `ProjectionFrontmatter` | Standardized YAML frontmatter envelope for planning projections (PLN-0... |
| [mission.rs](#src-planning-projections-mission-rs) | 94 | `MissionProjection` | Deterministic one-way MISSION.md projection generator (PLN-03, D-16). |
| [mod.rs](#src-planning-projections-mod-rs) | 113 | `Functions/Traits` | Planning artifact projections (PLN-03, D-13..D-16).  Generates determi... |
| [plan.rs](#src-planning-projections-plan-rs) | 114 | `PlanProjection` | Deterministic one-way PLAN.md projection generator (PLN-03, D-16). |
| [renderer.rs](#src-planning-projections-renderer-rs) | 7 | `Functions/Traits` | ProjectionRenderer trait for deterministic markdown output (PLN-03). |
| [requirements.rs](#src-planning-projections-requirements-rs) | 101 | `RequirementsProjection` | Deterministic one-way REQUIREMENTS.md projection generator (PLN-03, D-... |
| [state.rs](#src-planning-projections-state-rs) | 103 | `StateProjection` | Deterministic one-way STATE.md projection generator (PLN-03, D-16). |
| [requirements.rs](#src-planning-requirements-rs) | 603 | `EngineeringRequirement, EpistemicRevision, Provenance` | Engineering requirements, epistemic classifications, and provenance tr... |
| [review.rs](#src-planning-review-rs) | 3447 | `CandidateTasksWrapper, DynamicQuestionsWrapper, ExecutionAuthorization` | Human-governed plan review, task review, and execution authorization l... |
| [risks.rs](#src-planning-risks-rs) | 262 | `PlanningAssumption, PlanningRisk, PlanningUnknown` | Planning risks, assumptions, and unknowns with explicit criticality ra... |
| [service.rs](#src-planning-service-rs) | 2543 | `PlanDecompositionDto, PlanServiceImpl, PlanTaskDto` | Production PlanService implementation bridging planning subsystem to A... |
| [validation.rs](#src-planning-validation-rs) | 859 | `MockPolicyGate, PlanValidator, ValidationReport` | Deterministic multi-stage plan validation pipeline (PLN-02, D-09..D-12... |

---

### `src/planning/constraints.rs` {#src-planning-constraints-rs}

- **Source Link:** [`src/planning/constraints.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/planning/constraints.rs)
- **Lines of Code:** 364 (12723 bytes)

#### Primary Responsibility
Deterministic static repository constraint discovery engine (PLN-01, D-07).  Performs read-only inspection of repository manifests and directory layout without executing shell commands or relying on heavyweight indexing.

#### Types & Trait Declarations
- **Structs (2):** `ConstraintDiscoveryEngine`, `RepositoryPlanEvidence`
- **Enums (1):** `RepositoryConstraint`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn description(&self) -> String;
// pub
fn discover(repo_root: &Path) -> Vec<RepositoryConstraint>;
// private
fn is_safe_file(canonical_root: &Path, path: &Path) -> bool;
// private
fn is_safe_dir(canonical_root: &Path, path: &Path) -> bool;
// pub
fn from_graph(constraints: Vec<RepositoryConstraint>,
        graph: &crate::repo::graph::RepositoryGraph,) -> Self;
// private
fn test_discover_mock_repository_constraints();
// private
fn test_empty_or_nonexistent_repo_root();
// private
fn test_repository_plan_evidence();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_discover_mock_repository_constraints`, `test_empty_or_nonexistent_repo_root`, `test_repository_plan_evidence`

---

### `src/planning/metrics.rs` {#src-planning-metrics-rs}

- **Source Link:** [`src/planning/metrics.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/planning/metrics.rs)
- **Lines of Code:** 257 (9577 bytes)

#### Primary Responsibility
Plan quality metrics and telemetry for adaptive planning (PLN-22).  `PlanQualityMetrics` captures structural quality indicators for a `CandidatePlan` without imposing policy or validation logic — it is a pure measurement artifact. The runtime records these for observability, revision auditing, and planning-quality analysis. It does NOT alter plan state.

#### Types & Trait Declarations
- **Structs (1):** `PlanQualityMetrics`

#### Key Functions & Signatures (11 shown)
```rust
// pub
fn compute(plan: &CandidatePlan) -> Self;
// pub
fn has_full_verification_coverage(&self) -> bool;
// pub
fn has_invalidated_assumptions(&self) -> bool;
// pub
fn has_revision_record(&self) -> bool;
// pub
fn summary(&self) -> String;
// private
fn task(id: &str, mutating: bool) -> CandidateTask;
// private
fn test_metrics_empty_plan();
// private
fn test_metrics_no_criteria();
// private
fn test_metrics_full_criteria();
// private
fn test_metrics_high_risk_and_assumptions();
// private
fn test_metrics_revision_tracking();
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_metrics_empty_plan`, `test_metrics_no_criteria`, `test_metrics_full_criteria`, `test_metrics_high_risk_and_assumptions`, `test_metrics_revision_tracking`

---

### `src/planning/mod.rs` {#src-planning-mod-rs}

- **Source Link:** [`src/planning/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/planning/mod.rs)
- **Lines of Code:** 44 (1952 bytes)

#### Primary Responsibility
Planning subsystem module (PLN-01..PLN-05, PLN-22).  Owns candidate task decomposition, engineering requirements with epistemic classification, static repository constraint intake, deterministic multi-stage plan validation, and one-way planning artifact projections.  Contracts include: PlanQualityMetrics telemetry, CandidatePlanAssumption, TaskRiskLevel, ReplanningTrigger, and PlanRevisionRecord as kernel contracts.

---

### `src/planning/projections/frontmatter.rs` {#src-planning-projections-frontmatter-rs}

- **Source Link:** [`src/planning/projections/frontmatter.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/planning/projections/frontmatter.rs)
- **Lines of Code:** 142 (5522 bytes)

#### Primary Responsibility
Standardized YAML frontmatter envelope for planning projections (PLN-03, D-16).

#### Types & Trait Declarations
- **Structs (1):** `ProjectionFrontmatter`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn new(projection_type: impl Into<String>,
        mission_id: MissionId,
        source_state_sequence: u64,) -> Self;
// pub
fn render_yaml(&self) -> String;
// pub
fn parse_from_markdown(content: &str) -> Result<Self, String>;
// private
fn test_frontmatter_render_and_parse_roundtrip();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_frontmatter_render_and_parse_roundtrip`

---

### `src/planning/projections/mission.rs` {#src-planning-projections-mission-rs}

- **Source Link:** [`src/planning/projections/mission.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/planning/projections/mission.rs)
- **Lines of Code:** 94 (3002 bytes)

#### Primary Responsibility
Deterministic one-way MISSION.md projection generator (PLN-03, D-16).

#### Types & Trait Declarations
- **Structs (1):** `MissionProjection`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn new(frontmatter: ProjectionFrontmatter, objective: impl Into<String>) -> Self;
// pub
fn with_autonomy_mode(mut self, mode: AutonomyMode) -> Self;
// pub
fn with_constraints(mut self, constraints: Vec<String>) -> Self;
// pub
fn with_success_criteria(mut self, criteria: Vec<String>) -> Self;
// private
fn render(&self) -> String;
// private
fn test_mission_projection_rendering();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_mission_projection_rendering`

---

### `src/planning/projections/mod.rs` {#src-planning-projections-mod-rs}

- **Source Link:** [`src/planning/projections/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/planning/projections/mod.rs)
- **Lines of Code:** 113 (3513 bytes)

#### Primary Responsibility
Planning artifact projections (PLN-03, D-13..D-16).  Generates deterministic one-way markdown projections for MISSION.md, REQUIREMENTS.md, PLAN.md, and STATE.md, housed under `.m31a/missions/&lt;id&gt;/projections/`.

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn mission_projections_dir(storage_root: &Path, mission_id: MissionId) -> PathBuf;
// pub
fn is_projection_stale(projection_sequence: u64, authoritative_sequence: u64) -> bool;
// pub
fn check_file_staleness(file_path: &Path, authoritative_sequence: u64) -> Result<bool, String>;
// private
fn test_mission_projections_dir_layout();
// private
fn test_mission_projections_dir_already_in_m31a();
// private
fn test_staleness_detection();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_mission_projections_dir_layout`, `test_mission_projections_dir_already_in_m31a`, `test_staleness_detection`

---

### `src/planning/projections/plan.rs` {#src-planning-projections-plan-rs}

- **Source Link:** [`src/planning/projections/plan.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/planning/projections/plan.rs)
- **Lines of Code:** 114 (4113 bytes)

#### Primary Responsibility
Deterministic one-way PLAN.md projection generator (PLN-03, D-16).

#### Types & Trait Declarations
- **Structs (1):** `PlanProjection`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn new(frontmatter: ProjectionFrontmatter, plan: CandidatePlan) -> Self;
// private
fn render(&self) -> String;
// private
fn test_plan_projection_rendering();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_plan_projection_rendering`

---

### `src/planning/projections/renderer.rs` {#src-planning-projections-renderer-rs}

- **Source Link:** [`src/planning/projections/renderer.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/planning/projections/renderer.rs)
- **Lines of Code:** 7 (312 bytes)

#### Primary Responsibility
ProjectionRenderer trait for deterministic markdown output (PLN-03).

#### Types & Trait Declarations
- **Traits (1):** `ProjectionRenderer`

#### Key Functions & Signatures (1 shown)
```rust
// private
fn render(&self) -> String;
```

---

### `src/planning/projections/requirements.rs` {#src-planning-projections-requirements-rs}

- **Source Link:** [`src/planning/projections/requirements.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/planning/projections/requirements.rs)
- **Lines of Code:** 101 (3297 bytes)

#### Primary Responsibility
Deterministic one-way REQUIREMENTS.md projection generator (PLN-03, D-16).

#### Types & Trait Declarations
- **Structs (1):** `RequirementsProjection`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn new(frontmatter: ProjectionFrontmatter,
        requirements: Vec<EngineeringRequirement>,) -> Self;
// private
fn render(&self) -> String;
// private
fn test_requirements_projection_rendering();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_requirements_projection_rendering`

---

### `src/planning/projections/state.rs` {#src-planning-projections-state-rs}

- **Source Link:** [`src/planning/projections/state.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/planning/projections/state.rs)
- **Lines of Code:** 103 (3243 bytes)

#### Primary Responsibility
Deterministic one-way STATE.md projection generator (PLN-03, D-16).

#### Types & Trait Declarations
- **Structs (1):** `StateProjection`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn new(frontmatter: ProjectionFrontmatter,
        mission_state: impl Into<String>,
        current_cycle: u64,) -> Sel;
// pub
fn with_stage(mut self, stage: impl Into<String>) -> Self;
// pub
fn with_task_counts(mut self, active: usize, completed: usize) -> Self;
// pub
fn with_escalations(mut self, escalations: usize) -> Self;
// private
fn render(&self) -> String;
// private
fn test_state_projection_rendering();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_state_projection_rendering`

---

### `src/planning/requirements.rs` {#src-planning-requirements-rs}

- **Source Link:** [`src/planning/requirements.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/planning/requirements.rs)
- **Lines of Code:** 603 (20035 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Engineering requirements, epistemic classifications, and provenance trust models (PLN-01, PLN-04, D-05, D-06).

#### Types & Trait Declarations
- **Structs (4):** `EngineeringRequirement`, `EpistemicRevision`, `Provenance`, `RequirementKey`
- **Enums (5):** `EpistemicStatus`, `ProvenanceSourceType`, `RequirementCategory`, `RequirementPriority`, `TrustLevel`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn can_verify_facts(&self) -> bool;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn new(source_type: ProvenanceSourceType,
        trust_level: TrustLevel,
        actor: impl Into<String>,) -> Self;
// pub
fn with_location(mut self, location: impl Into<String>) -> Self;
// pub
fn with_reason(mut self, reason: impl Into<String>) -> Self;
// pub
fn new(from_status: EpistemicStatus,
        to_status: EpistemicStatus,
        provenance: Provenance,
        reason:;
// pub
fn new(key: impl Into<String>) -> Self;
// pub
fn as_str(&self) -> &str;
// private
fn deref(&self) -> &Self::Target;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_epistemic_status_serde_and_display`, `test_trust_level_serde_and_verification_rules`, `test_provenance_full_roundtrip`, `test_requirement_status_transition_with_provenance_guard`, `test_requirement_category_and_priority`

---

### `src/planning/review.rs` {#src-planning-review-rs}

- **Source Link:** [`src/planning/review.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/planning/review.rs)
- **Lines of Code:** 3447 (133609 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Human-governed plan review, task review, and execution authorization lifecycle.  Enforces: "The model proposes. The runtime decides."  Key responsibilities: - First-class Plan Review: create session, display (MD/JSON), manual edit, model revision, accept, reject. - Plan Versioning: immutable history, provenance, author attribution. - First-class Task Review: lowering from accepted plan, editing, adding, removing (with dependency validation), regenerating, accepting. - Task Graph Validation: schema, duplicate IDs, missing prerequisites, cycle detection, capability validation. - Execution Authorization: explicit operator authorization record bound to exact plan/task revision; automatic invalidation on upstream change.

#### Types & Trait Declarations
- **Structs (9):** `CandidateTasksWrapper`, `DynamicQuestionsWrapper`, `ExecutionAuthorization`, `PlanReviewSession`, `PlanRevision`, `PreExecutionCoordinator`, `PromptSemanticAnalyzer`, `TaskReviewSession`, `TaskRevision`
- **Enums (6):** `AuthorizationDecision`, `PlanReviewStatus`, `PreExecutionResponse`, `RevisionAuthorType`, `TaskGraphValidationError`, `TaskReviewStatus`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(session_id: impl Into<String>,
        revision: u32,
        plan_id: impl Into<String>,
        content: Candid;
// pub
fn to_json(&self) -> Result<String, serde_json::Error>;
// pub
fn compute_content_hash(content: &CandidatePlan) -> String;
// pub
fn content_hash(&self) -> String;
// pub
fn to_markdown(&self) -> String;
// pub
fn new(session_id: impl Into<String>,
        revision: u32,
        plan_revision: u32,
        tasks: Vec<CandidateTas;
// pub
fn to_json(&self) -> Result<String, serde_json::Error>;
// pub
fn compute_tasks_hash(tasks: &[CandidateTask]) -> String;
// pub
fn content_hash(&self) -> String;
// pub
fn to_markdown(&self) -> String;
// pub
fn new(session_id: impl Into<String>,
        plan_revision: u32,
        task_revision: u32,
        authorized_by: imp;
// pub
fn with_execution_binding(mut self,
        policy_hash: impl Into<String>,
        workspace_root: impl Into<String>,
 ;
// pub
fn with_content_hashes(mut self,
        plan_hash: impl Into<String>,
        task_hash: impl Into<String>,) -> Self;
// pub
fn is_valid_for(&self, current_plan_rev: u32, current_task_rev: u32) -> bool;
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_task_graph_validation_detects_cycles`, `test_task_graph_validation_detects_missing_dep`, `test_task_graph_validation_detects_duplicate_id`, `test_task_removal_checks_dependents`, `test_authorization_binding_and_invalidation`

---

### `src/planning/risks.rs` {#src-planning-risks-rs}

- **Source Link:** [`src/planning/risks.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/planning/risks.rs)
- **Lines of Code:** 262 (8289 bytes)

#### Primary Responsibility
Planning risks, assumptions, and unknowns with explicit criticality ratings (PLN-01, PLN-02, D-08).

#### Types & Trait Declarations
- **Structs (3):** `PlanningAssumption`, `PlanningRisk`, `PlanningUnknown`
- **Enums (2):** `Criticality`, `UnknownFate`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn is_blocking_threshold(&self) -> bool;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn new(id: impl Into<String>,
        description: impl Into<String>,
        criticality: Criticality,
        provenan;
// pub
fn with_mitigation(mut self, mitigation: impl Into<String>) -> Self;
// pub
fn new(id: impl Into<String>,
        description: impl Into<String>,
        criticality: Criticality,
        provenan;
// pub
fn with_resolution_strategy(mut self, strategy: impl Into<String>) -> Self;
// private
fn default_unknown_fate() -> UnknownFate;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// pub
fn new(id: impl Into<String>,
        description: impl Into<String>,
        criticality: Criticality,
        provenan;
// pub
fn with_discovery_plan(mut self, plan: impl Into<String>) -> Self;
// pub
fn with_fate(mut self, fate: UnknownFate) -> Self;
// pub
fn with_resolution(mut self, resolution: impl Into<String>) -> Self;
// private
fn test_critical_assumption_construction_and_serde();
// private
fn test_planning_risk_and_unknown();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_critical_assumption_construction_and_serde`, `test_planning_risk_and_unknown`

---

### `src/planning/service.rs` {#src-planning-service-rs}

- **Source Link:** [`src/planning/service.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/planning/service.rs)
- **Lines of Code:** 2543 (106619 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Production PlanService implementation bridging planning subsystem to Autonomy Controller (PLN-01, PLN-03, PLN-05).

#### Types & Trait Declarations
- **Structs (4):** `PlanDecompositionDto`, `PlanServiceImpl`, `PlanTaskDto`, `TestModelCaller`
- **Enums (2):** `CapabilityDto`, `VerificationDto`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn id(&self) -> &str;
// pub
fn mode(&self) -> Option<&str>;
// pub
fn to_strategy(&self, expected_outputs: &[String]) -> Result<VerificationStrategy, String>;
// private
fn parse_proposed_verification(spec: &str,
    expected_outputs: &[String],) -> Result<VerificationStrategy, String>;
// private
fn try_parse_dto_slice(slice: &str) -> Option<PlanDecompositionDto>;
// pub(crate)
fn parse_decomposition_json(text: &str) -> Result<PlanDecompositionDto, String>;
// pub(crate)
fn parse_dto_from_value(val: serde_json::Value) -> Result<PlanDecompositionDto, String>;
// pub(crate)
fn parse_dto_from_proposal(proposal: ModelProposal,) -> Result<PlanDecompositionDto, String>;
// pub
fn is_transient_provider_error(err: &str) -> (bool, Option<Duration>);
// pub
fn normalize_capability_id(raw: &str) -> String;
// pub
fn align_candidate_task_role(task: &mut CandidateTask);
// pub
fn align_candidate_task_role_with_contract(task: &mut CandidateTask,
    is_read_only_contract: bool,);
// pub(crate)
fn compile_resolved_planning_prompt(catalog: &dyn PromptCatalog,
    compiler: &dyn PromptCompiler,
    contract: &crate;
// pub
fn is_read_only_objective(objective: &str) -> bool;
// pub
fn new(storage_root: impl Into<PathBuf>) -> Self;
```

#### Unit Verification (16 inline tests)
Tests defined within module:
`test_parse_decomposition_accepts_prompt_vocabulary_aliases`, `test_parse_decomposition_accepts_bare_task_array`, `test_parse_decomposition_rejects_garbage`, `test_plan_service_no_model_actionable_objective_fails_explicitly`, `test_plan_service_no_model_read_only_yields_empty_plan`, `test_plan_service_replan`, `test_classify_objective_table_driven`, `test_study_codebase_produces_non_empty_researcher_plan`, `test_security_audit_produces_read_only_envelope`, `test_actionable_objective_empty_model_fails_explicitly`...

---

### `src/planning/validation.rs` {#src-planning-validation-rs}

- **Source Link:** [`src/planning/validation.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/planning/validation.rs)
- **Lines of Code:** 859 (31797 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Deterministic multi-stage plan validation pipeline (PLN-02, D-09..D-12).  Validates candidate plans across three sequential stages: 1. Graph / Structural validation (cycles, missing prerequisites, duplicates) 2. Capability / Policy satisfiability (authorization dry-run, ASK never becomes ALLOW) 3. Safety / Bounds / Evidence validation (resource limits, verification strategies, contradictory criteria)

#### Types & Trait Declarations
- **Structs (3):** `MockPolicyGate`, `PlanValidator`, `ValidationReport`
- **Enums (3):** `NormalizedPredicate`, `ValidationError`, `ValidationWarning`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn is_valid(&self) -> bool;
// pub
fn add_error(&mut self, err: ValidationError);
// pub
fn add_warning(&mut self, warn: ValidationWarning);
// pub
fn error_count(&self) -> usize;
// pub
fn warning_count(&self) -> usize;
// private
fn parse(text: &str) -> Option<Self>;
// private
fn contradicts(&self, other: &Self) -> Option<String>;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new() -> Self;
// pub
fn with_read_only(mut self, read_only: bool) -> Self;
// pub
fn with_allow_empty(mut self, allow: bool) -> Self;
// pub
fn with_available_capabilities(mut self, caps: HashSet<String>) -> Self;
// pub
fn with_policy_gate(mut self, gate: Arc<dyn PolicyGate>) -> Self;
// pub
fn with_autonomy_mode(mut self, mode: AutonomyMode) -> Self;
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_validation_report_validity`, `test_structural_pass_cycle_and_missing_keys`, `test_capability_pass_ask_and_escalate_never_allow`, `test_safety_bounds_and_contradictory_criteria`, `test_capability_pass_rejects_role_envelope_violations`, `test_capability_pass_allows_valid_role_envelope`

---
