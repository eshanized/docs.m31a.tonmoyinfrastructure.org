# Genesis & Engineering Workflows

> **Architectural Layer:** L8 Workflow  
> **Source Directory:** `src/workflow`  
> **File Count:** 35 source files  

35-file multi-stage genesis workflows, ADR creation, charter, synthesis, and roadmap.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [compiler.rs](#src-workflow-compiler-rs) | 514 | `CompiledWorkflow, LoweredWorkflow, WorkflowCompiler` | Deterministic workflow manifest compiler resolving prompt contracts an... |
| [definition.rs](#src-workflow-definition-rs) | 707 | `InputBinding, OutputBinding, QualityGate` | Declarative workflow definitions, step specifications, and input/outpu... |
| [engine.rs](#src-workflow-engine-rs) | 1635 | `WorkflowEngine, WorkflowExecutionSnapshot, WorkflowRunHandle` | WorkflowEngine coordinating durable multi-step workflow execution over... |
| [error.rs](#src-workflow-error-rs) | 537 | `WorkflowError` | Typed error model for workflow definitions, state transitions, and per... |
| [brownfield.rs](#src-workflow-genesis-brownfield-rs) | 191 | `BrownfieldMap, CodebaseTopology` | Brownfield codebase scanning, topology mapping, and BROWNFIELD.md proj... |
| [dimension_registry.rs](#src-workflow-genesis-dimension_registry-rs) | 392 | `ResearchDimensionDefinition, ResearchDimensionRegistry, DimensionError` | Open research-dimension registry: existence authority for Genesis rese... |
| [discovery.rs](#src-workflow-genesis-discovery-rs) | 1209 | `DiscoveryFact, DiscoverySession, DiscoveryTurn` | Socratic discovery dialogue, ambiguity scoring, and convergence engine... |
| [environment.rs](#src-workflow-genesis-environment-rs) | 684 | `EnvironmentFact, WorkspaceEnvironment, WorkspaceEvidence` | Deterministic environment probing and workspace fact extraction. |
| [errors.rs](#src-workflow-genesis-errors-rs) | 59 | `GenesisError` | Typed error model for Project Genesis discovery, research, and synthes... |
| [intake.rs](#src-workflow-genesis-intake-rs) | 211 | `GenesisOptions, GenesisRequest, GenesisMode` | Genesis intake types, mode definition, and request aggregates. |
| [mod.rs](#src-workflow-genesis-mod-rs) | 198 | `GenesisController, GenesisPipelineOutcome` | Project Genesis: Discovery, Environment Probing, and Research Orchestr... |
| [project.rs](#src-workflow-genesis-project-rs) | 545 | `AmbiguityAssessment, OperationalInvariants, ProjectBoundaries` | Project Charter domain model, ambiguity assessment, and PROJECT.md mar... |
| [provenance.rs](#src-workflow-genesis-provenance-rs) | 149 | `ResearchEvidence, ResearchFinding, ResearchSourceType` | Research source provenance, evidence tracking, and citation models. |
| [research_decision.rs](#src-workflow-genesis-research_decision-rs) | 218 | `ResearchDecision, ResearchDimension` | Research decision logic, dimension definitions, and skip/trigger evalu... |
| [researcher.rs](#src-workflow-genesis-researcher-rs) | 438 | `ResearchOrchestrator` | Bounded parallel research orchestrator and workflow definition compile... |
| [synthesis.rs](#src-workflow-genesis-synthesis-rs) | 332 | `ConsensusPoint, ContradictionResolution, OpenUnknown` | Multi-dimensional research synthesis, consensus extraction, and SUMMAR... |
| [manifest.rs](#src-workflow-manifest-rs) | 570 | `InputBindingManifest, OutputBindingManifest, QualityGateManifest` | Declarative TOML workflow manifest parser, schema models, and strict v... |
| [mod.rs](#src-workflow-mod-rs) | 101 | `Functions/Traits` | Workflow domain contracts, manifest parsing, prompt catalog, quality g... |
| [adr.rs](#src-workflow-planning-adr-rs) | 457 | `AdrId, AdrRegistry, ArchitectureDecisionRecord` | Architecture Decision Record (ADR) domain model, registry, and project... |
| [architecture.rs](#src-workflow-planning-architecture-rs) | 473 | `ArchitectureComponent, ArchitectureDataStore, ArchitectureDocument` | Architecture models, component topologies, security trust boundaries, ... |
| [architecture_synthesizer.rs](#src-workflow-planning-architecture_synthesizer-rs) | 702 | `ArchitectureSynthesizer, DerivedGroup` | System Architecture Synthesizer extracting topologies, interfaces, and... |
| [decision.rs](#src-workflow-planning-decision-rs) | 90 | `DecisionStatus` | Architectural decision statuses and governance rules. |
| [invalidation.rs](#src-workflow-planning-invalidation-rs) | 214 | `PlanningChangeSet, PlanningInvalidator` | Cascading planning invalidation and change impact analysis (Section 31... |
| [mod.rs](#src-workflow-planning-mod-rs) | 389 | `PlanningCoordinator, PlanningPipelineOutcome` | Upstream planning, specifications, ADRs, risk register, and phased roa... |
| [requirements.rs](#src-workflow-planning-requirements-rs) | 243 | `RequirementsDocument` | Authoritative requirements document model and Markdown projections.  R... |
| [requirements_synthesizer.rs](#src-workflow-planning-requirements_synthesizer-rs) | 296 | `RequirementsSynthesizer` | Requirements Synthesizer extracting EngineeringRequirements from Genes... |
| [risks.rs](#src-workflow-planning-risks-rs) | 280 | `RiskEntry, RiskRegister, QualitativeImpact` | Risk register, assumptions, unknowns, and RISKS.md projection. |
| [roadmap.rs](#src-workflow-planning-roadmap-rs) | 825 | `Roadmap, RoadmapDependency, RoadmapPhase` | Dependency-aware Roadmap DAG compilation, phase sequencing, and ROADMA... |
| [state.rs](#src-workflow-planning-state-rs) | 437 | `PlanningState, PlanningStateMachine, PlanningLifecycleState` | Planning lifecycle state machine and STATE.md projection. |
| [traceability.rs](#src-workflow-planning-traceability-rs) | 218 | `TraceLink, TraceabilityMatrix` | Bidirectional traceability matrix linking requirements, research, arch... |
| [validation.rs](#src-workflow-planning-validation-rs) | 353 | `PlanningQualityGates` | Quality gates for Requirements, Architecture, and Roadmap synthesis. |
| [provenance.rs](#src-workflow-provenance-rs) | 184 | `StepProvenance, WorkflowProvenance` | Provenance tracking and cryptographic content hashing for compiled wor... |
| [quality_gate.rs](#src-workflow-quality_gate-rs) | 462 | `QualityGateContext, QualityGateResult, QualityGateViolation` | QualityGate contracts, deterministic Tier-1 and Tier-2 evaluation, and... |
| [repository.rs](#src-workflow-repository-rs) | 900 | `SqliteWorkflowRepository` | SQLite persistence and repository trait for workflow runs, steps, and ... |
| [state.rs](#src-workflow-state-rs) | 628 | `WorkflowArtifact, WorkflowRun, WorkflowStepRun` | Durable state aggregates and transition validation for workflow runs a... |

---

### `src/workflow/compiler.rs` {#src-workflow-compiler-rs}

- **Source Link:** [`src/workflow/compiler.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/compiler.rs)
- **Lines of Code:** 514 (21053 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Deterministic workflow manifest compiler resolving prompt contracts and attaching provenance.

#### Types & Trait Declarations
- **Structs (3):** `CompiledWorkflow`, `LoweredWorkflow`, `WorkflowCompiler`

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn from_definition(definition: WorkflowDefinition) -> Result<Self, WorkflowError>;
// pub
fn map_step_verification(step: &WorkflowStepDefinition) -> VerificationStrategy;
// pub
fn compute_unblocked_step_keys(&self,
        approved_keys: &std::collections::HashSet<String>,) -> std::collections::H;
// pub
fn lower(&self, mission_id: MissionId) -> Result<LoweredWorkflow, WorkflowError>;
// pub
fn lower_subset(&self,
        mission_id: MissionId,
        included_step_keys: Option<&std::collections::HashSet<Stri;
// pub
fn lower_default(&self) -> Result<LoweredWorkflow, WorkflowError>;
// pub
fn new(catalog: &'a dyn PromptCatalog) -> Self;
// pub
fn with_strict_roles(mut self, strict: bool) -> Self;
// pub
fn compile(&self,
        manifest: &WorkflowManifest,
        source_path: Option<&str>,
        workspace_root: Option;
// pub
fn lower(&self,
        manifest: &WorkflowManifest,
        source_path: Option<&str>,
        workspace_root: Option<&;
```

---

### `src/workflow/definition.rs` {#src-workflow-definition-rs}

- **Source Link:** [`src/workflow/definition.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/definition.rs)
- **Lines of Code:** 707 (28810 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Declarative workflow definitions, step specifications, and input/output bindings.

#### Types & Trait Declarations
- **Structs (5):** `InputBinding`, `OutputBinding`, `QualityGate`, `WorkflowDefinition`, `WorkflowStepDefinition`
- **Enums (1):** `RecoveryStrategy`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default_step_timeout() -> u64;
// private
fn default_workflow_version() -> u32;
// private
fn default_max_retries() -> u32;
// pub
fn effective_recovery_strategy(&self,
        default_strategy: &RecoveryStrategy,) -> RecoveryStrategy;
// pub
fn effective_prompt_ref(&self,) -> Result<crate::prompt::PromptReference, crate::workflow::error::WorkflowError>;
// pub
fn validate(&self) -> Result<(), WorkflowError>;
// pub
fn topological_order(&self) -> Result<Vec<String>, WorkflowError>;
// pub
fn get_step(&self, key: &str) -> Option<&WorkflowStepDefinition>;
// pub
fn validate_artifact_path(path: &Path,
    workspace_root: Option<&Path>,) -> Result<PathBuf, WorkflowError>;
// private
fn sample_step(key: &str, deps: Vec<&str>) -> WorkflowStepDefinition;
// private
fn test_valid_linear_workflow();
// private
fn test_parallel_siblings_topological_order();
// private
fn test_converging_dependencies();
// private
fn test_cycle_detection();
// private
fn test_self_dependency_rejected();
```

#### Unit Verification (8 inline tests)
Tests defined within module:
`test_valid_linear_workflow`, `test_parallel_siblings_topological_order`, `test_converging_dependencies`, `test_cycle_detection`, `test_self_dependency_rejected`, `test_missing_dependency_rejected`, `test_duplicate_step_key_rejected`, `test_artifact_path_validation`

---

### `src/workflow/engine.rs` {#src-workflow-engine-rs}

- **Source Link:** [`src/workflow/engine.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/engine.rs)
- **Lines of Code:** 1635 (63668 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
WorkflowEngine coordinating durable multi-step workflow execution over M31A runtime authorities.  # Core Invariant  "The model proposes. The runtime decides."  Under the unified authority model (AD-003), WorkflowEngine is a pure declarative workflow lowering and canonical runtime orchestrator. There is exactly ONE production execution path:  ```text Workflow definition ↓ WorkflowCompiler / CompiledWorkflow::lower ↓ LoweredWorkflow ↓ Canonical Mission + CandidatePlan ↓ AutonomyController::run ↓ SchedulerEngine ↓ WorkerDispatcher ↓ WorkerRunner ```  WorkflowEngine cannot independently calculate ready waves, allocate workers, or declare task completion. All execution authority resides exclusively in `AutonomyController`

#### Types & Trait Declarations
- **Structs (4):** `WorkflowEngine`, `WorkflowExecutionSnapshot`, `WorkflowRunHandle`, `WorkflowStartRequest`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(workspace_root: impl Into<PathBuf>) -> Self;
// pub
fn with_mode(mut self, mode: WorkflowMode) -> Self;
// pub
fn with_parameter(mut self, key: impl Into<String>, value: impl Into<String>) -> Self;
// pub
fn new(repository: Arc<dyn WorkflowRepository>,
        prompt_catalog: Arc<dyn PromptCatalog>,
        event_bus: Optio;
// pub
fn from_dependencies(repository: Arc<dyn WorkflowRepository>,
        prompt_catalog: Arc<dyn PromptCatalog>,
        de;
// pub
fn with_dependencies(mut self, dependencies: ControllerDependencies) -> Self;
// pub
fn dependencies(&self) -> Option<&ControllerDependencies>;
// pub
fn with_artifact_service(mut self,
        artifact_service: Arc<crate::persistence::ArtifactService>,) -> Self;
// pub
fn artifact_service(&self) -> Option<&Arc<crate::persistence::ArtifactService>>;
// pub
fn repository(&self) -> &Arc<dyn WorkflowRepository>;
// pub
fn prompt_catalog(&self) -> &Arc<dyn PromptCatalog>;
// pub
async fn start_workflow(&self,
        compiled: &CompiledWorkflow,
        request: WorkflowStartRequest,) -> Result<Wo;
// pub
async fn execute_autonomously(&self,
        compiled: &CompiledWorkflow,
        request: WorkflowStartRequest,) -> Res;
// pub
async fn advance_workflow(&self,
        run_id: WorkflowRunId,
        compiled: &CompiledWorkflow,) -> Result<Workflow;
// private
async fn sync_workflow_from_controller_halt(&self,
        run_id: WorkflowRunId,
        mission_id: MissionId,
       ;
```

---

### `src/workflow/error.rs` {#src-workflow-error-rs}

- **Source Link:** [`src/workflow/error.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/error.rs)
- **Lines of Code:** 537 (20816 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Typed error model for workflow definitions, state transitions, and persistence.

#### Types & Trait Declarations
- **Enums (1):** `WorkflowError`

#### Key Functions & Signatures (2 shown)
```rust
// private
fn from(err: WorkflowError) -> Self;
// private
fn from(err: crate::prompt::PromptError) -> Self;
```

---

### `src/workflow/genesis/brownfield.rs` {#src-workflow-genesis-brownfield-rs}

- **Source Link:** [`src/workflow/genesis/brownfield.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/genesis/brownfield.rs)
- **Lines of Code:** 191 (7006 bytes)

#### Primary Responsibility
Brownfield codebase scanning, topology mapping, and BROWNFIELD.md projection.

#### Types & Trait Declarations
- **Structs (2):** `BrownfieldMap`, `CodebaseTopology`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn scan(workspace_root: &Path) -> Result<Self, GenesisError>;
// pub
fn to_markdown(&self) -> String;
// pub
fn save_to_dir(&self,
        workspace_root: &Path,
        projection_dir: &str,) -> Result<PathBuf, GenesisError>;
```

---

### `src/workflow/genesis/dimension_registry.rs` {#src-workflow-genesis-dimension_registry-rs}

- **Source Link:** [`src/workflow/genesis/dimension_registry.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/genesis/dimension_registry.rs)
- **Lines of Code:** 392 (16352 bytes)

#### Primary Responsibility
Open research-dimension registry: existence authority for Genesis research dimensions.  ## Authority model  ```text dimension definition (built-in data or registered extension) ↓ ResearchDimensionRegistry (existence authority) ↓ generic orchestration (researcher, synthesis, requirements, architecture) ```  [`ResearchDimension`] is pure identity. Everything behavioral — prompt contract, researcher role, artifact filename, and the requirements- synthesis mapping (key prefix, category, priority, rationale) — lives in [`ResearchDimensionDefinition`]. Adding a dimension registers a definition; the research engine iterates the decision's selected ids without any per-dimension branch.  ## No silent loss  Every consumer resolves dimensions through this registry and fails explicitly on unknown ids. Unknown artifact filenames are preserved in an explicitly-marked unregistered bucket, never misattributed to an unrelated dimension.

#### Types & Trait Declarations
- **Structs (2):** `ResearchDimensionDefinition`, `ResearchDimensionRegistry`
- **Enums (1):** `DimensionError`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn with_builtins() -> Self;
// pub
fn global() -> &'static RwLock<ResearchDimensionRegistry>;
// pub
fn register(&mut self, def: ResearchDimensionDefinition) -> Result<(), DimensionError>;
// pub
fn resolve(&self, id: &ResearchDimension) -> Option<&ResearchDimensionDefinition>;
// pub
fn resolve_filename(&self, filename: &str) -> Option<&ResearchDimensionDefinition>;
// pub
fn contains(&self, id: &ResearchDimension) -> bool;
// pub
fn full_set(&self) -> Vec<ResearchDimension>;
// pub
fn targeted_set(&self) -> Vec<ResearchDimension>;
// pub
fn builtin_ids(&self) -> Vec<String>;
// pub
fn all_ids(&self) -> Vec<String>;
// pub
fn is_full_set(&self, selected: &[ResearchDimension]) -> bool;
// pub
fn register_global(def: ResearchDimensionDefinition) -> Result<(), DimensionError>;
// pub
fn resolve_global(id: &ResearchDimension) -> Option<ResearchDimensionDefinition>;
// private
fn validate_dimension_definition(def: &ResearchDimensionDefinition) -> Result<(), DimensionError>;
// private
fn builtin_dimension_definitions() -> Vec<ResearchDimensionDefinition>;
```

---

### `src/workflow/genesis/discovery.rs` {#src-workflow-genesis-discovery-rs}

- **Source Link:** [`src/workflow/genesis/discovery.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/genesis/discovery.rs)
- **Lines of Code:** 1209 (47483 bytes)

#### Primary Responsibility
Socratic discovery dialogue, ambiguity scoring, and convergence engine.

#### Types & Trait Declarations
- **Structs (4):** `DiscoveryFact`, `DiscoverySession`, `DiscoveryTurn`, `DynamicQuestion`
- **Enums (4):** `AnswerValidationError`, `ConvergenceReason`, `DiscoveryPillar`, `QuestionValidationError`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(pillar: DiscoveryPillar, key: impl Into<String>, value: impl Into<String>) -> Self;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(request: GenesisRequest, environment: WorkspaceEnvironment) -> Self;
// pub
fn workflow_tier(&self) -> WorkflowTier;
// pub
fn unknowns(&self) -> Vec<PlanningUnknown>;
// pub
fn requires_user_decision(&self) -> bool;
// pub
fn check_convergence(&self) -> (bool, Option<ConvergenceReason>);
// pub
fn next_turn(&mut self) -> Result<Option<DiscoveryTurn>, GenesisError>;
// pub
fn submit_response(&mut self, response: &str) -> Result<bool, GenesisError>;
// pub
fn synthesize_charter(&self) -> Result<ProjectCharter, GenesisError>;
// private
fn formulate_question_for_pillar(&self,
        pillar: DiscoveryPillar,) -> (String, Vec<String>, String);
// pub
fn classify_workflow_tier(prompt: &str, env: &WorkspaceEnvironment) -> WorkflowTier;
// private
fn make_unknown(id: &str, desc: &str, criticality: Criticality) -> PlanningUnknown;
// pub
fn extract_unknowns(prompt: &str, tier: WorkflowTier) -> Vec<PlanningUnknown>;
```

---

### `src/workflow/genesis/environment.rs` {#src-workflow-genesis-environment-rs}

- **Source Link:** [`src/workflow/genesis/environment.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/genesis/environment.rs)
- **Lines of Code:** 684 (25491 bytes)

#### Primary Responsibility
Deterministic environment probing and workspace fact extraction.

#### Types & Trait Declarations
- **Structs (3):** `EnvironmentFact`, `WorkspaceEnvironment`, `WorkspaceEvidence`
- **Enums (4):** `Confidence`, `EnvironmentCategory`, `FactSource`, `WorkspaceMode`

#### Key Functions & Signatures (14 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(category: EnvironmentCategory,
        key: impl Into<String>,
        value: impl Into<String>,
        source: ;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn probe(workspace_root: &Path) -> Result<Self, GenesisError>;
// pub
fn get_fact(&self, key: &str) -> Option<&str>;
// pub
fn fact_equals(&self, key: &str, expected: &str) -> bool;
// pub
fn has_fact(&self, key: &str) -> bool;
// pub
fn facts_in_category(&self, category: EnvironmentCategory) -> Vec<&EnvironmentFact>;
// pub
fn is_greenfield(&self) -> bool;
// pub
fn is_brownfield(&self) -> bool;
// pub
fn is_unknown(&self) -> bool;
// private
fn probe_toolchain(facts: &mut Vec<EnvironmentFact>, tool: &str, args: &[&str]);
// private
fn run_cmd_in_dir(dir: &Path, tool: &str, args: &[&str]) -> Option<String>;
// private
fn scan_workspace_recursive(dir: &Path,
    current_depth: usize,
    max_depth: usize,
    evidence: &mut WorkspaceEvid;
```

---

### `src/workflow/genesis/errors.rs` {#src-workflow-genesis-errors-rs}

- **Source Link:** [`src/workflow/genesis/errors.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/genesis/errors.rs)
- **Lines of Code:** 59 (1482 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Typed error model for Project Genesis discovery, research, and synthesis.

#### Types & Trait Declarations
- **Enums (1):** `GenesisError`

#### Key Functions & Signatures (2 shown)
```rust
// private
fn from(err: GenesisError) -> Self;
// private
fn from(err: GenesisError) -> Self;
```

---

### `src/workflow/genesis/intake.rs` {#src-workflow-genesis-intake-rs}

- **Source Link:** [`src/workflow/genesis/intake.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/genesis/intake.rs)
- **Lines of Code:** 211 (8442 bytes)

#### Primary Responsibility
Genesis intake types, mode definition, and request aggregates.

#### Types & Trait Declarations
- **Structs (2):** `GenesisOptions`, `GenesisRequest`
- **Enums (1):** `GenesisMode`

#### Key Functions & Signatures (13 shown)
```rust
// private
fn default_true() -> bool;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn default() -> Self;
// pub
fn from_config(config: &ResolvedConfiguration) -> Self;
// pub
fn with_require_charter_approval(mut self, require: bool) -> Self;
// pub
fn with_require_architecture_approval(mut self, require: bool) -> Self;
// pub
fn with_require_roadmap_approval(mut self, require: bool) -> Self;
// pub
fn with_auto_advance(mut self, auto: bool) -> Self;
// pub
fn canonicalize_projection_dir(raw: &str) -> String;
// pub
fn new(prompt: impl Into<String>, workspace_root: impl Into<PathBuf>) -> Self;
// pub
fn with_mission_id(mut self, mission_id: crate::ids::MissionId) -> Self;
// pub
fn with_mode(mut self, mode: GenesisMode) -> Self;
// pub
fn with_options(mut self, options: GenesisOptions) -> Self;
```

---

### `src/workflow/genesis/mod.rs` {#src-workflow-genesis-mod-rs}

- **Source Link:** [`src/workflow/genesis/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/genesis/mod.rs)
- **Lines of Code:** 198 (6587 bytes)

#### Primary Responsibility
Project Genesis: Discovery, Environment Probing, and Research Orchestration.  # Architecture Invariant  ```text Genesis Controller ↓ WorkflowEngine ↓ WorkflowStep ↓ Mission ↓ TaskGraph ↓ SchedulerEngine ↓ AgentRuntime ```  "The model proposes. The runtime decides."

#### Types & Trait Declarations
- **Structs (2):** `GenesisController`, `GenesisPipelineOutcome`

#### Key Functions & Signatures (7 shown)
```rust
// pub
async fn register_artifacts(&self,
        artifact_service: &crate::persistence::artifacts::ArtifactService,) -> Result;
// pub
fn probe(workspace_root: &Path) -> Result<WorkspaceEnvironment, GenesisError>;
// pub
fn map_brownfield(workspace_root: &Path,
        projection_dir: &str,) -> Result<BrownfieldMap, GenesisError>;
// pub
fn run_discovery(session: &mut DiscoverySession,
        workspace_root: &Path,
        projection_dir: &str,) -> Result;
// pub
fn decide_research(charter: &ProjectCharter,
        env: &WorkspaceEnvironment,
        options: &GenesisOptions,) -> R;
// pub
async fn execute_research(engine: &WorkflowEngine,
        charter: &ProjectCharter,
        decision: &ResearchDecision;
// pub
fn run_planning(charter: &ProjectCharter,
        summary: Option<&ResearchSummary>,
        findings: &[ResearchFinding;
```

---

### `src/workflow/genesis/project.rs` {#src-workflow-genesis-project-rs}

- **Source Link:** [`src/workflow/genesis/project.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/genesis/project.rs)
- **Lines of Code:** 545 (21049 bytes)

#### Primary Responsibility
Project Charter domain model, ambiguity assessment, and PROJECT.md markdown projection.

#### Types & Trait Declarations
- **Structs (6):** `AmbiguityAssessment`, `OperationalInvariants`, `ProjectBoundaries`, `ProjectCharter`, `TargetDomainModel`, `TechnicalPreferences`
- **Enums (1):** `WorkflowTier`

#### Key Functions & Signatures (13 shown)
```rust
// private
fn default() -> Self;
// private
fn eq(&self, other: &Self) -> bool;
// private
fn hash(&self, state: &mut H);
// pub
fn is_standard(&self) -> bool;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(project_name: impl Into<String>, overview: impl Into<String>) -> Self;
// pub
fn with_workflow_tier(mut self, tier: WorkflowTier) -> Self;
// pub
fn with_domain_model(mut self, model: TargetDomainModel) -> Self;
// pub
fn approve(&mut self);
// pub
fn validate(&self) -> Result<(), GenesisError>;
// pub
fn to_markdown(&self) -> String;
// pub
fn from_markdown(content: &str) -> Result<Self, GenesisError>;
// pub
fn save_to_dir(&self,
        workspace_root: &Path,
        projection_dir: &str,) -> Result<PathBuf, GenesisError>;
```

---

### `src/workflow/genesis/provenance.rs` {#src-workflow-genesis-provenance-rs}

- **Source Link:** [`src/workflow/genesis/provenance.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/genesis/provenance.rs)
- **Lines of Code:** 149 (4740 bytes)

#### Primary Responsibility
Research source provenance, evidence tracking, and citation models.

#### Types & Trait Declarations
- **Structs (2):** `ResearchEvidence`, `ResearchFinding`
- **Enums (1):** `ResearchSourceType`

#### Key Functions & Signatures (4 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(dimension: ResearchDimension,
        source_type: ResearchSourceType,
        source_uri: impl Into<String>,
   ;
// pub
fn new(dimension: ResearchDimension,
        topic: impl Into<String>,
        summary: impl Into<String>,) -> Self;
// pub
fn to_markdown(&self) -> String;
```

---

### `src/workflow/genesis/research_decision.rs` {#src-workflow-genesis-research_decision-rs}

- **Source Link:** [`src/workflow/genesis/research_decision.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/genesis/research_decision.rs)
- **Lines of Code:** 218 (8514 bytes)

#### Primary Responsibility
Research decision logic, dimension definitions, and skip/trigger evaluation.

#### Types & Trait Declarations
- **Structs (2):** `ResearchDecision`, `ResearchDimension`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(id: impl Into<String>) -> Self;
// pub
fn as_str(&self) -> &str;
// pub
fn is_well_formed(&self) -> bool;
// pub
fn stack() -> Self;
// pub
fn features() -> Self;
// pub
fn architecture() -> Self;
// pub
fn pitfalls() -> Self;
// pub
fn security() -> Self;
// pub
fn deployment() -> Self;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn skip(reason: impl Into<String>) -> Self;
// pub
fn execute(dimensions: Vec<ResearchDimension>, trigger_reason: impl Into<String>) -> Self;
// pub
fn is_full_greenfield(&self) -> bool;
// pub
fn is_targeted_delta(&self) -> bool;
```

---

### `src/workflow/genesis/researcher.rs` {#src-workflow-genesis-researcher-rs}

- **Source Link:** [`src/workflow/genesis/researcher.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/genesis/researcher.rs)
- **Lines of Code:** 438 (18598 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Bounded parallel research orchestrator and workflow definition compiler.

#### Types & Trait Declarations
- **Structs (1):** `ResearchOrchestrator`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn build_workflow_definition(charter: &ProjectCharter,
        decision: &ResearchDecision,
        options: &GenesisOpt;
// pub
fn compile_research_workflow(charter: &ProjectCharter,
        decision: &ResearchDecision,
        options: &GenesisOpt;
// pub
fn parse_finding(dim: &super::research_decision::ResearchDimension,
        dimension_id: &str,
        content: &str,) ;
// pub
fn materialize_research_artifacts(workspace_root: &Path,
        projection_dir: &str,
        findings: &[crate::workfl;
// pub
fn collect_findings(workspace_root: &Path,
        projection_dir: &str,
        dimensions: &[super::research_decision:;
// pub
async fn execute(engine: &WorkflowEngine,
        charter: &ProjectCharter,
        decision: &ResearchDecision,
       ;
```

---

### `src/workflow/genesis/synthesis.rs` {#src-workflow-genesis-synthesis-rs}

- **Source Link:** [`src/workflow/genesis/synthesis.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/genesis/synthesis.rs)
- **Lines of Code:** 332 (12864 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Multi-dimensional research synthesis, consensus extraction, and SUMMARY.md generation.

#### Types & Trait Declarations
- **Structs (7):** `ConsensusPoint`, `ContradictionResolution`, `OpenUnknown`, `RejectedAlternative`, `ResearchSummary`, `ResearchSynthesizer`, `TradeoffAnalysis`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn new(project_name: impl Into<String>, executive_summary: impl Into<String>) -> Self;
// pub
fn validate(&self) -> Result<(), GenesisError>;
// pub
fn to_markdown(&self) -> String;
// pub
fn save_to_dir(&self,
        workspace_root: &Path,
        projection_dir: &str,) -> Result<PathBuf, GenesisError>;
// pub
fn synthesize(charter: &ProjectCharter,
        findings: &[ResearchFinding],) -> Result<ResearchSummary, GenesisError>;
// pub
fn synthesize_from_dimension_texts(charter: &ProjectCharter,
        dimension_contents: &[(&str, &str);
```

---

### `src/workflow/manifest.rs` {#src-workflow-manifest-rs}

- **Source Link:** [`src/workflow/manifest.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/manifest.rs)
- **Lines of Code:** 570 (23540 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Declarative TOML workflow manifest parser, schema models, and strict validation.

#### Types & Trait Declarations
- **Structs (6):** `InputBindingManifest`, `OutputBindingManifest`, `QualityGateManifest`, `WorkflowHeaderManifest`, `WorkflowManifest`, `WorkflowStepManifest`

#### Key Functions & Signatures (7 shown)
```rust
// private
fn default_manifest_version() -> u32;
// private
fn default_workflow_version() -> u32;
// private
fn default_step_timeout() -> u64;
// pub
fn from_toml_str(toml_str: &str) -> Result<Self, WorkflowError>;
// pub
fn from_file(path: &Path, workspace_root: Option<&Path>) -> Result<Self, WorkflowError>;
// pub
fn validate(&self, workspace_root: Option<&Path>) -> Result<(), WorkflowError>;
// private
fn detect_cycles(&self) -> Result<(), WorkflowError>;
```

---

### `src/workflow/mod.rs` {#src-workflow-mod-rs}

- **Source Link:** [`src/workflow/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/mod.rs)
- **Lines of Code:** 101 (3662 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Workflow domain contracts, manifest parsing, prompt catalog, quality gates, and persistence.  # Architecture Invariant  Workflow orchestrates above Mission and Task:  ```text Workflow ↓ WorkflowStep ↓ Mission ↓ TaskGraph ↓ Scheduler ↓ AgentRuntime ```  "The model proposes. The runtime decides."

---

### `src/workflow/planning/adr.rs` {#src-workflow-planning-adr-rs}

- **Source Link:** [`src/workflow/planning/adr.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/planning/adr.rs)
- **Lines of Code:** 457 (14882 bytes)

#### Primary Responsibility
Architecture Decision Record (ADR) domain model, registry, and projections.

#### Types & Trait Declarations
- **Structs (3):** `AdrId`, `AdrRegistry`, `ArchitectureDecisionRecord`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(id: impl Into<String>) -> Self;
// pub
fn from_number(num: usize) -> Self;
// pub
fn as_str(&self) -> &str;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(s: &str) -> Self;
// private
fn from(s: String) -> Self;
// pub
fn new(id: AdrId,
        title: impl Into<String>,
        context: impl Into<String>,
        decision: impl Into<Stri;
// pub
fn with_alternatives(mut self, alternatives: Vec<String>) -> Self;
// pub
fn with_consequences(mut self, consequences: Vec<String>) -> Self;
// pub
fn with_residual_risks(mut self, risks: Vec<String>) -> Self;
// pub
fn with_linked_requirements(mut self, requirements: Vec<RequirementKey>) -> Self;
// pub
fn with_linked_research(mut self, research: Vec<String>) -> Self;
// pub
fn with_status(mut self, status: DecisionStatus) -> Self;
// pub
fn to_markdown(&self) -> String;
// pub
fn new() -> Self;
```

---

### `src/workflow/planning/architecture.rs` {#src-workflow-planning-architecture-rs}

- **Source Link:** [`src/workflow/planning/architecture.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/planning/architecture.rs)
- **Lines of Code:** 473 (16619 bytes)

#### Primary Responsibility
Architecture models, component topologies, security trust boundaries, and ARCHITECTURE.md projection.

#### Types & Trait Declarations
- **Structs (7):** `ArchitectureComponent`, `ArchitectureDataStore`, `ArchitectureDocument`, `ArchitectureInterface`, `ArchitectureSubsystem`, `DeploymentBoundary`, `TrustBoundary`
- **Enums (1):** `ComponentStatus`

#### Key Functions & Signatures (12 shown)
```rust
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// pub
fn new(id: impl Into<String>,
        name: impl Into<String>,
        subsystem: impl Into<String>,
        responsibil;
// pub
fn with_depends_on(mut self, depends_on: Vec<String>) -> Self;
// pub
fn with_requirements(mut self, requirements: Vec<RequirementKey>) -> Self;
// pub
fn with_status(mut self, status: ComponentStatus) -> Self;
// pub
fn new(id: impl Into<String>,
        name: impl Into<String>,
        description: impl Into<String>,) -> Self;
// pub
fn new(id: impl Into<String>,
        name: impl Into<String>,
        provider: impl Into<String>,
        contract_typ;
// pub
fn new(project_name: impl Into<String>, system_context: impl Into<String>) -> Self;
// pub
fn sort_deterministic(&mut self);
// pub
fn add_component(&mut self, comp: ArchitectureComponent) -> Result<(), WorkflowError>;
// pub
fn to_markdown(&self) -> String;
// pub
fn save_to_dir(&self,
        workspace_root: &Path,
        projection_dir: &str,) -> Result<PathBuf, WorkflowError>;
```

---

### `src/workflow/planning/architecture_synthesizer.rs` {#src-workflow-planning-architecture_synthesizer-rs}

- **Source Link:** [`src/workflow/planning/architecture_synthesizer.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/planning/architecture_synthesizer.rs)
- **Lines of Code:** 702 (31449 bytes)

#### Primary Responsibility
System Architecture Synthesizer extracting topologies, interfaces, and candidate ADRs.

#### Types & Trait Declarations
- **Structs (2):** `ArchitectureSynthesizer`, `DerivedGroup`

#### Key Functions & Signatures (5 shown)
```rust
// pub
fn synthesize(requirements: &RequirementsDocument,
        charter: &ProjectCharter,
        summary: Option<&ResearchSu;
// private
fn slugify(text: &str) -> String;
// private
fn content_hash(inputs: &[&str]) -> String;
// private
fn category_label(category: RequirementCategory) -> String;
// private
fn derive_requirement_groups(project_name: &str,
    requirements: &RequirementsDocument,
    findings: &[ResearchFindin;
```

---

### `src/workflow/planning/decision.rs` {#src-workflow-planning-decision-rs}

- **Source Link:** [`src/workflow/planning/decision.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/planning/decision.rs)
- **Lines of Code:** 90 (3329 bytes)

#### Primary Responsibility
Architectural decision statuses and governance rules.

#### Types & Trait Declarations
- **Enums (1):** `DecisionStatus`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn is_authoritative(&self) -> bool;
// pub
fn can_transition_to(&self, new_status: DecisionStatus) -> bool;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn test_decision_status_transitions();
// private
fn test_authoritative_rule();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_decision_status_transitions`, `test_authoritative_rule`

---

### `src/workflow/planning/invalidation.rs` {#src-workflow-planning-invalidation-rs}

- **Source Link:** [`src/workflow/planning/invalidation.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/planning/invalidation.rs)
- **Lines of Code:** 214 (7630 bytes)

#### Primary Responsibility
Cascading planning invalidation and change impact analysis (Section 31, 32, 33).

#### Types & Trait Declarations
- **Structs (2):** `PlanningChangeSet`, `PlanningInvalidator`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn has_changes(&self) -> bool;
// pub
fn compute_changeset(old_reqs: &RequirementsDocument,
        new_reqs: &RequirementsDocument,
        arch: &Architectu;
// pub
fn apply_invalidation(changeset: &PlanningChangeSet,
        arch: &mut ArchitectureDocument,
        adrs: &mut AdrRegi;
```

---

### `src/workflow/planning/mod.rs` {#src-workflow-planning-mod-rs}

- **Source Link:** [`src/workflow/planning/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/planning/mod.rs)
- **Lines of Code:** 389 (14648 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Upstream planning, specifications, ADRs, risk register, and phased roadmap.  # Architecture Invariant  ```text Project Charter (PROJECT.md) + Research Summary (SUMMARY.md) ↓ Requirements Synthesizer (REQUIREMENTS.md) ↓ System Architect (ARCHITECTURE.md + DECISIONS.md) ↓ Risk Register (RISKS.md) ↓ Roadmap Architect (ROADMAP.md) ↓ Planning State (STATE.md) ↓ Human Approval Gate ↓ Implementation Handoff (ImplementationReady) ```  "The model proposes. The runtime decides."

#### Types & Trait Declarations
- **Structs (2):** `PlanningCoordinator`, `PlanningPipelineOutcome`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn save_planning_document(workspace_root: &Path,
    projection_dir: &str,
    filename: &str,
    content: &str,) -> Re;
// pub
async fn register_artifacts(&self,
        artifact_service: &crate::persistence::artifacts::ArtifactService,
        pa;
// pub
fn run_planning(charter: &ProjectCharter,
        summary: Option<&ResearchSummary>,
        findings: &[ResearchFinding;
```

---

### `src/workflow/planning/requirements.rs` {#src-workflow-planning-requirements-rs}

- **Source Link:** [`src/workflow/planning/requirements.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/planning/requirements.rs)
- **Lines of Code:** 243 (8759 bytes)

#### Primary Responsibility
Authoritative requirements document model and Markdown projections.  Re-exports and extends M31A's authoritative `EngineeringRequirement` domain model.

#### Types & Trait Declarations
- **Structs (1):** `RequirementsDocument`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn new(project_name: impl Into<String>, scope: impl Into<String>) -> Self;
// pub
fn sort_deterministic(&mut self);
// pub
fn by_category(&self, category: RequirementCategory) -> Vec<&EngineeringRequirement>;
// pub
fn get(&self, key: &RequirementKey) -> Option<&EngineeringRequirement>;
// pub
fn add_requirement(&mut self, req: EngineeringRequirement) -> Result<(), WorkflowError>;
// pub
fn add_or_update(&mut self, req: EngineeringRequirement);
// pub
fn to_markdown(&self) -> String;
// pub
fn save_to_dir(&self,
        workspace_root: &Path,
        projection_dir: &str,) -> Result<PathBuf, WorkflowError>;
```

---

### `src/workflow/planning/requirements_synthesizer.rs` {#src-workflow-planning-requirements_synthesizer-rs}

- **Source Link:** [`src/workflow/planning/requirements_synthesizer.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/planning/requirements_synthesizer.rs)
- **Lines of Code:** 296 (12520 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Requirements Synthesizer extracting EngineeringRequirements from Genesis artifacts.

#### Types & Trait Declarations
- **Structs (1):** `RequirementsSynthesizer`

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn synthesize(charter: &ProjectCharter,
        summary: Option<&ResearchSummary>,
        findings: &[ResearchFinding],;
```

---

### `src/workflow/planning/risks.rs` {#src-workflow-planning-risks-rs}

- **Source Link:** [`src/workflow/planning/risks.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/planning/risks.rs)
- **Lines of Code:** 280 (8925 bytes)

#### Primary Responsibility
Risk register, assumptions, unknowns, and RISKS.md projection.

#### Types & Trait Declarations
- **Structs (2):** `RiskEntry`, `RiskRegister`
- **Enums (3):** `QualitativeImpact`, `QualitativeLikelihood`, `RiskStatus`

#### Key Functions & Signatures (13 shown)
```rust
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// pub
fn new(id: impl Into<String>,
        description: impl Into<String>,
        source: impl Into<String>,
        likelih;
// pub
fn with_requirements(mut self, reqs: Vec<RequirementKey>) -> Self;
// pub
fn with_components(mut self, comps: Vec<String>) -> Self;
// pub
fn new() -> Self;
// pub
fn add_risk(&mut self, risk: RiskEntry);
// pub
fn add_assumption(&mut self, assumption: PlanningAssumption);
// pub
fn add_unknown(&mut self, unknown: PlanningUnknown);
// pub
fn sort_deterministic(&mut self);
// pub
fn to_markdown(&self) -> String;
// pub
fn save_to_dir(&self,
        workspace_root: &Path,
        projection_dir: &str,) -> Result<PathBuf, WorkflowError>;
```

---

### `src/workflow/planning/roadmap.rs` {#src-workflow-planning-roadmap-rs}

- **Source Link:** [`src/workflow/planning/roadmap.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/planning/roadmap.rs)
- **Lines of Code:** 825 (31866 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Dependency-aware Roadmap DAG compilation, phase sequencing, and ROADMAP.md projection.

#### Types & Trait Declarations
- **Structs (4):** `Roadmap`, `RoadmapDependency`, `RoadmapPhase`, `RoadmapSynthesizer`
- **Enums (1):** `RoadmapPhaseStatus`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// pub
fn new(id: impl Into<String>,
        name: impl Into<String>,
        objective: impl Into<String>,
        verificatio;
// pub
fn with_requirements(mut self, reqs: Vec<RequirementKey>) -> Self;
// pub
fn with_architecture(mut self, arch_refs: Vec<String>) -> Self;
// pub
fn with_dependencies(mut self, deps: Vec<String>) -> Self;
// pub
fn with_exit_criteria(mut self, criteria: Vec<String>) -> Self;
// pub
fn with_enabling(mut self, enabling: bool) -> Self;
// pub
fn with_risks(mut self, risks: Vec<String>) -> Self;
// pub
fn new(id: impl Into<String>, objective: impl Into<String>) -> Self;
// pub
fn add_phase(&mut self, phase: RoadmapPhase);
// pub
fn get_phase(&self, id: &str) -> Option<&RoadmapPhase>;
// pub
fn get_phase_mut(&mut self, id: &str) -> Option<&mut RoadmapPhase>;
// pub
fn validate_dag(&self) -> Result<Vec<String>, WorkflowError>;
// pub
fn to_markdown(&self) -> String;
// pub
fn save_to_dir(&self,
        workspace_root: &Path,
        projection_dir: &str,) -> Result<PathBuf, WorkflowError>;
```

---

### `src/workflow/planning/state.rs` {#src-workflow-planning-state-rs}

- **Source Link:** [`src/workflow/planning/state.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/planning/state.rs)
- **Lines of Code:** 437 (18172 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Planning lifecycle state machine and STATE.md projection.

#### Types & Trait Declarations
- **Structs (2):** `PlanningState`, `PlanningStateMachine`
- **Enums (1):** `PlanningLifecycleState`

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn can_transition_to(&self, target: PlanningLifecycleState) -> bool;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn new() -> Self;
// pub
fn transition_to(&mut self,
        next: PlanningLifecycleState,
        reason: impl Into<String>,) -> Result<(), Work;
// private
fn default() -> Self;
// pub
fn new(project_name: impl Into<String>, lifecycle_state: PlanningLifecycleState) -> Self;
// pub
fn to_markdown(&self) -> String;
// pub
fn save_to_dir(&self,
        workspace_root: &Path,
        projection_dir: &str,) -> Result<PathBuf, WorkflowError>;
// pub
fn from_markdown(content: &str) -> Result<Self, WorkflowError>;
```

---

### `src/workflow/planning/traceability.rs` {#src-workflow-planning-traceability-rs}

- **Source Link:** [`src/workflow/planning/traceability.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/planning/traceability.rs)
- **Lines of Code:** 218 (7287 bytes)

#### Primary Responsibility
Bidirectional traceability matrix linking requirements, research, architecture, ADRs, and roadmap phases.

#### Types & Trait Declarations
- **Structs (2):** `TraceLink`, `TraceabilityMatrix`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn new() -> Self;
// pub
fn build(requirements: &RequirementsDocument,
        arch: &ArchitectureDocument,
        adrs: &AdrRegistry,
        r;
// pub
fn validate(&self) -> Result<(), Vec<String>>;
// pub
fn to_markdown(&self) -> String;
```

---

### `src/workflow/planning/validation.rs` {#src-workflow-planning-validation-rs}

- **Source Link:** [`src/workflow/planning/validation.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/planning/validation.rs)
- **Lines of Code:** 353 (14309 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Quality gates for Requirements, Architecture, and Roadmap synthesis.

#### Types & Trait Declarations
- **Structs (1):** `PlanningQualityGates`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn evaluate_requirements_tier1(reqs: &RequirementsDocument) -> QualityGateResult;
// pub
fn evaluate_requirements_tier2(reqs: &RequirementsDocument) -> QualityGateResult;
// pub
fn evaluate_architecture_tier1(arch: &ArchitectureDocument) -> QualityGateResult;
// pub
fn evaluate_architecture_tier2(arch: &ArchitectureDocument,
        reqs: &RequirementsDocument,
        adrs: &AdrRegis;
// pub
fn evaluate_roadmap_tier1(roadmap: &Roadmap) -> QualityGateResult;
// pub
fn evaluate_roadmap_tier2(roadmap: &Roadmap,
        reqs: &RequirementsDocument,
        arch: &ArchitectureDocument,) ;
```

---

### `src/workflow/provenance.rs` {#src-workflow-provenance-rs}

- **Source Link:** [`src/workflow/provenance.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/provenance.rs)
- **Lines of Code:** 184 (7118 bytes)

#### Primary Responsibility
Provenance tracking and cryptographic content hashing for compiled workflows.

#### Types & Trait Declarations
- **Structs (2):** `StepProvenance`, `WorkflowProvenance`

#### Key Functions & Signatures (5 shown)
```rust
// pub
fn new(step_key: impl Into<String>,
        prompt_id: impl Into<String>,
        prompt_version: u32,
        prompt_co;
// pub
fn with_invocation_provenance(mut self, prov: &PromptInvocationProvenance) -> Self;
// pub
fn new(manifest_id: impl Into<String>,
        manifest_version: u32,
        manifest_hash: impl Into<String>,
        ;
// pub
fn calculate_composite_hash(manifest_hash: &str,
        step_provenance: &BTreeMap<String, StepProvenance>,) -> String;
// pub
fn verify(&self,
        current_manifest_hash: &str,
        current_prompt_hashes: &BTreeMap<String, String>,) -> Resu;
```

---

### `src/workflow/quality_gate.rs` {#src-workflow-quality_gate-rs}

- **Source Link:** [`src/workflow/quality_gate.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/quality_gate.rs)
- **Lines of Code:** 462 (18150 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
QualityGate contracts, deterministic Tier-1 and Tier-2 evaluation, and violation reporting.

#### Types & Trait Declarations
- **Structs (5):** `QualityGateContext`, `QualityGateResult`, `QualityGateViolation`, `Tier1QualityGateEvaluator`, `Tier2QualityGateEvaluator`
- **Enums (2):** `QualityGateSeverity`, `QualityGateTier`
- **Traits (1):** `QualityGateEvaluator`

#### Key Functions & Signatures (9 shown)
```rust
// pub
fn error(code: impl Into<String>,
        message: impl Into<String>,
        step_key: Option<String>,
        artifact;
// pub
fn warning(code: impl Into<String>,
        message: impl Into<String>,
        step_key: Option<String>,
        artifa;
// pub
fn pass(tier: QualityGateTier) -> Self;
// pub
fn fail(tier: QualityGateTier, mut violations: Vec<QualityGateViolation>) -> Self;
// private
fn evaluate(&self,
        gate: &QualityGate,
        context: &QualityGateContext<'_>,) -> Result<QualityGateResult, W;
// pub
fn new() -> Self;
// private
fn evaluate(&self,
        gate: &QualityGate,
        context: &QualityGateContext<'_>,) -> Result<QualityGateResult, W;
// pub
fn new() -> Self;
// private
fn evaluate(&self,
        gate: &QualityGate,
        context: &QualityGateContext<'_>,) -> Result<QualityGateResult, W;
```

---

### `src/workflow/repository.rs` {#src-workflow-repository-rs}

- **Source Link:** [`src/workflow/repository.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/repository.rs)
- **Lines of Code:** 900 (31251 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
SQLite persistence and repository trait for workflow runs, steps, and artifacts.

#### Types & Trait Declarations
- **Structs (1):** `SqliteWorkflowRepository`
- **Traits (1):** `WorkflowRepository`

#### Key Functions & Signatures (15 shown)
```rust
// private
async fn create_run(&self, run: &WorkflowRun) -> Result<(), WorkflowError>;
// private
async fn get_run(&self, id: WorkflowRunId) -> Result<Option<WorkflowRun>, WorkflowError>;
// private
async fn get_run_by_execution_run_id(&self,
        execution_run_id: ExecutionRunId,) -> Result<Option<WorkflowRun>, Wo;
// private
async fn update_run(&self, run: &WorkflowRun) -> Result<(), WorkflowError>;
// private
async fn create_step_run(&self, step_run: &WorkflowStepRun) -> Result<(), WorkflowError>;
// private
async fn get_step_run(&self,
        id: WorkflowStepRunId,) -> Result<Option<WorkflowStepRun>, WorkflowError>;
// private
async fn get_step_run_by_key(&self,
        run_id: WorkflowRunId,
        step_key: &str,) -> Result<Option<WorkflowSte;
// private
async fn update_step_run(&self, step_run: &WorkflowStepRun) -> Result<(), WorkflowError>;
// private
async fn list_step_runs(&self,
        run_id: WorkflowRunId,) -> Result<Vec<WorkflowStepRun>, WorkflowError>;
// private
async fn record_artifact(&self, artifact: &WorkflowArtifact) -> Result<(), WorkflowError>;
// private
async fn get_artifact(&self, id: ArtifactId) -> Result<Option<WorkflowArtifact>, WorkflowError>;
// private
async fn list_artifacts(&self,
        run_id: WorkflowRunId,) -> Result<Vec<WorkflowArtifact>, WorkflowError>;
// private
async fn list_step_artifacts(&self,
        step_run_id: WorkflowStepRunId,) -> Result<Vec<WorkflowArtifact>, WorkflowEr;
// private
async fn update_artifact_status(&self,
        id: ArtifactId,
        status: WorkflowArtifactStatus,) -> Result<(), Wo;
// private
async fn advance_step_and_update_run(&self,
        run: &WorkflowRun,
        step_run: &WorkflowStepRun,) -> Result<();
```

---

### `src/workflow/state.rs` {#src-workflow-state-rs}

- **Source Link:** [`src/workflow/state.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/workflow/state.rs)
- **Lines of Code:** 628 (18892 bytes)

#### Primary Responsibility
Durable state aggregates and transition validation for workflow runs and steps.

#### Types & Trait Declarations
- **Structs (3):** `WorkflowArtifact`, `WorkflowRun`, `WorkflowStepRun`
- **Enums (4):** `WorkflowArtifactStatus`, `WorkflowMode`, `WorkflowRunState`, `WorkflowStepState`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn can_transition_to(&self, target: WorkflowRunState) -> bool;
// pub
fn is_terminal(&self) -> bool;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn can_transition_to(&self, target: WorkflowStepState) -> bool;
// pub
fn is_terminal(&self) -> bool;
// pub
fn new(definition_id: impl Into<String>,
        definition_version: u32,
        workspace_root: PathBuf,
        mode:;
// pub
fn with_run_id(mut self, run_id: ExecutionRunId) -> Self;
// pub
fn transition_to(&mut self,
        new_state: WorkflowRunState,
        error_summary: Option<String>,) -> Result<(), W;
// pub
fn new(workflow_run_id: WorkflowRunId, step_key: impl Into<String>) -> Self;
// pub
fn transition_to(&mut self,
        new_state: WorkflowStepState,
        halt_reason: Option<String>,) -> Result<(), Wo;
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_workflow_run_lifecycle_transitions`, `test_invalid_workflow_run_transitions`, `test_step_run_transitions`, `test_step_retry_increments_attempt`

---
