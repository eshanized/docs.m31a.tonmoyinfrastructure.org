# Scheduler & Job Admission

> **Architectural Layer:** L5 Scheduling  
> **Source Directory:** `src/scheduler`  
> **File Count:** 10 source files  

Global job worker pool, concurrency limits, and task scheduling.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [concurrency.rs](#src-scheduler-concurrency-rs) | 202 | `ConcurrencyLimiter, ConcurrencyLimits, ConcurrencyReservation` | Subsystem component |
| [engine.rs](#src-scheduler-engine-rs) | 1296 | `SchedulerEngine` | Subsystem component |
| [events.rs](#src-scheduler-events-rs) | 402 | `Functions/Traits` | Subsystem component |
| [mod.rs](#src-scheduler-mod-rs) | 15 | `Functions/Traits` | Task DAG scheduler, concurrency limiter, and resource locking subsyste... |
| [queue.rs](#src-scheduler-queue-rs) | 217 | `PriorityDispatchQueue, QueueTaskEntry` | Subsystem component |
| [key.rs](#src-scheduler-resources-key-rs) | 255 | `ResourceKey, LockMode, PathScope` | Subsystem component |
| [lease.rs](#src-scheduler-resources-lease-rs) | 221 | `ActiveLease, LeaseId, ResourceLeaseGuard` | Subsystem component |
| [manager.rs](#src-scheduler-resources-manager-rs) | 318 | `ResourceConflictError, ResourceManager, ResourceManagerInner` | Subsystem component |
| [mod.rs](#src-scheduler-resources-mod-rs) | 9 | `Functions/Traits` | Hierarchical resource locking and conflict resolution. |
| [snapshot.rs](#src-scheduler-snapshot-rs) | 74 | `QueueStatistics, SchedulerSnapshot` | Subsystem component |

---

### `src/scheduler/concurrency.rs` {#src-scheduler-concurrency-rs}

- **Source Link:** [`src/scheduler/concurrency.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/scheduler/concurrency.rs)
- **Lines of Code:** 202 (6753 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (3):** `ConcurrencyLimiter`, `ConcurrencyLimits`, `ConcurrencyReservation`
- **Enums (1):** `ConcurrencyExhaustedError`

#### Key Functions & Signatures (9 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn active_global_workers(&self) -> usize;
// pub
fn active_for_role(&self, role: AgentRole) -> usize;
// pub
fn can_reserve(&self,
        role: AgentRole,
        limits: &ConcurrencyLimits,) -> Result<(), ConcurrencyExhaustedEr;
// pub
fn try_reserve(&mut self,
        role: AgentRole,
        limits: &ConcurrencyLimits,) -> Result<ConcurrencyReservation;
// pub
fn release(&mut self, role: AgentRole);
// private
fn test_global_limit_rejection();
// private
fn test_role_limit_rejection();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_global_limit_rejection`, `test_role_limit_rejection`

---

### `src/scheduler/engine.rs` {#src-scheduler-engine-rs}

- **Source Link:** [`src/scheduler/engine.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/scheduler/engine.rs)
- **Lines of Code:** 1296 (48112 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (1):** `SchedulerEngine`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn compute_cpm_for_graph(graph: &TaskGraph) -> CriticalPathInfo;
// pub
fn new(pool: SqlitePool,
        resource_manager: Arc<ResourceManager>,
        limits: ConcurrencyLimits,
        even;
// pub
fn resource_manager(&self) -> &Arc<ResourceManager>;
// pub
async fn set_task_resources(&self,
        task_id: TaskId,
        resources: Vec<(ResourceKey, LockMode);
// pub
async fn get_task_resources(&self, task_id: TaskId) -> Vec<(ResourceKey, LockMode)>;
// pub
async fn ensure_active_graph_loaded(&self,
        mission_id: MissionId,) -> Result<(), SchedulerError>;
// pub
async fn materialize_plan(&self,
        mission_id: MissionId,
        plan: &CandidatePlan,) -> Result<TaskGraphId, Sc;
// pub
async fn reconcile_plan(&self,
        mission_id: MissionId,
        new_plan: &CandidatePlan,) -> Result<(TaskGraphId,;
// private
fn task_repo(&self) -> crate::persistence::sqlite::repositories::SqliteTaskRepository;
// pub
async fn mark_task_completed(&self,
        task_id: TaskId,
        result: impl Into<Option<TaskResult>>,) -> Result<(;
// pub
async fn mark_task_failed(&self,
        task_id: TaskId,
        error_summary: String,
        retryable: bool,) -> Re;
// pub
async fn mark_task_skipped(&self,
        task_id: TaskId,
        reason: String,) -> Result<(), SchedulerError>;
// pub
async fn mark_task_needs_review(&self, task_id: TaskId) -> Result<(), SchedulerError>;
// pub
async fn review_task(&self,
        task_id: TaskId,
        approved: bool,
        reviewer: String,) -> Result<(), Sc;
// pub
async fn cancel_task(&self, task_id: TaskId) -> Result<(), SchedulerError>;
```

---

### `src/scheduler/events.rs` {#src-scheduler-events-rs}

- **Source Link:** [`src/scheduler/events.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/scheduler/events.rs)
- **Lines of Code:** 402 (10171 bytes)

#### Primary Responsibility
Internal implementation file.

#### Key Functions & Signatures (15 shown)
```rust
// pub
async fn emit_graph_materialized(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    graph_id: Ta;
// pub
async fn emit_wave_tier(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    graph_id: TaskGraphId;
// pub
async fn emit_resource_leased(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    lease_id: uuid:;
// pub
async fn emit_resource_released(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    lease_id: uui;
// pub
async fn emit_task_blocked(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    task_id: TaskId,
 ;
// pub
async fn emit_task_unblocked(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    task_id: TaskId,;
// pub
async fn emit_critical_path_recalculated(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    grap;
// pub
async fn emit_task_started(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    task_id: TaskId,
 ;
// pub
async fn emit_task_completed(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    task_id: TaskId,;
// pub
async fn emit_task_failed(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    task_id: TaskId,
  ;
// pub
async fn emit_task_cancelled(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    task_id: TaskId,;
// pub
async fn emit_task_attempt_failed(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    task_id: Ta;
// pub
async fn emit_task_retry_scheduled(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    task_id: T;
// pub
async fn emit_task_skipped(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    task_id: TaskId,
 ;
// pub
async fn emit_task_needs_review(bus: &Arc<dyn EventBus>,
    sequence: u64,
    mission_id: MissionId,
    task_id: Task;
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_emit_scheduler_events`

---

### `src/scheduler/mod.rs` {#src-scheduler-mod-rs}

- **Source Link:** [`src/scheduler/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/scheduler/mod.rs)
- **Lines of Code:** 15 (449 bytes)

#### Primary Responsibility
Task DAG scheduler, concurrency limiter, and resource locking subsystem.

---

### `src/scheduler/queue.rs` {#src-scheduler-queue-rs}

- **Source Link:** [`src/scheduler/queue.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/scheduler/queue.rs)
- **Lines of Code:** 217 (6466 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (2):** `PriorityDispatchQueue`, `QueueTaskEntry`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(task_id: TaskId,
        base_priority: u32,
        on_critical_path: bool,
        required_resources: Vec<(Res;
// pub
fn effective_priority(&self, interval: u32, increment: u32, max_bonus: u32) -> u32;
// private
fn default() -> Self;
// pub
fn new(aging_interval: u32,
        aging_increment: u32,
        max_age_bonus: u32,
        starvation_threshold: u32,;
// pub
fn len(&self) -> usize;
// pub
fn is_empty(&self) -> bool;
// pub
fn entries(&self) -> &BTreeMap<TaskId, QueueTaskEntry>;
// pub
fn push(&mut self, entry: QueueTaskEntry);
// pub
fn remove(&mut self, task_id: TaskId) -> Option<QueueTaskEntry>;
// pub
fn get(&self, task_id: TaskId) -> Option<&QueueTaskEntry>;
// pub
fn record_bypass(&mut self, task_id: TaskId);
// pub
fn is_starving(&self, task_id: TaskId) -> bool;
// pub
fn pop_highest_feasible(&mut self, is_feasible: F) -> Option<QueueTaskEntry>
    where
        F: Fn(&QueueTaskEntry) ->;
// private
fn test_effective_priority_linear_aging();
// private
fn test_queue_bypass_dispatches_next_feasible();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_effective_priority_linear_aging`, `test_queue_bypass_dispatches_next_feasible`

---

### `src/scheduler/resources/key.rs` {#src-scheduler-resources-key-rs}

- **Source Link:** [`src/scheduler/resources/key.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/scheduler/resources/key.rs)
- **Lines of Code:** 255 (8813 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (1):** `ResourceKey`
- **Enums (3):** `LockMode`, `PathScope`, `ResourceNamespace`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn workspace(path: impl AsRef<Path>, scope: PathScope) -> Self;
// pub
fn repository(name: impl Into<String>) -> Self;
// pub
fn subsystem(name: impl Into<String>) -> Self;
// pub
fn capability(id: impl Into<String>) -> Self;
// pub
fn tool(name: impl Into<String>) -> Self;
// pub
fn custom(namespace: impl Into<String>, id: impl Into<String>) -> Self;
// pub
fn conflicts_with(&self,
        my_mode: LockMode,
        other: &ResourceKey,
        other_mode: LockMode,) -> bool;
// private
fn is_prefix_of(prefix: &[String], full: &[String]) -> bool;
// private
fn test_subtree_conflicts_with_descendant_exact();
// private
fn test_component_segment_boundary_prevents_false_positive();
// private
fn test_shared_shared_identical_file_does_not_conflict();
// private
fn test_exclusive_shared_identical_file_conflicts();
// private
fn test_exact_directory_does_not_conflict_with_descendant_file();
// private
fn test_disjoint_subtrees_do_not_conflict();
```

#### Unit Verification (7 inline tests)
Tests defined within module:
`test_subtree_conflicts_with_descendant_exact`, `test_component_segment_boundary_prevents_false_positive`, `test_shared_shared_identical_file_does_not_conflict`, `test_exclusive_shared_identical_file_conflicts`, `test_exact_directory_does_not_conflict_with_descendant_file`, `test_disjoint_subtrees_do_not_conflict`, `test_non_filesystem_namespaces`

---

### `src/scheduler/resources/lease.rs` {#src-scheduler-resources-lease-rs}

- **Source Link:** [`src/scheduler/resources/lease.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/scheduler/resources/lease.rs)
- **Lines of Code:** 221 (5722 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (4):** `ActiveLease`, `LeaseId`, `ResourceLeaseGuard`, `TestReleaser`
- **Traits (1):** `LeaseReleaser`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn from_uuid(uuid: Uuid) -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: LeaseId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
// private
fn release_leases(&self, task_id: TaskId, lease_ids: &[LeaseId]);
// pub
fn new(task_id: TaskId,
        lease_ids: Vec<LeaseId>,
        releaser: Option<Arc<dyn LeaseReleaser>>,) -> Self;
// pub
fn task_id(&self) -> TaskId;
// pub
fn lease_ids(&self) -> &[LeaseId];
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_lease_id_serde_roundtrip`, `test_lease_id_from_str`, `test_resource_lease_guard_drop_releases`, `test_resource_lease_guard_disarm_prevents_release`

---

### `src/scheduler/resources/manager.rs` {#src-scheduler-resources-manager-rs}

- **Source Link:** [`src/scheduler/resources/manager.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/scheduler/resources/manager.rs)
- **Lines of Code:** 318 (10947 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (3):** `ResourceConflictError`, `ResourceManager`, `ResourceManagerInner`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(pool: Option<SqlitePool>, owner_generation: u64) -> Self;
// pub
fn owner_generation(&self) -> u64;
// pub
fn active_leases_count(&self) -> usize;
// pub
fn get_task_leases(&self, task_id: TaskId) -> Vec<ActiveLease>;
// pub
fn check_availability(&self,
        requests: &[(ResourceKey, LockMode);
// pub
fn acquire(&self,
        task_id: TaskId,
        mission_id: MissionId,
        requests: Vec<(ResourceKey, LockMode);
// private
fn acquire_internal(&self,
        task_id: TaskId,
        mission_id: MissionId,
        requests: Vec<(ResourceKey, L;
// pub
async fn acquire_persisted(&self,
        task_id: TaskId,
        mission_id: MissionId,
        requests: Vec<(Resourc;
// pub
fn release_task_leases(&self, task_id: TaskId) -> Vec<ActiveLease>;
// private
fn release_task_leases_internal(&self, task_id: TaskId, spawn_bg: bool) -> Vec<ActiveLease>;
// pub
async fn release_task_leases_persisted(&self, task_id: TaskId) -> Vec<ActiveLease>;
// pub
fn revoke_task_leases(&self, task_id: TaskId, _reason: &str) -> Vec<ActiveLease>;
// private
fn release_leases(&self, task_id: TaskId, _lease_ids: &[LeaseId]);
// private
async fn insert_leases_sqlite(pool: &SqlitePool, leases: &[ActiveLease]) -> Result<(), M31AError>;
// private
async fn record_release_sqlite(pool: &SqlitePool,
    task_id: TaskId,
    released_at: DateTime<Utc>,) -> Result<(), M3;
```

---

### `src/scheduler/resources/mod.rs` {#src-scheduler-resources-mod-rs}

- **Source Link:** [`src/scheduler/resources/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/scheduler/resources/mod.rs)
- **Lines of Code:** 9 (307 bytes)

#### Primary Responsibility
Hierarchical resource locking and conflict resolution.

---

### `src/scheduler/snapshot.rs` {#src-scheduler-snapshot-rs}

- **Source Link:** [`src/scheduler/snapshot.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/scheduler/snapshot.rs)
- **Lines of Code:** 74 (2460 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (2):** `QueueStatistics`, `SchedulerSnapshot`

#### Key Functions & Signatures (1 shown)
```rust
// private
fn test_scheduler_snapshot_serde_roundtrip();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_scheduler_snapshot_serde_roundtrip`

---
