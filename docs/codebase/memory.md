# Engineering Memory

> **Architectural Layer:** L3 Intelligence  
> **Source Directory:** `src/memory`  
> **File Count:** 6 source files  

Persistent engineering decisions, architectural assumptions, and historical project memory.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [continuity.rs](#src-memory-continuity-rs) | 237 | `EngineeringContinuityState, SessionContinuityEngine` | Session Continuity Engine.  Reconstructs active engineering state afte... |
| [mod.rs](#src-memory-mod-rs) | 30 | `Functions/Traits` | Long-Horizon Engineering Memory &amp; Project State Continuity.  Subor... |
| [reconciler.rs](#src-memory-reconciler-rs) | 146 | `MemoryReconciler, MemoryReconciliationReport` | Repository-Aware Memory Reconciler.  Subordinates memory claims to rep... |
| [repository.rs](#src-memory-repository-rs) | 1620 | `SqliteEngineeringMemoryRepository` | SQLite repository implementation for Long-Horizon Engineering Memory. ... |
| [retrieval.rs](#src-memory-retrieval-rs) | 233 | `MemoryRetrievalCriteria, TaskAwareMemoryRetriever` | Task-Aware Structured Memory Retrieval.  Provides deterministic releva... |
| [types.rs](#src-memory-types-rs) | 3 | `Functions/Traits` | Re-exports of canonical kernel memory domain types. |

---

### `src/memory/continuity.rs` {#src-memory-continuity-rs}

- **Source Link:** [`src/memory/continuity.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/memory/continuity.rs)
- **Lines of Code:** 237 (8064 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Session Continuity Engine.  Reconstructs active engineering state after process restart, terminal closure, or model session replacement without replaying conversational transcripts.  Restores: - Current mission &amp; plan revision - Task partitions (active, completed, failed) - Open review findings &amp; active assumptions - Authoritative architectural decisions - Latest checkpoint and verification obligations

#### Types & Trait Declarations
- **Structs (2):** `EngineeringContinuityState`, `SessionContinuityEngine`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn format_continuity_briefing(&self) -> String;
// pub
fn new(pool: SqlitePool) -> Self;
// pub
async fn restore_session(&self,
        mission_id: MissionId,) -> Result<EngineeringContinuityState, M31AError>;
```

---

### `src/memory/mod.rs` {#src-memory-mod-rs}

- **Source Link:** [`src/memory/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/memory/mod.rs)
- **Lines of Code:** 30 (1407 bytes)

#### Primary Responsibility
Long-Horizon Engineering Memory &amp; Project State Continuity.  Subordinates memory to runtime state and repository reality. Enforces: - Strict single-crate Rust architecture - Zero second databases, zero second event stores, zero second checkpoint systems - Epistemic assumption lifecycle (Active -&gt; Tested -&gt; Confirmed / Invalidated) - Durable review findings surviving sessions - Durable architectural decisions with supersession - Failure diagnosis and failed repair memory to avoid repeating mutations - Task-aware structured memory retrieval - Repository-aware memory reconciliation against workspace reality - Session continuity across restarts

---

### `src/memory/reconciler.rs` {#src-memory-reconciler-rs}

- **Source Link:** [`src/memory/reconciler.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/memory/reconciler.rs)
- **Lines of Code:** 146 (5490 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Repository-Aware Memory Reconciler.  Subordinates memory claims to repository reality: - Validates file existence and content hashes against actual workspace filesystem. - Marks assumptions invalidated when target files drift or symbols disappear. - Marks verification records stale when verified source files are mutated. - Ensures repository reality ALWAYS wins over stale memory.

#### Types & Trait Declarations
- **Structs (2):** `MemoryReconciler`, `MemoryReconciliationReport`

#### Key Functions & Signatures (2 shown)
```rust
// pub
fn new(store: &'a S, workspace_root: &'a Path) -> Self;
// pub
async fn reconcile_mission(&self,
        mission_id: MissionId,) -> Result<MemoryReconciliationReport, sqlx::Error>;
```

---

### `src/memory/repository.rs` {#src-memory-repository-rs}

- **Source Link:** [`src/memory/repository.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/memory/repository.rs)
- **Lines of Code:** 1620 (63322 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
SQLite repository implementation for Long-Horizon Engineering Memory.  Reuses canonical SqlitePool without introducing any second database or duplicate storage.

#### Types & Trait Declarations
- **Structs (1):** `SqliteEngineeringMemoryRepository`
- **Traits (1):** `EngineeringMemoryStore`

#### Key Functions & Signatures (15 shown)
```rust
// private
async fn save_decision(&self, decision: &EngineeringDecision) -> Result<(), sqlx::Error>;
// private
async fn get_decision(&self, id: &str) -> Result<Option<EngineeringDecision>, sqlx::Error>;
// private
async fn list_decisions(&self,
        scope: Option<MemoryScope>,
        mission_id: Option<MissionId>,
        status;
// private
async fn supersede_decision(&self,
        old_id: &str,
        new_decision: &EngineeringDecision,) -> Result<(), sqlx;
// private
async fn save_assumption(&self, assumption: &EngineeringAssumption) -> Result<(), sqlx::Error>;
// private
async fn get_assumption(&self, id: Uuid) -> Result<Option<EngineeringAssumption>, sqlx::Error>;
// private
async fn update_assumption_status(&self,
        id: Uuid,
        status: AssumptionStatus,
        evidence: Option<&s;
// private
async fn list_assumptions(&self,
        mission_id: MissionId,
        task_id: Option<TaskId>,
        status: Option<;
// private
async fn save_failure_diagnosis(&self,
        diagnosis: &FailureDiagnosisRecord,) -> Result<(), sqlx::Error>;
// private
async fn get_failure_diagnosis(&self,
        id: Uuid,) -> Result<Option<FailureDiagnosisRecord>, sqlx::Error>;
// private
async fn find_diagnosis_by_signature(&self,
        mission_id: MissionId,
        signature: &str,) -> Result<Option<Fa;
// private
async fn update_repair_status(&self, id: Uuid, status: RepairStatus) -> Result<(), sqlx::Error>;
// private
async fn increment_recurrence(&self, id: Uuid) -> Result<(), sqlx::Error>;
// private
async fn list_diagnoses(&self,
        mission_id: MissionId,
        task_id: Option<TaskId>,) -> Result<Vec<FailureDia;
// private
async fn save_review_finding(&self, finding: &ReviewFindingRecord) -> Result<(), sqlx::Error>;
```

---

### `src/memory/retrieval.rs` {#src-memory-retrieval-rs}

- **Source Link:** [`src/memory/retrieval.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/memory/retrieval.rs)
- **Lines of Code:** 233 (8231 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Task-Aware Structured Memory Retrieval.  Provides deterministic relevance filtering for architectural decisions, active assumptions, diagnostic failures, and review findings based on: - Target files &amp; symbols - Requirement keys - Diagnostic error signatures - Mission and task scopes  Excludes unrelated project history from model context.

#### Types & Trait Declarations
- **Structs (2):** `MemoryRetrievalCriteria`, `TaskAwareMemoryRetriever`

#### Key Functions & Signatures (2 shown)
```rust
// pub
fn new(store: &'a S) -> Self;
// pub
async fn retrieve_snapshot(&self,
        criteria: &MemoryRetrievalCriteria<'a>,) -> Result<EngineeringMemorySnapshot, ;
```

---

### `src/memory/types.rs` {#src-memory-types-rs}

- **Source Link:** [`src/memory/types.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/memory/types.rs)
- **Lines of Code:** 3 (91 bytes)

#### Primary Responsibility
Re-exports of canonical kernel memory domain types.

---
