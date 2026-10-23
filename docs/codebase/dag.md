# DAG & Critical Path Method

> **Architectural Layer:** L5 Planning  
> **Source Directory:** `src/dag`  
> **File Count:** 7 source files  

Directed acyclic task graphs, topological sorting, critical path analysis, and reconciliation.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [cpm.rs](#src-dag-cpm-rs) | 274 | `CriticalPathInfo, ScheduleDrift` | Dual-track Critical Path Method (CPM) engine (D-11, DAG-05).  Provides... |
| [graph.rs](#src-dag-graph-rs) | 364 | `DependencyEdge, TaskGraph, DependencyKind` | TaskGraph authoritative domain aggregate and dependency edge model (D-... |
| [materializer.rs](#src-dag-materializer-rs) | 383 | `TaskGraphMaterializer, MaterializationLane` | Atomic transactional materialization of CandidatePlan into authoritati... |
| [mod.rs](#src-dag-mod-rs) | 20 | `Functions/Traits` | Authoritative TaskGraph domain model, defensive DAG validation, CPM, a... |
| [ops.rs](#src-dag-ops-rs) | 864 | `DependencyAnomalies, GraphAdjacency, GraphError` | Domain-neutral, strongly-typed, deterministic directed acyclic graph (... |
| [reconciler.rs](#src-dag-reconciler-rs) | 372 | `ReconciliationResult, TaskGraphReconciler` | Subsystem component |
| [validator.rs](#src-dag-validator-rs) | 315 | `TaskGraphValidator, GraphValidationError` | Defensive Task DAG validator with deterministic cycle detection (D-16,... |

---

### `src/dag/cpm.rs` {#src-dag-cpm-rs}

- **Source Link:** [`src/dag/cpm.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/dag/cpm.rs)
- **Lines of Code:** 274 (10214 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Dual-track Critical Path Method (CPM) engine (D-11, DAG-05).  Provides baseline and live schedule projection, early/late time computation, total slack (float), critical path detection, and schedule drift analysis.

#### Types & Trait Declarations
- **Structs (2):** `CriticalPathInfo`, `ScheduleDrift`

#### Key Functions & Signatures (5 shown)
```rust
// pub
fn calculate_drift(baseline: &CriticalPathInfo, live: &CriticalPathInfo) -> ScheduleDrift;
// pub
fn calculate_cpm(topological_order: &[TaskId],
    prerequisites_of: &BTreeMap<TaskId, BTreeSet<TaskId>>,
    dependents;
// private
fn test_linear_cpm();
// private
fn test_diamond_cpm_slack();
// private
fn test_schedule_drift();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_linear_cpm`, `test_diamond_cpm_slack`, `test_schedule_drift`

---

### `src/dag/graph.rs` {#src-dag-graph-rs}

- **Source Link:** [`src/dag/graph.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/dag/graph.rs)
- **Lines of Code:** 364 (12694 bytes)

#### Primary Responsibility
TaskGraph authoritative domain aggregate and dependency edge model (D-09, D-13, D-15).

#### Types & Trait Declarations
- **Structs (2):** `DependencyEdge`, `TaskGraph`
- **Enums (1):** `DependencyKind`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn hard(prerequisite_id: TaskId, dependent_id: TaskId) -> Self;
// pub
fn soft(prerequisite_id: TaskId, dependent_id: TaskId) -> Self;
// pub
fn build_from_records(id: TaskGraphId,
        mission_id: MissionId,
        revision: u32,
        plan_id: String,
  ;
// pub
fn canonical_run_id(&self) -> ExecutionRunId;
// pub
fn rebuild_derived_indexes(&mut self);
// pub
fn is_dependency_satisfied(&self, task_id: TaskId) -> bool;
// pub
fn find_task_by_candidate_key(&self, key: &CandidateTaskKey) -> Option<&Task>;
// pub
fn find_candidate_key(&self, id: TaskId) -> Option<&CandidateTaskKey>;
// pub
fn get_task(&self, id: TaskId) -> Option<&Task>;
// pub
fn get_task_mut(&mut self, id: TaskId) -> Option<&mut Task>;
// pub
fn topological_order(&self) -> Vec<TaskId>;
// pub
fn task_count(&self) -> usize;
// pub
fn edge_count(&self) -> usize;
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_task_graph_cache_reconstruction_and_wave_tiers`

---

### `src/dag/materializer.rs` {#src-dag-materializer-rs}

- **Source Link:** [`src/dag/materializer.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/dag/materializer.rs)
- **Lines of Code:** 383 (16571 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Atomic transactional materialization of CandidatePlan into authoritative TaskGraph (D-13, D-16, DAG-01).

#### Types & Trait Declarations
- **Structs (1):** `TaskGraphMaterializer`
- **Enums (1):** `MaterializationLane`

#### Key Functions & Signatures (5 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(pool: SqlitePool) -> Self;
// pub
async fn materialize_authorized(&self,
        mission_id: MissionId,
        plan: &CandidatePlan,
        plan_revisio;
// pub
async fn materialize_in_lane(&self,
        mission_id: MissionId,
        plan: &CandidatePlan,
        lane: Materiali;
// pub
async fn materialize(&self,
        mission_id: MissionId,
        plan: &CandidatePlan,) -> Result<TaskGraph, M31AError;
```

---

### `src/dag/mod.rs` {#src-dag-mod-rs}

- **Source Link:** [`src/dag/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/dag/mod.rs)
- **Lines of Code:** 20 (884 bytes)

#### Primary Responsibility
Authoritative TaskGraph domain model, defensive DAG validation, CPM, and reconciler.

---

### `src/dag/ops.rs` {#src-dag-ops-rs}

- **Source Link:** [`src/dag/ops.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/dag/ops.rs)
- **Lines of Code:** 864 (28284 bytes)

#### Primary Responsibility
Domain-neutral, strongly-typed, deterministic directed acyclic graph (DAG) algorithms.  This module serves as the single authoritative implementation for graph algorithms across the entire M31A codebase, replacing previously duplicated ad-hoc implementations.  Supported capabilities: 1. Defensive graph validation (self-loops, dangling endpoints, duplicate edges) 2. Cycle detection and deterministic cycle path extraction 3. Deterministic topological sorting (Kahn's algorithm with `BTreeSet` tie-breaking) 4. Topological execution wave / tier calculation 5. Dependency indexing (dependents, prerequisites, in-degrees, roots, leaves) 6. Transitive reachability (ancestors, descendants) 7. Readiness evaluation against completed prerequisites  Domain aggregates (Roadmap, Workflow, TaskGraph, Scheduler waves) preserve their distinct domain semantics and boundaries while delegating all graph operations to this module.

#### Types & Trait Declarations
- **Structs (2):** `DependencyAnomalies`, `GraphAdjacency`
- **Enums (1):** `GraphError`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn is_empty(&self) -> bool;
// pub
fn build(nodes: impl IntoIterator<Item = N>,
        edges: impl IntoIterator<Item = (N, N);
// pub
fn build_validated(nodes: impl IntoIterator<Item = N>,
        edges: impl IntoIterator<Item = (N, N);
// pub
fn topological_sort(&self) -> Result<Vec<N>, GraphError<N>>;
// pub
fn compute_waves(&self) -> Result<Vec<Vec<N>>, GraphError<N>>;
// pub
fn compute_wave_tiers_with_sorter(&self,
        mut sorter: F,) -> Result<BTreeMap<usize, Vec<N>>, GraphError<N>>
    w;
// pub
fn compute_wave_tiers_permissive(&self, mut sorter: F) -> BTreeMap<usize, Vec<N>>
    where
        F: FnMut(&mut [N]),;
// pub
fn is_ready(&self, node: &N, completed: &BTreeSet<N>) -> bool;
// pub
fn ready_nodes(&self,
        candidates: impl IntoIterator<Item = &'a N>,
        completed: &BTreeSet<N>,) -> Vec<N>
 ;
// pub
fn ancestors_of(&self, node: &N) -> BTreeSet<N>;
// pub
fn descendants_of(&self, node: &N) -> BTreeSet<N>;
// pub
fn roots(&self) -> BTreeSet<N>;
// pub
fn leaves(&self) -> BTreeSet<N>;
// pub
fn topological_sort(nodes: impl IntoIterator<Item = N>,
    edges: impl IntoIterator<Item = (N, N);
```

#### Unit Verification (9 inline tests)
Tests defined within module:
`test_empty_graph`, `test_single_node`, `test_linear_dag`, `test_diamond_dag`, `test_cycle_detection`, `test_self_loop`, `test_missing_endpoint`, `test_duplicate_edge`, `test_readiness_determination`

---

### `src/dag/reconciler.rs` {#src-dag-reconciler-rs}

- **Source Link:** [`src/dag/reconciler.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/dag/reconciler.rs)
- **Lines of Code:** 372 (16093 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (2):** `ReconciliationResult`, `TaskGraphReconciler`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn compute_task_fingerprint(task: &CandidateTask) -> String;
// pub
fn new(pool: SqlitePool) -> Self;
// pub
async fn reconcile(&self,
        mission_id: MissionId,
        old_graph: &TaskGraph,
        new_plan: &CandidatePlan;
// pub
async fn reconcile_with_summary(&self,
        mission_id: MissionId,
        old_graph: &TaskGraph,
        new_plan: &;
```

---

### `src/dag/validator.rs` {#src-dag-validator-rs}

- **Source Link:** [`src/dag/validator.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/dag/validator.rs)
- **Lines of Code:** 315 (10344 bytes)

#### Primary Responsibility
Defensive Task DAG validator with deterministic cycle detection (D-16, DAG-01, DAG-06).

#### Types & Trait Declarations
- **Structs (1):** `TaskGraphValidator`
- **Enums (1):** `GraphValidationError`

#### Key Functions & Signatures (13 shown)
```rust
// private
fn from(err: crate::dag::ops::GraphError<N>) -> Self;
// pub
fn new() -> Self;
// pub
fn validate_candidate_plan(&self,
        plan: &CandidatePlan,) -> Result<Vec<CandidateTaskKey>, GraphValidationError>;
// pub
fn validate_graph(&self,
        tasks: &BTreeMap<TaskId, Task>,
        edges: &BTreeSet<DependencyEdge>,) -> Result<Ve;
// private
fn make_candidate(id: &str, depends_on: Vec<&str>) -> CandidateTask;
// private
fn test_reject_empty_plan();
// private
fn test_reject_self_loop();
// private
fn test_reject_direct_two_node_cycle();
// private
fn test_reject_three_node_indirect_cycle();
// private
fn test_reject_missing_endpoint();
// private
fn test_reject_duplicate_dependency();
// private
fn test_deterministic_topological_sort();
// private
fn test_validate_graph_roundtrip();
```

#### Unit Verification (8 inline tests)
Tests defined within module:
`test_reject_empty_plan`, `test_reject_self_loop`, `test_reject_direct_two_node_cycle`, `test_reject_three_node_indirect_cycle`, `test_reject_missing_endpoint`, `test_reject_duplicate_dependency`, `test_deterministic_topological_sort`, `test_validate_graph_roundtrip`

---
