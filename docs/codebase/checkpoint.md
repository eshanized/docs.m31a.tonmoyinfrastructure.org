# Checkpoint & Crash Recovery

> **Architectural Layer:** L6/L7 Checkpoints  
> **Source Directory:** `src/checkpoint`  
> **File Count:** 6 source files  

Two-phase durable checkpoint protocol, manifest hashing, crash recovery scanner, and safe resume.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [crash_recovery.rs](#src-checkpoint-crash_recovery-rs) | 969 | `BackgroundJobsReconciliation, CrashRecoveryResult, ScanSharedContext` | Staged startup crash recovery scanner, process reconciliation &amp; sp... |
| [integrity.rs](#src-checkpoint-integrity-rs) | 213 | `CheckpointIntegrityValidator, CheckpointIntegrityError` | Checkpoint Integrity Validator implementing 5-point verification (CHK-... |
| [manager.rs](#src-checkpoint-manager-rs) | 598 | `CheckpointManager, CheckpointRestoreResult, StagedArtifactInput` | Checkpoint Manager implementing the durable two-phase protocol (CHK-01... |
| [manifest.rs](#src-checkpoint-manifest-rs) | 95 | `CheckpointManifest` | Checkpoint Manifest domain model (CHK-01, D-13).  A CheckpointManifest... |
| [mod.rs](#src-checkpoint-mod-rs) | 25 | `Functions/Traits` | Checkpoint subsystem root module (CHK-01–CHK-05, D-13–D-16).  Enforces... |
| [resume.rs](#src-checkpoint-resume-rs) | 436 | `SafeResumeEngine, SafeResumeReport, SafeResumeError` | Safe resume engine and task completion preservation (CHK-05, D-16).  E... |

---

### `src/checkpoint/crash_recovery.rs` {#src-checkpoint-crash_recovery-rs}

- **Source Link:** [`src/checkpoint/crash_recovery.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/checkpoint/crash_recovery.rs)
- **Lines of Code:** 969 (43961 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Staged startup crash recovery scanner, process reconciliation &amp; spool sealing (CHK-02, CHK-03, D-14, D-15).  Enforces: - Deterministic classification into 4 recovery states: `SafeToResume`, `NeedsRepair`, `Ambiguous`, `Corrupt`. - Fail-closed: `Ambiguous` and `Corrupt` states are NEVER auto-promoted to `SafeToResume` or success. - PID recycling protection: process starttimes from `/proc/&lt;pid&gt;/stat` are verified before sending signals. - Surviving abandoned process groups are terminated via `ProcessTreeController` signal escalation. - Open output spools are sealed with `[INTERRUPTED]` and promoted to `FsArtifactStore`. - Complete scan results are persisted in SQLite prior to resumption.

#### Types & Trait Declarations
- **Structs (4):** `BackgroundJobsReconciliation`, `CrashRecoveryResult`, `ScanSharedContext`, `StartupCrashRecoveryScanner`
- **Enums (2):** `CrashRecoveryClassification`, `CrashRecoveryError`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn is_safe(&self) -> bool;
// pub
fn as_str(&self) -> &'static str;
// pub
fn new(pool: SqlitePool,
        artifact_store: Arc<dyn ArtifactStore>,
        workspace_root: impl AsRef<Path>,) -> S;
// pub
fn integrity_check_count(&self) -> usize;
// private
async fn check_database_integrity_once(&self) -> Option<String>;
// private
async fn capture_shared_baseline_once(&self) -> ScanSharedContext;
// private
async fn prepare_scan_context(&self) -> ScanSharedContext;
// pub
async fn scan_and_reconcile(&self,
        mission_id: MissionId,) -> Result<CrashRecoveryResult, CrashRecoveryError>;
// pub
async fn scan_and_reconcile_cancelled(&self,
        mission_id: MissionId,
        cancel: Option<&tokio_util::sync::Ca;
// private
async fn reconcile_one_with_context(&self,
        mission_id: MissionId,
        ctx: &ScanSharedContext,) -> Result<Cr;
// pub
async fn reconcile_in_flight_tasks(&self,
        mission_id: MissionId,) -> Result<usize, sqlx::Error>;
// private
async fn reconcile_background_jobs(&self,
        mission_id: MissionId,) -> Result<BackgroundJobsReconciliation, sqlx::;
// private
async fn persist_scan_result(&self, result: &CrashRecoveryResult) -> Result<(), sqlx::Error>;
// pub
async fn scan_all_in_flight(&self) -> Result<Vec<CrashRecoveryResult>, CrashRecoveryError>;
// private
async fn reconcile_legacy_missions_once(&self) -> Result<(), CrashRecoveryError>;
```

---

### `src/checkpoint/integrity.rs` {#src-checkpoint-integrity-rs}

- **Source Link:** [`src/checkpoint/integrity.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/checkpoint/integrity.rs)
- **Lines of Code:** 213 (8513 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Checkpoint Integrity Validator implementing 5-point verification (CHK-04).  5-Point Validation Pass: 1. Schema compatibility: verifies manifest schema_version is supported. 2. State integrity: verifies manifest hash matches recomputed canonical hash, and all state components are coherent. 3. Artifact availability: verifies every artifact in artifact_references exists in FsArtifactStore and matches recorded SHA-256 and size. 4. Repository compatibility: verifies snapshot_identity matches expected workspace baseline. 5. Policy compatibility: verifies policy_context_hash matches active policy rules.

#### Types & Trait Declarations
- **Structs (1):** `CheckpointIntegrityValidator`
- **Enums (1):** `CheckpointIntegrityError`

#### Key Functions & Signatures (5 shown)
```rust
// pub
fn new(artifact_store: Arc<dyn ArtifactStore>) -> Self;
// pub
fn with_policy_hash(mut self, hash: impl Into<String>) -> Self;
// pub
fn with_repo_hash(mut self, hash: impl Into<String>) -> Self;
// pub
async fn validate(&self,
        manifest: &CheckpointManifest,) -> Result<(), CheckpointIntegrityError>;
// pub
async fn validate_with_recorded_hash(&self,
        manifest: &CheckpointManifest,
        recorded_manifest_hash: Optio;
```

---

### `src/checkpoint/manager.rs` {#src-checkpoint-manager-rs}

- **Source Link:** [`src/checkpoint/manager.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/checkpoint/manager.rs)
- **Lines of Code:** 598 (23918 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Checkpoint Manager implementing the durable two-phase protocol (CHK-01, D-13).  Durability order (prepare → promote → verify → commit): - Step 1: External Artifact Staging - Write all external verification/evidence artifacts to `staging/&#123;checkpoint_id&#125;/`. - Flush and sync files to disk via `tokio::fs::File::sync_all`. - Compute content-addressed SHA-256 hashes and sizes; validate strictly against manifest. - Step 2: Payload Promotion &amp; Verification - Promote payloads to the authoritative `FsArtifactStore` FIRST, read each payload back, and verify its hash. The checkpoint row is only committed after every payload is provably durable — a checkpoint row therefore never claims payload durability for an absent payload. - Step 3: Atomic SQLite Commit - Begin single SQLite transaction. - Insert checkpoint metadata, manifest JSON, and manifest hash into `checkpoints`. - Insert artifact linkages into `checkpoint_artifacts`. - Insert/update the unified `artifacts` ledger with hash verification (immutability: conflicting content under an existing identity fails). - Commit SQLite transaction. - If a crash occurs between promotion and commit, payloads exist without metadata rows: detectable orphans reclaimed by `gc_orphan_payloads`; restore refuses to run without both halves.

#### Types & Trait Declarations
- **Structs (3):** `CheckpointManager`, `CheckpointRestoreResult`, `StagedArtifactInput`
- **Enums (1):** `CheckpointError`

#### Key Functions & Signatures (12 shown)
```rust
// pub
fn new(artifact_id: ArtifactId,
        data: Vec<u8>,
        extension: impl Into<String>,
        artifact_type: impl;
// pub
fn new(pool: SqlitePool,
        artifact_store: Arc<dyn ArtifactStore>,
        staging_dir: impl AsRef<Path>,) -> Self;
// pub
fn staging_dir(&self) -> &Path;
// pub
async fn create_checkpoint(&self,
        manifest: &CheckpointManifest,
        artifacts: Vec<StagedArtifactInput>,) -;
// private
async fn promote_payload(&self, artifact: &StagedArtifactInput) -> Result<(), CheckpointError>;
// pub
async fn gc_orphan_payloads(&self) -> Result<usize, CheckpointError>;
// pub
async fn clean_orphaned_staging(&self) -> Result<usize, CheckpointError>;
// pub
async fn restore_checkpoint(&self,
        checkpoint_id: CheckpointId,
        target_workspace: &Path,) -> Result<Chec;
// pub
async fn get_latest_checkpoint_info(pool: &SqlitePool,
        mission_id: crate::ids::MissionId,) -> Result<Option<(i64;
// pub
async fn get_checkpoint_manifest(pool: &SqlitePool,
        checkpoint_id: CheckpointId,) -> Result<Option<(i64, Checkpo;
// pub
async fn checkpoint_exists(pool: &SqlitePool,
        checkpoint_id: CheckpointId,) -> Result<bool, sqlx::Error>;
// pub
async fn list_checkpoint_ids(pool: &SqlitePool,
        mission_id: Option<crate::ids::MissionId>,) -> Result<Vec<Checkp;
```

---

### `src/checkpoint/manifest.rs` {#src-checkpoint-manifest-rs}

- **Source Link:** [`src/checkpoint/manifest.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/checkpoint/manifest.rs)
- **Lines of Code:** 95 (3521 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Checkpoint Manifest domain model (CHK-01, D-13).  A CheckpointManifest represents a coherent durable boundary capturing all 9 specification-mandated state components bound by a content-addressed SHA-256 hash: 1. Mission state &amp; identity 2. Task states (Map of TaskId -&gt; TaskState) 3. Agent metadata &amp; context 4. Background job states (Map of JobId -&gt; state) 5. Policy context hash 6. Verification check IDs 7. External artifact references (ArtifactId, SHA-256, byte size) 8. Repository snapshot identity (RepositoryBaseline SHA-256) 9. Scheduler watermark &amp; cycle sequence

#### Types & Trait Declarations
- **Structs (1):** `CheckpointManifest`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn new(checkpoint_id: CheckpointId,
        mission_id: MissionId,
        sequence: u64,
        stage: impl Into<Strin;
// pub
fn compute_manifest_hash(&self) -> String;
// pub
fn is_schema_supported(&self) -> bool;
```

---

### `src/checkpoint/mod.rs` {#src-checkpoint-mod-rs}

- **Source Link:** [`src/checkpoint/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/checkpoint/mod.rs)
- **Lines of Code:** 25 (1049 bytes)

#### Primary Responsibility
Checkpoint subsystem root module (CHK-01–CHK-05, D-13–D-16).  Enforces: - Strict two-phase checkpoint commit (staging -&gt; sync -&gt; validation -&gt; atomic SQLite commit) - CheckpointManifest domain model binding all 9 state components with SHA-256 hash - 5-point CheckpointIntegrityValidator - Staged StartupCrashRecoveryScanner with POSIX process group cleanup &amp; spool sealing - SafeResumeEngine preserving completed work while invalidating drifted tasks

---

### `src/checkpoint/resume.rs` {#src-checkpoint-resume-rs}

- **Source Link:** [`src/checkpoint/resume.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/checkpoint/resume.rs)
- **Lines of Code:** 436 (19104 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Safe resume engine and task completion preservation (CHK-05, D-16).  Enforces: - Preservation of completed tasks (`TaskState::Succeeded`) whose repository files and verified artifacts match the checkpoint baseline. - Targeted invalidation of only drifted, missing-artifact, or broken tasks to `TaskState::Pending`. - Rescheduling of in-flight (`TaskState::Running`) tasks to `TaskState::Pending` for clean dispatch. - Avoids blind full-graph re-executions.

#### Types & Trait Declarations
- **Structs (2):** `SafeResumeEngine`, `SafeResumeReport`
- **Enums (1):** `SafeResumeError`

#### Key Functions & Signatures (5 shown)
```rust
// pub
fn new(pool: SqlitePool,
        artifact_store: Arc<dyn ArtifactStore>,
        workspace_root: impl AsRef<Path>,) -> S;
// pub
fn with_task_output_file(mut self, task_id: TaskId, path: impl Into<String>) -> Self;
// pub
fn associate_task_output_file(&mut self, task_id: TaskId, path: impl Into<String>);
// pub
async fn hydrate_task_output_files(&mut self,
        mission_id: MissionId,) -> Result<(), SafeResumeError>;
// pub
async fn resume_mission(&self,
        mission_id: MissionId,
        manifest: &CheckpointManifest,) -> Result<SafeResu;
```

---
