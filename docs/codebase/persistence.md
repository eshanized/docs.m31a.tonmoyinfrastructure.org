# Persistence & SQLite

> **Architectural Layer:** L0 Persistence  
> **Source Directory:** `src/persistence`  
> **File Count:** 26 source files  

SQLite database pool, schema migrations 001-032, repositories, and artifact store.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [fs_store.rs](#src-persistence-artifacts-fs_store-rs) | 355 | `FsArtifactStore, EvidenceClassification` | Filesystem artifact store implementation  Per PST-03, filesystem stora... |
| [mod.rs](#src-persistence-artifacts-mod-rs) | 15 | `Functions/Traits` | Artifact storage module  Per PST-03, filesystem/object storage stores ... |
| [quota.rs](#src-persistence-artifacts-quota-rs) | 237 | `QuotaEnforcer, StreamingQuotaWriter, ArtifactExemption` | Streaming Artifact Quota Enforcer &amp; Protection (BST-01, D-08).  En... |
| [service.rs](#src-persistence-artifacts-service-rs) | 1168 | `ArtifactProvenance, ArtifactRecord, ArtifactService` | Canonical Artifact Lifecycle and Provenance Authority (ART-01, ART-02,... |
| [mod.rs](#src-persistence-mod-rs) | 18 | `Functions/Traits` | Persistence module - SQLite, streams, and artifact storage  Per D-17, ... |
| [paths.rs](#src-persistence-paths-rs) | 83 | `Functions/Traits` | Platform-aware path resolution.  Canonical authority: [`crate::storage... |
| [mod.rs](#src-persistence-sqlite-mod-rs) | 15 | `Functions/Traits` | SQLite persistence module  Per D-03, sqlx for SQLite (async, compile-t... |
| [pool.rs](#src-persistence-sqlite-pool-rs) | 67 | `Functions/Traits` | SQLite connection pool setup  Per D-03, sqlx for SQLite with compile-t... |
| [agent.rs](#src-persistence-sqlite-repositories-agent-rs) | 236 | `SqliteAgentRepository` | SQLite concrete implementation of AgentRepository (AGT-05, PST-01). |
| [agent_handoff.rs](#src-persistence-sqlite-repositories-agent_handoff-rs) | 240 | `SqliteAgentHandoffRepository` | SQLite concrete implementation of AgentHandoffRepository (AGT-06, D-14... |
| [event.rs](#src-persistence-sqlite-repositories-event-rs) | 275 | `SqliteEventRepository` | SQLite concrete implementation of EventRepository (D-10, D-11, D-16, E... |
| [execution_run.rs](#src-persistence-sqlite-repositories-execution_run-rs) | 497 | `SqliteExecutionRunRepository` | SQLite concrete implementation of ExecutionRunRepository. |
| [lifecycle.rs](#src-persistence-sqlite-repositories-lifecycle-rs) | 1162 | `PersistedLifecycleState, PersistedQuestionRecord, ResumeAuthExpectations` | SQLite persistence repository for human-governed lifecycle state.  Sto... |
| [mission.rs](#src-persistence-sqlite-repositories-mission-rs) | 563 | `SqliteMissionRepository` | SQLite concrete implementation of MissionRepository (D-01, D-15, PST-0... |
| [mod.rs](#src-persistence-sqlite-repositories-mod-rs) | 477 | `MockAgentRepository, MockEventRepository, MockMissionRepository` | Repository trait definitions and concrete SQLite implementations.  Per... |
| [report.rs](#src-persistence-sqlite-repositories-report-rs) | 180 | `CompletionReportMetadata, SqliteReportRepository` | SQLite repository for Completion Reports metadata (RPT-01, D-13). |
| [row.rs](#src-persistence-sqlite-repositories-row-rs) | 105 | `EncodedAggregateFields` | Shared decoding for SQLite rows representing lifecycle aggregates. |
| [session.rs](#src-persistence-sqlite-repositories-session-rs) | 261 | `SqliteSessionRepository` | SQLite concrete implementation of SessionRepository (MSN-05, PST-01). |
| [system_state.rs](#src-persistence-sqlite-repositories-system_state-rs) | 167 | `SqliteSystemStateRepository` | SQLite implementation of SystemStateRepository (SYS-01, D-22). |
| [task.rs](#src-persistence-sqlite-repositories-task-rs) | 923 | `SqliteTaskRepository` | SQLite implementation of TaskRepository (PST-01, D-13, DAG-05). |
| [task_graph.rs](#src-persistence-sqlite-repositories-task_graph-rs) | 604 | `SqliteTaskGraphRepository` | SQLite implementation of TaskGraphRepository (D-13, DAG-01, DAG-05). |
| [telemetry.rs](#src-persistence-sqlite-repositories-telemetry-rs) | 279 | `SqliteTelemetryRepository` | SQLite repository for Telemetry Spans and Metric Samples (OBS-01, D-01... |
| [schema.rs](#src-persistence-sqlite-schema-rs) | 243 | `Functions/Traits` | Schema definitions and migration runner  Uses sqlx::migrate! macro to ... |
| [transaction.rs](#src-persistence-sqlite-transaction-rs) | 529 | `SqliteTransactionManager, TaskExecutionTelemetry, EventLogSchema` | Transactional persistence boundaries for atomic aggregate and event co... |
| [file_stream.rs](#src-persistence-streams-file_stream-rs) | 200 | `FileStream` | Append-only file stream implementation  Per PST-02, append-only storag... |
| [mod.rs](#src-persistence-streams-mod-rs) | 7 | `Functions/Traits` | Stream storage module  Per PST-02, append-only files store high-volume... |

---

### `src/persistence/artifacts/fs_store.rs` {#src-persistence-artifacts-fs_store-rs}

- **Source Link:** [`src/persistence/artifacts/fs_store.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/artifacts/fs_store.rs)
- **Lines of Code:** 355 (12284 bytes)

#### Primary Responsibility
Filesystem artifact store implementation  Per PST-03, filesystem storage for large blobs (logs, reports, patches) outside relational rows. Artifact IDs are UUIDs, not user-provided strings.

#### Types & Trait Declarations
- **Structs (1):** `FsArtifactStore`
- **Enums (1):** `EvidenceClassification`
- **Traits (1):** `ArtifactStore`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
async fn store(&self,
        artifact_id: ArtifactId,
        data: &[u8],
        extension: &str,) -> Result<PathBuf,;
// private
async fn store_classified(&self,
        artifact_id: ArtifactId,
        data: &[u8],
        extension: &str,
        ;
// private
async fn record_classification(&self,
        _artifact_id: ArtifactId,
        _extension: &str,
        _classificatio;
// private
async fn retrieve(&self,
        artifact_id: ArtifactId,
        extension: &str,) -> Result<Vec<u8>, M31AError>;
// private
fn path_for(&self, artifact_id: ArtifactId, extension: &str) -> PathBuf;
// private
async fn exists(&self, artifact_id: ArtifactId, extension: &str) -> bool;
// private
fn store_base_dir(&self) -> Option<PathBuf>;
// pub
fn new(base_dir: impl AsRef<Path>) -> Self;
// pub
fn base_dir(&self) -> &Path;
// private
fn artifact_path(&self, artifact_id: ArtifactId, extension: &str) -> PathBuf;
// private
async fn ensure_dir(&self) -> Result<(), M31AError>;
// private
async fn store(&self,
        artifact_id: ArtifactId,
        data: &[u8],
        extension: &str,) -> Result<PathBuf,;
// private
async fn retrieve(&self,
        artifact_id: ArtifactId,
        extension: &str,) -> Result<Vec<u8>, M31AError>;
// private
fn path_for(&self, artifact_id: ArtifactId, extension: &str) -> PathBuf;
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_fs_artifact_store_store_and_retrieve`, `test_fs_artifact_store_path_for`, `test_fs_artifact_store_binary_data`, `test_fs_artifact_store_multiple_artifacts`, `test_fs_artifact_store_extension_sanitization`, `test_fs_artifact_store_retrieve_nonexistent`

---

### `src/persistence/artifacts/mod.rs` {#src-persistence-artifacts-mod-rs}

- **Source Link:** [`src/persistence/artifacts/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/artifacts/mod.rs)
- **Lines of Code:** 15 (556 bytes)

#### Primary Responsibility
Artifact storage module  Per PST-03, filesystem/object storage stores large logs, reports, patches, test output, screenshots, and generated artifacts.

---

### `src/persistence/artifacts/quota.rs` {#src-persistence-artifacts-quota-rs}

- **Source Link:** [`src/persistence/artifacts/quota.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/artifacts/quota.rs)
- **Lines of Code:** 237 (7763 bytes)

#### Primary Responsibility
Streaming Artifact Quota Enforcer &amp; Protection (BST-01, D-08).  Enforces byte-level limits on single artifact sizes and cumulative mission storage with strict exemption for verification, audit, checkpoint, and completion artifacts.

#### Types & Trait Declarations
- **Structs (2):** `QuotaEnforcer`, `StreamingQuotaWriter`
- **Enums (2):** `ArtifactExemption`, `QuotaError`

#### Key Functions & Signatures (12 shown)
```rust
// pub
fn new(inner: W,
        max_artifact_bytes: Option<u64>,
        max_mission_bytes: Option<u64>,
        cumulative_cou;
// pub
fn bytes_written(&self) -> u64;
// private
fn poll_write(mut self: Pin<&mut Self>,
        cx: &mut Context<'_>,
        buf: &[u8],) -> Poll<io::Result<usize>>;
// private
fn poll_flush(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<io::Result<()>>;
// private
fn poll_shutdown(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<io::Result<()>>;
// pub
fn new(max_artifact_bytes: Option<u64>, max_mission_bytes: Option<u64>) -> Self;
// pub
fn current_cumulative_bytes(&self) -> u64;
// pub
fn can_evict(&self, exemption: ArtifactExemption) -> bool;
// pub
fn check_bytes(&self, size: u64, exemption: ArtifactExemption) -> Result<(), QuotaError>;
// pub
fn wrap_writer(&self,
        inner: W,
        exemption: ArtifactExemption,) -> StreamingQuotaWriter<W>;
// private
async fn test_streaming_quota_writer_enforces_limit();
// private
async fn test_protected_artifacts_exempt_from_quota();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_streaming_quota_writer_enforces_limit`, `test_protected_artifacts_exempt_from_quota`

---

### `src/persistence/artifacts/service.rs` {#src-persistence-artifacts-service-rs}

- **Source Link:** [`src/persistence/artifacts/service.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/artifacts/service.rs)
- **Lines of Code:** 1168 (39975 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Canonical Artifact Lifecycle and Provenance Authority (ART-01, ART-02, D-13).  Provides ONE canonical authority for the artifact lifecycle across: produce -&gt; identify/hash -&gt; store -&gt; register -&gt; provenance -&gt; validate -&gt; project -&gt; consume.  Storage vs Authority Distinction: - Domain Aggregate: `ArtifactRecord`, `ArtifactProvenance`, `ArtifactStatus` - Physical Payload Storage: `FsArtifactStore` (`.m31a/artifacts/&#123;artifact_id&#125;.&#123;extension&#125;`) - Metadata &amp; Provenance Ledger: SQLite (`artifacts`, `workflow_artifacts`, `checkpoint_artifacts`) - Projections: Derived human-readable files (`.m31a/project/*.md`, `REPORT.md`), never operational state.

#### Types & Trait Declarations
- **Structs (4):** `ArtifactProvenance`, `ArtifactRecord`, `ArtifactService`, `IntegrityCheckResult`
- **Enums (2):** `ArtifactError`, `ArtifactStatus`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn compute_artifact_hash(data: &[u8]) -> String;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn new() -> Self;
// pub
fn for_workflow_step(workflow_run_id: WorkflowRunId,
        step_run_id: WorkflowStepRunId,
        producer_role: impl;
// pub
fn for_task(mission_id: MissionId,
        task_id: TaskId,
        producer_role: impl Into<String>,) -> Self;
// pub
fn for_mission(mission_id: MissionId) -> Self;
// pub
fn with_parent(mut self, parent_id: ArtifactId) -> Self;
// pub
fn with_check(mut self, check_id: CheckId) -> Self;
// pub
fn with_prompt(mut self, prompt_id: impl Into<String>, version: u32) -> Self;
// pub
fn with_model(mut self, model: impl Into<String>) -> Self;
// pub
fn with_quarantine_reason(mut self, reason: impl Into<String>) -> Self;
// pub
fn new(store: Arc<dyn ArtifactStore>, pool: SqlitePool) -> Self;
// pub
fn store(&self) -> &Arc<dyn ArtifactStore>;
// pub
fn pool(&self) -> &SqlitePool;
```

---

### `src/persistence/mod.rs` {#src-persistence-mod-rs}

- **Source Link:** [`src/persistence/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/mod.rs)
- **Lines of Code:** 18 (743 bytes)

#### Primary Responsibility
Persistence module - SQLite, streams, and artifact storage  Per D-17, persistence/ owns the sqlx/SQLite implementation and transactional storage. Per D-19, no generic platform/ module — platform-specific abstractions introduced at subsystem boundaries when required (paths.rs lives in persistence/).

---

### `src/persistence/paths.rs` {#src-persistence-paths-rs}

- **Source Link:** [`src/persistence/paths.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/paths.rs)
- **Lines of Code:** 83 (3142 bytes)

#### Primary Responsibility
Platform-aware path resolution.  Canonical authority: [`crate::storage::StorageLayout`]. This module retains its public functions for compatibility and delegates to the single canonical authority (`deployment::DeploymentPaths` / `storage`).

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn global_data_dir() -> Option<PathBuf>;
// pub
fn global_config_dir() -> Option<PathBuf>;
// pub
fn global_data_dir_for_channel(channel: crate::deployment::DeploymentChannel,) -> Option<PathBuf>;
// pub
fn global_config_dir_for_channel(channel: crate::deployment::DeploymentChannel,) -> Option<PathBuf>;
// pub
fn project_local_dir(workspace_root: &std::path::Path) -> PathBuf;
// pub
fn project_db_path(workspace_root: &std::path::Path,
    channel: crate::deployment::DeploymentChannel,) -> PathBuf;
// pub
fn canonical_db_path_for_workspace(workspace_root: &std::path::Path) -> PathBuf;
// private
fn test_project_local_dir();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_project_local_dir`

---

### `src/persistence/sqlite/mod.rs` {#src-persistence-sqlite-mod-rs}

- **Source Link:** [`src/persistence/sqlite/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/mod.rs)
- **Lines of Code:** 15 (449 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
SQLite persistence module  Per D-03, sqlx for SQLite (async, compile-time checked queries, migration support). Per D-17, persistence/ owns the sqlx/SQLite implementation.

---

### `src/persistence/sqlite/pool.rs` {#src-persistence-sqlite-pool-rs}

- **Source Link:** [`src/persistence/sqlite/pool.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/pool.rs)
- **Lines of Code:** 67 (2287 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
SQLite connection pool setup  Per D-03, sqlx for SQLite with compile-time checked queries and migration support. Per RESEARCH.md Pitfall 3, set appropriate busy_timeout for concurrent access.

#### Key Functions & Signatures (2 shown)
```rust
// pub
async fn create_pool(db_path: &Path) -> Result<SqlitePool, sqlx::Error>;
// private
async fn test_create_pool();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_create_pool`

---

### `src/persistence/sqlite/repositories/agent.rs` {#src-persistence-sqlite-repositories-agent-rs}

- **Source Link:** [`src/persistence/sqlite/repositories/agent.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/repositories/agent.rs)
- **Lines of Code:** 236 (8079 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
SQLite concrete implementation of AgentRepository (AGT-05, PST-01).

#### Types & Trait Declarations
- **Structs (1):** `SqliteAgentRepository`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn new(pool: SqlitePool) -> Self;
// pub
async fn insert(&self, agent: &Agent) -> Result<(), M31AError>;
// pub
async fn get(&self, id: AgentId) -> Result<Option<Agent>, M31AError>;
// private
async fn insert(&self, agent: &Agent) -> Result<(), M31AError>;
// private
async fn get(&self, id: AgentId) -> Result<Option<Agent>, M31AError>;
// private
async fn update_status(&self, id: AgentId, status: AgentState) -> Result<(), M31AError>;
// private
async fn list_by_mission(&self, mission_id: MissionId) -> Result<Vec<Agent>, M31AError>;
// private
fn map_row_to_agent(row: SqliteRow) -> Result<Agent, M31AError>;
```

---

### `src/persistence/sqlite/repositories/agent_handoff.rs` {#src-persistence-sqlite-repositories-agent_handoff-rs}

- **Source Link:** [`src/persistence/sqlite/repositories/agent_handoff.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/repositories/agent_handoff.rs)
- **Lines of Code:** 240 (9250 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
SQLite concrete implementation of AgentHandoffRepository (AGT-06, D-14).

#### Types & Trait Declarations
- **Structs (1):** `SqliteAgentHandoffRepository`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn new(pool: SqlitePool) -> Self;
// pub
async fn insert_handoff(&self, record: &HandoffRecord) -> Result<(), HandoffError>;
// pub
async fn find_by_mission(&self,
        mission_id: MissionId,) -> Result<Vec<HandoffRecord>, HandoffError>;
// pub
async fn find_by_task(&self, task_id: TaskId) -> Result<Vec<HandoffRecord>, HandoffError>;
// private
async fn insert_handoff(&self, record: &HandoffRecord) -> Result<(), HandoffError>;
// private
async fn find_by_mission(&self,
        mission_id: MissionId,) -> Result<Vec<HandoffRecord>, HandoffError>;
// private
async fn find_by_task(&self, task_id: TaskId) -> Result<Vec<HandoffRecord>, HandoffError>;
// private
fn map_row_to_handoff(row: SqliteRow) -> Result<HandoffRecord, HandoffError>;
```

---

### `src/persistence/sqlite/repositories/event.rs` {#src-persistence-sqlite-repositories-event-rs}

- **Source Link:** [`src/persistence/sqlite/repositories/event.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/repositories/event.rs)
- **Lines of Code:** 275 (9867 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
SQLite concrete implementation of EventRepository (D-10, D-11, D-16, EVT-02, EVT-03).

#### Types & Trait Declarations
- **Structs (1):** `SqliteEventRepository`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn new(pool: SqlitePool) -> Self;
// pub
async fn next_sequence(&self, mission_id: Option<MissionId>) -> Result<u64, M31AError>;
// pub
async fn list_since_sequence(&self,
        mission_id: MissionId,
        since: u64,) -> Result<Vec<EventEnvelope>, M3;
// private
async fn append(&self, envelope: &EventEnvelope) -> Result<(), M31AError>;
// private
async fn list_by_mission(&self,
        mission_id: MissionId,) -> Result<Vec<EventEnvelope>, M31AError>;
// private
async fn latest_sequence(&self, mission_id: Option<MissionId>) -> Result<u64, M31AError>;
// private
fn map_row_to_envelope(row: SqliteRow) -> Result<EventEnvelope, M31AError>;
// private
async fn test_sqlite_event_repository_sequence_ordering();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_sqlite_event_repository_sequence_ordering`

---

### `src/persistence/sqlite/repositories/execution_run.rs` {#src-persistence-sqlite-repositories-execution_run-rs}

- **Source Link:** [`src/persistence/sqlite/repositories/execution_run.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/repositories/execution_run.rs)
- **Lines of Code:** 497 (18136 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
SQLite concrete implementation of ExecutionRunRepository.

#### Types & Trait Declarations
- **Structs (1):** `SqliteExecutionRunRepository`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(pool: SqlitePool) -> Self;
// pub
async fn update_watermark(&self,
        id: ExecutionRunId,
        sequence: u64,) -> Result<(), M31AError>;
// pub
async fn get_by_parent(&self,
        parent_id: ExecutionRunId,) -> Result<Vec<ExecutionRun>, M31AError>;
// pub
async fn get(&self, id: ExecutionRunId) -> Result<Option<ExecutionRun>, M31AError>;
// pub
async fn insert(&self, run: &ExecutionRun) -> Result<(), M31AError>;
// pub
async fn update_status(&self,
        id: ExecutionRunId,
        status: ExecutionRunState,) -> Result<(), M31AError>;
// pub
async fn list_all(&self) -> Result<Vec<ExecutionRun>, M31AError>;
// private
async fn insert(&self, run: &ExecutionRun) -> Result<(), M31AError>;
// private
async fn get(&self, id: ExecutionRunId) -> Result<Option<ExecutionRun>, M31AError>;
// private
async fn update_status(&self,
        id: ExecutionRunId,
        status: ExecutionRunState,) -> Result<(), M31AError>;
// private
async fn list_all(&self) -> Result<Vec<ExecutionRun>, M31AError>;
// private
async fn update_watermark(&self, id: ExecutionRunId, sequence: u64) -> Result<(), M31AError>;
// private
fn map_row_to_execution_run(row: SqliteRow) -> Result<ExecutionRun, M31AError>;
// private
async fn setup_db() -> SqlitePool;
// private
async fn test_execution_run_crud();
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_execution_run_crud`, `corrupt_persisted_mode_and_timestamps_fail_closed`, `test_f06_terminal_resurrection_rejected`, `test_f06_invalid_forward_leaps_rejected`, `test_f06_valid_lifecycle_progression`

---

### `src/persistence/sqlite/repositories/lifecycle.rs` {#src-persistence-sqlite-repositories-lifecycle-rs}

- **Source Link:** [`src/persistence/sqlite/repositories/lifecycle.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/repositories/lifecycle.rs)
- **Lines of Code:** 1162 (46377 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
SQLite persistence repository for human-governed lifecycle state.  Stores and loads: - `session_lifecycle_state`: current stage, plan revision, task revision, authorization pointer - `plan_revisions`: versioned plan proposals, author attribution, status - `task_revisions`: versioned candidate task graphs, plan revision bindings - `discovery_questions`: dynamic questions, status, user answers - `execution_authorizations`: explicit operator authorizations, invalidation tracking

#### Types & Trait Declarations
- **Structs (4):** `PersistedLifecycleState`, `PersistedQuestionRecord`, `ResumeAuthExpectations`, `SqliteLifecycleRepository`
- **Enums (3):** `ResumeAuthError`, `ResumeAuthVerdict`, `ValidatedTransitionError`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(pool: SqlitePool) -> Self;
// private
fn session_bytes(session_str: &str) -> Vec<u8>;
// pub
async fn save_validated_transition(&self,
        session_id: &str,
        expected_current: LifecycleStage,
        ev;
// pub
async fn save_lifecycle_state(&self,
        state: &PersistedLifecycleState,) -> Result<(), sqlx::Error>;
// pub
async fn load_lifecycle_state(&self,
        session_id: &str,) -> Result<Option<PersistedLifecycleState>, sqlx::Error>;
// pub
async fn save_plan_revision(&self, revision: &PlanRevision) -> Result<(), sqlx::Error>;
// pub
async fn load_plan_revisions(&self,
        session_id: &str,) -> Result<Vec<PlanRevision>, sqlx::Error>;
// pub
async fn load_latest_plan_revision(&self,
        session_id: &str,) -> Result<Option<PlanRevision>, sqlx::Error>;
// pub
async fn load_plan_revision(&self,
        session_id: &str,
        revision: u32,) -> Result<Option<PlanRevision>, sql;
// private
async fn update_revision_status_for_table(&self,
        is_plan: bool,
        session_id: &str,
        revision: u32,;
// pub
async fn update_plan_revision_status(&self,
        session_id: &str,
        revision: u32,
        status: PlanReviewS;
// pub
async fn save_task_revision(&self, revision: &TaskRevision) -> Result<(), sqlx::Error>;
// pub
async fn load_task_revisions(&self,
        session_id: &str,) -> Result<Vec<TaskRevision>, sqlx::Error>;
// pub
async fn load_latest_task_revision(&self,
        session_id: &str,) -> Result<Option<TaskRevision>, sqlx::Error>;
// pub
async fn load_task_revision(&self,
        session_id: &str,
        revision: u32,) -> Result<Option<TaskRevision>, sql;
```

---

### `src/persistence/sqlite/repositories/mission.rs` {#src-persistence-sqlite-repositories-mission-rs}

- **Source Link:** [`src/persistence/sqlite/repositories/mission.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/repositories/mission.rs)
- **Lines of Code:** 563 (21750 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
SQLite concrete implementation of MissionRepository (D-01, D-15, PST-01).

#### Types & Trait Declarations
- **Structs (1):** `SqliteMissionRepository`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(pool: SqlitePool) -> Self;
// pub
async fn update_watermark(&self, id: MissionId, sequence: u64) -> Result<(), M31AError>;
// pub
async fn get_by_parent(&self, parent_id: MissionId) -> Result<Vec<Mission>, M31AError>;
// pub
async fn get(&self, id: MissionId) -> Result<Option<Mission>, M31AError>;
// pub
async fn insert(&self, mission: &Mission) -> Result<(), M31AError>;
// pub
async fn update_status(&self,
        id: MissionId,
        status: MissionState,) -> Result<(), M31AError>;
// pub
async fn list_all(&self) -> Result<Vec<Mission>, M31AError>;
// private
async fn insert(&self, mission: &Mission) -> Result<(), M31AError>;
// private
async fn get(&self, id: MissionId) -> Result<Option<Mission>, M31AError>;
// private
async fn update_status(&self, id: MissionId, status: MissionState) -> Result<(), M31AError>;
// private
async fn list_all(&self) -> Result<Vec<Mission>, M31AError>;
// private
async fn update_watermark(&self, id: MissionId, sequence: u64) -> Result<(), M31AError>;
// private
fn map_row_to_mission(row: SqliteRow) -> Result<Mission, M31AError>;
// pub
fn map_legacy_status_to_canonical(status: &str) -> Result<&'static str, M31AError>;
// pub
async fn ensure_canonical_row_for_legacy(pool: &SqlitePool,
    id: MissionId,) -> Result<bool, M31AError>;
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_sqlite_mission_repository_crud`, `test_sqlite_mission_repository_fork_queries`

---

### `src/persistence/sqlite/repositories/mod.rs` {#src-persistence-sqlite-repositories-mod-rs}

- **Source Link:** [`src/persistence/sqlite/repositories/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/repositories/mod.rs)
- **Lines of Code:** 477 (16495 bytes)

#### Primary Responsibility
Repository trait definitions and concrete SQLite implementations.  Per D-17, persistence behind explicit contracts. Per D-22, repository implementations must ensure exactly one authoritative state per mission.

#### Types & Trait Declarations
- **Structs (5):** `MockAgentRepository`, `MockEventRepository`, `MockMissionRepository`, `MockSessionRepository`, `MockTaskRepository`
- **Traits (7):** `AgentRepository`, `EventRepository`, `ExecutionRunRepository`, `MissionRepository`, `SessionRepository`, `TaskGraphRepository`, `TaskRepository`

#### Key Functions & Signatures (15 shown)
```rust
// private
async fn insert(&self, run: &ExecutionRun) -> Result<(), M31AError>;
// private
async fn get(&self, id: ExecutionRunId) -> Result<Option<ExecutionRun>, M31AError>;
// private
async fn update_status(&self,
        id: ExecutionRunId,
        status: ExecutionRunState,) -> Result<(), M31AError>;
// private
async fn list_all(&self) -> Result<Vec<ExecutionRun>, M31AError>;
// private
async fn update_watermark(&self, id: ExecutionRunId, sequence: u64) -> Result<(), M31AError>;
// private
async fn insert(&self, mission: &Mission) -> Result<(), M31AError>;
// private
async fn get(&self, id: MissionId) -> Result<Option<Mission>, M31AError>;
// private
async fn update_status(&self, id: MissionId, status: MissionState) -> Result<(), M31AError>;
// private
async fn list_all(&self) -> Result<Vec<Mission>, M31AError>;
// private
async fn update_watermark(&self, id: MissionId, sequence: u64) -> Result<(), M31AError>;
// private
async fn insert(&self, session: &Session) -> Result<(), M31AError>;
// private
async fn get(&self, id: SessionId) -> Result<Option<Session>, M31AError>;
// private
async fn list_by_mission(&self, mission_id: MissionId) -> Result<Vec<Session>, M31AError>;
// private
async fn list_by_run(&self, run_id: ExecutionRunId) -> Result<Vec<Session>, M31AError>;
// private
async fn close(&self, id: SessionId) -> Result<(), M31AError>;
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_traits_compile_and_can_be_mocked`

---

### `src/persistence/sqlite/repositories/report.rs` {#src-persistence-sqlite-repositories-report-rs}

- **Source Link:** [`src/persistence/sqlite/repositories/report.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/repositories/report.rs)
- **Lines of Code:** 180 (6686 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
SQLite repository for Completion Reports metadata (RPT-01, D-13).

#### Types & Trait Declarations
- **Structs (2):** `CompletionReportMetadata`, `SqliteReportRepository`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn new(pool: SqlitePool) -> Self;
// pub
async fn record_report(&self,
        report: &CompletionReport,
        md_artifact_id: &ArtifactId,
        json_artif;
// pub
async fn get_report_metadata(&self,
        mission_id: &MissionId,) -> Result<Option<CompletionReportMetadata>, M31AErr;
```

---

### `src/persistence/sqlite/repositories/row.rs` {#src-persistence-sqlite-repositories-row-rs}

- **Source Link:** [`src/persistence/sqlite/repositories/row.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/repositories/row.rs)
- **Lines of Code:** 105 (3703 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
Shared decoding for SQLite rows representing lifecycle aggregates.

#### Types & Trait Declarations
- **Structs (1):** `EncodedAggregateFields`

#### Key Functions & Signatures (7 shown)
```rust
// pub(crate)
fn encode_aggregate_fields(policy_context: &PolicyContext,
    constraints: &[String],
    requirements: &[String],
    ;
// pub(crate)
fn decode_json_column(row: &SqliteRow,
    column: &str,
    aggregate: &str,) -> Result<T, M31AError>;
// pub(crate)
fn decode_autonomy_mode(row: &SqliteRow,
    aggregate: &str,) -> Result<AutonomyMode, M31AError>;
// pub(crate)
fn decode_aggregate_status(row: &SqliteRow,
    aggregate: &str,) -> Result<ExecutionRunState, M31AError>;
// pub(crate)
fn decode_required_timestamp(row: &SqliteRow,
    column: &str,
    aggregate: &str,) -> Result<DateTime<Utc>, M31AError;
// pub(crate)
fn decode_optional_timestamp(row: &SqliteRow,
    column: &str,
    aggregate: &str,) -> Result<Option<DateTime<Utc>>, M;
// private
fn parse_timestamp(raw: &str, column: &str, aggregate: &str) -> Result<DateTime<Utc>, M31AError>;
```

---

### `src/persistence/sqlite/repositories/session.rs` {#src-persistence-sqlite-repositories-session-rs}

- **Source Link:** [`src/persistence/sqlite/repositories/session.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/repositories/session.rs)
- **Lines of Code:** 261 (9746 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
SQLite concrete implementation of SessionRepository (MSN-05, PST-01).

#### Types & Trait Declarations
- **Structs (1):** `SqliteSessionRepository`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn new(pool: SqlitePool) -> Self;
// private
async fn insert(&self, session: &Session) -> Result<(), M31AError>;
// private
async fn get(&self, id: SessionId) -> Result<Option<Session>, M31AError>;
// private
async fn list_by_mission(&self, mission_id: MissionId) -> Result<Vec<Session>, M31AError>;
// private
async fn list_by_run(&self, run_id: ExecutionRunId) -> Result<Vec<Session>, M31AError>;
// private
async fn close(&self, id: SessionId) -> Result<(), M31AError>;
// private
fn map_row_to_session(row: SqliteRow) -> Result<Session, M31AError>;
// private
async fn test_sqlite_session_repository_lifecycle();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_sqlite_session_repository_lifecycle`

---

### `src/persistence/sqlite/repositories/system_state.rs` {#src-persistence-sqlite-repositories-system_state-rs}

- **Source Link:** [`src/persistence/sqlite/repositories/system_state.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/repositories/system_state.rs)
- **Lines of Code:** 167 (5261 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
SQLite implementation of SystemStateRepository (SYS-01, D-22).

#### Types & Trait Declarations
- **Structs (1):** `SqliteSystemStateRepository`
- **Traits (1):** `SystemStateRepository`

#### Key Functions & Signatures (15 shown)
```rust
// private
async fn get(&self, key: &str) -> Result<Option<String>, M31AError>;
// private
async fn set(&self, key: &str, value: &str) -> Result<(), M31AError>;
// private
async fn delete(&self, key: &str) -> Result<(), M31AError>;
// private
async fn list_all(&self) -> Result<Vec<(String, String)>, M31AError>;
// pub
fn new(pool: SqlitePool) -> Self;
// pub
fn pool(&self) -> &SqlitePool;
// pub
async fn record_onboarding(&self,
        sentinel_json: &str,
        init_state_str: &str,) -> Result<(), M31AError>;
// pub
async fn get(&self, key: &str) -> Result<Option<String>, M31AError>;
// pub
async fn set(&self, key: &str, value: &str) -> Result<(), M31AError>;
// pub
async fn delete(&self, key: &str) -> Result<(), M31AError>;
// pub
async fn list_all(&self) -> Result<Vec<(String, String)>, M31AError>;
// private
async fn get(&self, key: &str) -> Result<Option<String>, M31AError>;
// private
async fn set(&self, key: &str, value: &str) -> Result<(), M31AError>;
// private
async fn delete(&self, key: &str) -> Result<(), M31AError>;
// private
async fn list_all(&self) -> Result<Vec<(String, String)>, M31AError>;
```

---

### `src/persistence/sqlite/repositories/task.rs` {#src-persistence-sqlite-repositories-task-rs}

- **Source Link:** [`src/persistence/sqlite/repositories/task.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/repositories/task.rs)
- **Lines of Code:** 923 (33653 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
SQLite implementation of TaskRepository (PST-01, D-13, DAG-05).

#### Types & Trait Declarations
- **Structs (1):** `SqliteTaskRepository`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(pool: SqlitePool) -> Self;
// pub
fn pool(&self) -> &SqlitePool;
// pub
async fn insert(&self, task: &Task) -> Result<(), M31AError>;
// pub
async fn get(&self, id: TaskId) -> Result<Option<Task>, M31AError>;
// pub
async fn update_status(&self, id: TaskId, status: TaskState) -> Result<(), M31AError>;
// pub
async fn list_by_mission(&self, mission_id: MissionId) -> Result<Vec<Task>, M31AError>;
// pub
async fn count_by_mission(&self, mission_id: MissionId) -> Result<usize, M31AError>;
// pub
async fn count_completed_by_mission(&self,
        mission_id: MissionId,) -> Result<usize, M31AError>;
// pub
async fn get_task_states_by_mission(&self,
        mission_id: MissionId,) -> Result<BTreeMap<TaskId, TaskState>, M31AEr;
// pub
async fn update_max_retries_by_candidate_key(&self,
        mission_id: MissionId,
        candidate_key: &str,
        ;
// pub
async fn list_candidate_summaries_by_mission(&self,
        mission_id: MissionId,) -> Result<Vec<(String, String, i64)>;
// pub
async fn mark_succeeded(&self,
        id: TaskId,
        result: Option<&TaskResult>,) -> Result<(), M31AError>;
// pub
async fn mark_ready(&self, id: TaskId) -> Result<(), M31AError>;
// pub
async fn mark_retry(&self, id: TaskId, retry_count: u32) -> Result<(), M31AError>;
// pub
async fn mark_failed(&self,
        id: TaskId,
        completed_at: DateTime<Utc>,) -> Result<(), M31AError>;
```

---

### `src/persistence/sqlite/repositories/task_graph.rs` {#src-persistence-sqlite-repositories-task_graph-rs}

- **Source Link:** [`src/persistence/sqlite/repositories/task_graph.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/repositories/task_graph.rs)
- **Lines of Code:** 604 (22746 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
SQLite implementation of TaskGraphRepository (D-13, DAG-01, DAG-05).

#### Types & Trait Declarations
- **Structs (1):** `SqliteTaskGraphRepository`

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn new(pool: SqlitePool) -> Self;
// private
async fn get_active_graph(&self,
        mission_id: MissionId,) -> Result<Option<TaskGraph>, M31AError>;
// private
async fn get_graph_by_id(&self, graph_id: TaskGraphId) -> Result<Option<TaskGraph>, M31AError>;
// private
async fn update_task_status(&self,
        task_id: TaskId,
        status: TaskState,) -> Result<(), M31AError>;
// private
async fn update_task_result(&self,
        task_id: TaskId,
        status: &str,
        result_json: Option<&str>,) ->;
// pub
async fn find_latest_active_graph(&self) -> Result<Option<TaskGraph>, M31AError>;
// pub
async fn find_latest_active_graph_for_workspace(&self,
        workspace_root: &std::path::Path,) -> Result<Option<TaskG;
// private
async fn load_tasks_for_graph(&self,
        graph_id: TaskGraphId,) -> Result<BTreeMap<TaskId, Task>, M31AError>;
// private
async fn load_edges_for_graph(&self,
        graph_id: TaskGraphId,) -> Result<BTreeSet<DependencyEdge>, M31AError>;
// pub(crate)
fn map_row_to_task(row: SqliteRow) -> Result<Task, M31AError>;
```

---

### `src/persistence/sqlite/repositories/telemetry.rs` {#src-persistence-sqlite-repositories-telemetry-rs}

- **Source Link:** [`src/persistence/sqlite/repositories/telemetry.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/repositories/telemetry.rs)
- **Lines of Code:** 279 (10103 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
SQLite repository for Telemetry Spans and Metric Samples (OBS-01, D-01).

#### Types & Trait Declarations
- **Structs (1):** `SqliteTelemetryRepository`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn new(pool: SqlitePool) -> Self;
// pub
async fn record_span(&self, span: &TelemetrySpan) -> Result<(), M31AError>;
// pub
async fn record_metric_sample(&self, sample: &MetricSample) -> Result<(), M31AError>;
// pub
async fn get_spans_for_mission(&self,
        mission_id: &MissionId,) -> Result<Vec<TelemetrySpan>, M31AError>;
// pub
async fn get_metrics_for_mission(&self,
        mission_id: &MissionId,) -> Result<Vec<MetricSample>, M31AError>;
// pub
async fn get_summary(&self, mission_id: &MissionId) -> Result<TelemetrySummary, M31AError>;
```

---

### `src/persistence/sqlite/schema.rs` {#src-persistence-sqlite-schema-rs}

- **Source Link:** [`src/persistence/sqlite/schema.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/schema.rs)
- **Lines of Code:** 243 (8890 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
Schema definitions and migration runner  Uses sqlx::migrate! macro to load and run migrations from ./migrations directory. Per RESEARCH.md Pattern 4, migrations are versioned and explicit.

#### Key Functions & Signatures (4 shown)
```rust
// pub
async fn run_migrations(pool: &SqlitePool) -> Result<(), sqlx::Error>;
// pub
async fn initialize_database(db_path: &Path) -> Result<SqlitePool, sqlx::Error>;
// private
async fn test_initialize_database_creates_tables();
// private
async fn test_run_migrations_idempotent();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_initialize_database_creates_tables`, `test_run_migrations_idempotent`

---

### `src/persistence/sqlite/transaction.rs` {#src-persistence-sqlite-transaction-rs}

- **Source Link:** [`src/persistence/sqlite/transaction.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/sqlite/transaction.rs)
- **Lines of Code:** 529 (20992 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Transactional persistence boundaries for atomic aggregate and event commits (PST-06, D-10, D-11).

#### Types & Trait Declarations
- **Structs (2):** `SqliteTransactionManager`, `TaskExecutionTelemetry`
- **Enums (1):** `EventLogSchema`

#### Key Functions & Signatures (10 shown)
```rust
// private
async fn append_event_log(tx: &mut sqlx::Transaction<'_, sqlx::Sqlite>,
    envelope: &EventEnvelope,
    schema: EventL;
// pub
fn new(pool: SqlitePool) -> Self;
// pub
fn pool(&self) -> &SqlitePool;
// pub
async fn commit_execution_run_with_event(&self,
        run: &ExecutionRun,
        envelope: &EventEnvelope,) -> Result;
// pub
async fn commit_mission_with_event(&self,
        mission: &Mission,
        envelope: &EventEnvelope,) -> Result<(), M3;
// pub
async fn begin(&self) -> Result<sqlx::Transaction<'_, sqlx::Sqlite>, M31AError>;
// pub
async fn commit_task_execution_side_effects(&self,
        mission_id: MissionId,
        task_id: TaskId,
        agent;
// private
async fn test_commit_mission_with_event_atomic_success();
// private
async fn test_commit_execution_run_event_persists_both_scope_ids();
// private
async fn test_commit_mission_with_event_rollback_on_failure();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_commit_mission_with_event_atomic_success`, `test_commit_execution_run_event_persists_both_scope_ids`, `test_commit_mission_with_event_rollback_on_failure`

---

### `src/persistence/streams/file_stream.rs` {#src-persistence-streams-file_stream-rs}

- **Source Link:** [`src/persistence/streams/file_stream.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/streams/file_stream.rs)
- **Lines of Code:** 200 (6953 bytes)

#### Primary Responsibility
Append-only file stream implementation  Per PST-02, append-only storage for high-volume event/transcript data without relational overhead. Each stream is a file with newline-delimited entries.

#### Types & Trait Declarations
- **Structs (1):** `FileStream`
- **Traits (1):** `StreamStore`

#### Key Functions & Signatures (12 shown)
```rust
// private
async fn append(&self, stream_name: &str, data: &[u8]) -> Result<(), M31AError>;
// private
async fn read_all(&self, stream_name: &str) -> Result<Vec<Vec<u8>>, M31AError>;
// pub
fn new(base_dir: impl AsRef<Path>) -> Self;
// private
fn stream_path(&self, stream_name: &str) -> PathBuf;
// private
async fn ensure_dir(&self) -> Result<(), M31AError>;
// private
async fn append(&self, stream_name: &str, data: &[u8]) -> Result<(), M31AError>;
// private
async fn read_all(&self, stream_name: &str) -> Result<Vec<Vec<u8>>, M31AError>;
// private
async fn test_file_stream_append_and_read();
// private
async fn test_file_stream_empty_stream();
// private
async fn test_file_stream_multiple_streams();
// private
async fn test_file_stream_path_sanitization();
// private
async fn test_file_stream_binary_data();
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_file_stream_append_and_read`, `test_file_stream_empty_stream`, `test_file_stream_multiple_streams`, `test_file_stream_path_sanitization`, `test_file_stream_binary_data`

---

### `src/persistence/streams/mod.rs` {#src-persistence-streams-mod-rs}

- **Source Link:** [`src/persistence/streams/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/persistence/streams/mod.rs)
- **Lines of Code:** 7 (187 bytes)

#### Primary Responsibility
Stream storage module  Per PST-02, append-only files store high-volume session/event/transcript streams.

---
