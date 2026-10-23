# Process Supervision

> **Architectural Layer:** L2 Process  
> **Source Directory:** `src/process`  
> **File Count:** 11 source files  

Process tree supervisor, PID tracking, spool capture, signal escalation, and timeouts.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [admission.rs](#src-process-admission-rs) | 137 | `JobAdmissionController, JobPermit` | Dedicated background job admission controller and concurrency permits ... |
| [confinement.rs](#src-process-confinement-rs) | 193 | `ConfinementHandle, ConfinementManager, ConfinementTier` | Platform-aware process confinement manager (D-07, SEC-03).  Provides d... |
| [env.rs](#src-process-env-rs) | 615 | `EnvironmentBuilder, ProcessSecurityViolation` | Deny-by-default child-process environment builder and sanitizer (CTL-0... |
| [hardened.rs](#src-process-hardened-rs) | 105 | `HardenedSpawn, HardenedSpawnError` | Canonical hardened process-spawn helper.  Single choke point for produ... |
| [identity.rs](#src-process-identity-rs) | 128 | `ProcessIdentity` | Platform-neutral process identity and instance verification (TL-02, JO... |
| [job.rs](#src-process-job-rs) | 1763 | `ActiveJobHandle, BackgroundJobRecord, JobManager` | Asynchronous background job supervisor, durable SQLite job manager, li... |
| [mod.rs](#src-process-mod-rs) | 43 | `Functions/Traits` | Shared supervised process and background job execution subsystem (CTL-... |
| [spool.rs](#src-process-spool-rs) | 430 | `DualBufferOutput, RingBuffer, SpoolPromotionResult` | Dual-buffer job output combining an in-memory ring buffer with append-... |
| [supervisor.rs](#src-process-supervisor-rs) | 279 | `ProcessSupervisor, ProcessError` | Supervised foreground command runner with timeouts and cancellation (T... |
| [tree.rs](#src-process-tree-rs) | 155 | `ProcessTreeController` | Supervised process-tree isolation and two-phase cancellation (TL-02, L... |
| [types.rs](#src-process-types-rs) | 40 | `JobDescriptor, JobOutputChunk, JobStatusInfo` | Process and background job core types (CTL-01, CTL-02). |

---

### `src/process/admission.rs` {#src-process-admission-rs}

- **Source Link:** [`src/process/admission.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/process/admission.rs)
- **Lines of Code:** 137 (4756 bytes)
- **Runtime Properties:** 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Dedicated background job admission controller and concurrency permits (JOB-01, D-15).

#### Types & Trait Declarations
- **Structs (2):** `JobAdmissionController`, `JobPermit`

#### Key Functions & Signatures (5 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn default() -> Self;
// pub
fn new(max_global: usize, max_per_mission: usize) -> Self;
// pub
async fn acquire_permit(&self,
        mission_id: MissionId,
        timeout: Duration,) -> Result<JobPermit, JobError>;
// pub
async fn available_permits(&self, mission_id: MissionId) -> (usize, usize);
```

---

### `src/process/confinement.rs` {#src-process-confinement-rs}

- **Source Link:** [`src/process/confinement.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/process/confinement.rs)
- **Lines of Code:** 193 (6277 bytes)

#### Primary Responsibility
Platform-aware process confinement manager (D-07, SEC-03).  Provides defense-in-depth process execution bounds: - Tier 1: Linux control-group enforcement (`memory.max`, `cpu.max`) - Tier 2: Portable resource budgets enforced via the platform boundary - Tier 3: Isolation-scope leadership and watchdog termination  Tier selection probes through the platform layer so higher layers reason about budgets rather than kernel interfaces.

#### Types & Trait Declarations
- **Structs (2):** `ConfinementHandle`, `ConfinementManager`
- **Enums (1):** `ConfinementTier`

#### Key Functions & Signatures (12 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_tier(tier: ConfinementTier) -> Self;
// pub
fn tier(&self) -> ConfinementTier;
// private
fn probe_host() -> (ConfinementTier, PathBuf);
// pub
fn apply_confinement(&self,
        cmd: &mut Command,
        limits: &ResourceBudget,
        job_id: &JobId,) -> Conf;
// pub
fn tier(&self) -> ConfinementTier;
// pub
fn attach_pid(&self, pid: u32);
// pub
fn cleanup(&mut self);
// private
fn drop(&mut self);
// private
fn test_confinement_tier_detection();
// private
fn test_apply_confinement_configures_command();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_confinement_tier_detection`, `test_apply_confinement_configures_command`

---

### `src/process/env.rs` {#src-process-env-rs}

- **Source Link:** [`src/process/env.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/process/env.rs)
- **Lines of Code:** 615 (21619 bytes)

#### Primary Responsibility
Deny-by-default child-process environment builder and sanitizer (CTL-01, TL-02, per D-15).  Non-negotiable invariants: - Child processes NEVER inherit the host process environment wholesale. - Minimal trusted baseline contains only platform/toolchain essentials. - Dangerous dynamic loader variables (`LD_PRELOAD`, etc.) are stripped. - Host secrets and API credentials (`NVIDIA_API_KEY`, etc.) are strictly excluded. - Working directory is pinned to the authorized task workspace root.

#### Types & Trait Declarations
- **Structs (1):** `EnvironmentBuilder`
- **Enums (1):** `ProcessSecurityViolation`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(workspace_root: impl Into<PathBuf>) -> Self;
// pub
fn new_with_platform(workspace_root: impl Into<PathBuf>, is_windows: bool) -> Self;
// pub
fn workspace_root(&self) -> &Path;
// pub
fn set_var(&mut self,
        key: impl Into<String>,
        value: impl Into<String>,) -> Result<&mut Self, String>;
// pub
fn is_forbidden_key(&self, key: &str) -> bool;
// pub
fn block_key(&mut self, key: impl Into<String>) -> &mut Self;
// pub
fn build_map(&self) -> HashMap<String, String>;
// pub
fn apply(&self, cmd: &mut Command);
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn check_command_safety(program: &str,
    args: &[String],) -> Result<(), ProcessSecurityViolation>;
// pub
fn tokenize_and_validate_shell_string(shell_str: &str) -> Result<(), ProcessSecurityViolation>;
// pub
fn validate_working_directory(working_dir: Option<&Path>,
    workspace_root: &Path,) -> Result<PathBuf, ProcessSecurity;
// private
fn test_environment_builder_rejects_forbidden_secrets_and_loader_vars();
// private
fn test_check_command_safety_posix_and_windows_shell_flags();
// private
fn test_tokenize_and_validate_shell_string();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_environment_builder_rejects_forbidden_secrets_and_loader_vars`, `test_check_command_safety_posix_and_windows_shell_flags`, `test_tokenize_and_validate_shell_string`, `test_environment_builder_windows_baseline_and_dangerous_vars`

---

### `src/process/hardened.rs` {#src-process-hardened-rs}

- **Source Link:** [`src/process/hardened.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/process/hardened.rs)
- **Lines of Code:** 105 (3776 bytes)
- **Runtime Properties:** 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Canonical hardened process-spawn helper.  Single choke point for production process execution outside the capability-provider path:  ```text input → working-directory validation (containment) → command safety validation (protected paths, git redirection) → environment scrubbing (deny-by-default, secrets never inherited) → execution (caller owns timeout / cancellation / sandbox) ```  There is no second process-sandbox implementation: sandbox confinement and resource limits reuse [`crate::sandbox`] and [`EnvironmentBuilder`].

#### Types & Trait Declarations
- **Structs (1):** `HardenedSpawn`
- **Enums (1):** `HardenedSpawnError`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn new(workspace_root: impl Into<PathBuf>) -> Self;
// pub
fn with_env_var(mut self,
        key: impl Into<String>,
        value: impl Into<String>,) -> Result<Self, HardenedSpa;
// pub
fn build_command(&self,
        program: &str,
        args: &[String],
        working_dir: Option<&Path>,) -> Result<t;
// pub
fn workspace_root(&self) -> &Path;
```

---

### `src/process/identity.rs` {#src-process-identity-rs}

- **Source Link:** [`src/process/identity.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/process/identity.rs)
- **Lines of Code:** 128 (4545 bytes)

#### Primary Responsibility
Platform-neutral process identity and instance verification (TL-02, JOB-02).  Provides durable representation for verifying that a process identifier (PID) continues to refer to the exact same process instance across restarts and checkpoints, protecting against OS identifier recycling hazards without embedding Linux-specific kernel structures in generic runtime data models.

#### Types & Trait Declarations
- **Structs (1):** `ProcessIdentity`

#### Key Functions & Signatures (8 shown)
```rust
// private
fn default_platform_name() -> String;
// pub
fn capture(pid: u32) -> Self;
// pub
fn matches(&self, current: &Self) -> bool;
// pub
fn is_live(&self) -> bool;
// pub
fn parse_metadata(json_str: &str) -> Option<Self>;
// pub
fn parse_metadata_with_fallback_pid(json_str: &str, fallback_pid: u32) -> Option<Self>;
// private
fn test_process_identity_roundtrip();
// private
fn test_process_identity_backward_compatibility();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_process_identity_roundtrip`, `test_process_identity_backward_compatibility`

---

### `src/process/job.rs` {#src-process-job-rs}

- **Source Link:** [`src/process/job.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/process/job.rs)
- **Lines of Code:** 1763 (65871 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Asynchronous background job supervisor, durable SQLite job manager, lifecycle management, and crash-safe startup reconciliation (CTL-01, TL-02, JOB-01, JOB-02, per D-13, D-15, D-16, §235).

#### Types & Trait Declarations
- **Structs (5):** `ActiveJobHandle`, `BackgroundJobRecord`, `JobManager`, `JobSupervisor`, `SubmitJobRequest`
- **Enums (2):** `JobError`, `JobState`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn is_terminal(&self) -> bool;
// pub
fn as_str(&self) -> &'static str;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn ownership(&self) -> (MissionId, TaskId, AgentId);
// pub
fn read_linux_process_starttime(pid: u32) -> Option<u64>;
// pub
async fn reconcile_jobs_on_startup(pool: &SqlitePool) -> Result<usize, sqlx::Error>;
// pub
fn new(pool: SqlitePool,
        admission: Arc<JobAdmissionController>,
        artifact_store: Arc<dyn ArtifactStore>,;
// pub
fn with_workspace_root(mut self, root: PathBuf) -> Self;
// pub
fn pool(&self) -> &SqlitePool;
// pub
fn admission(&self) -> &Arc<JobAdmissionController>;
// pub
fn artifact_store(&self) -> &Arc<dyn ArtifactStore>;
// pub
fn spool_dir(&self) -> &PathBuf;
// pub
async fn submit_job(&self, req: SubmitJobRequest) -> Result<JobId, JobError>;
// pub
async fn job_status(&self, job_id: &JobId) -> Result<BackgroundJobRecord, JobError>;
```

---

### `src/process/mod.rs` {#src-process-mod-rs}

- **Source Link:** [`src/process/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/process/mod.rs)
- **Lines of Code:** 43 (1749 bytes)
- **Runtime Properties:** 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Shared supervised process and background job execution subsystem (CTL-01, TL-02, per D-13, D-14, D-15, D-16).  Submodules: - `tree`: Platform-neutral process-group isolation and two-phase cancellation (`ProcessTreeController`). - `supervisor`: Bounded foreground command runner with timeouts and cooperative cancellation (`ProcessSupervisor`). - `job`: Asynchronous background job coordinator with orphan reaping (`JobSupervisor`). - `spool`: Dual-buffer output stream combining live ring buffer with durable disk spool (`DualBufferOutput`). - `env`: Deny-by-default process environment builder and credential isolation (`EnvironmentBuilder`).

---

### `src/process/spool.rs` {#src-process-spool-rs}

- **Source Link:** [`src/process/spool.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/process/spool.rs)
- **Lines of Code:** 430 (14327 bytes)

#### Primary Responsibility
Dual-buffer job output combining an in-memory ring buffer with append-only disk spooling (TL-02, D-16).  Enforces: - In-memory bounded ring buffer (e.g. 1000 lines / 64KB) for low-latency live tail queries. - Append-only disk spool file written incrementally so output is preserved across runtime restarts. - Terminal spool promotion: on completion, disk spool is hashed and promoted to an immutable artifact.

#### Types & Trait Declarations
- **Structs (3):** `DualBufferOutput`, `RingBuffer`, `SpoolPromotionResult`
- **Enums (2):** `SpoolLifecycleState`, `StreamType`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn new(max_lines: usize, max_bytes: usize) -> Self;
// private
fn push_line(&mut self, line: String);
// private
fn get_tail(&self, limit: usize) -> Vec<String>;
// pub
fn strip_ansi(s: &str) -> String;
// pub
fn new(job_id: JobId,
        spool_dir: PathBuf,
        max_ring_lines: usize,
        max_ring_bytes: usize,) -> Resu;
// pub
fn with_max_spool_bytes(self, cap: u64) -> Self;
// pub
fn truncated(&self) -> bool;
// pub
fn append(&self, stream: StreamType, data: &[u8]) -> Result<(), std::io::Error>;
// pub
fn read_chunk(&self, offset: u64, limit: usize) -> Result<JobOutputChunk, std::io::Error>;
// private
fn read_stream_slice(&self,
        path: &PathBuf,
        offset: u64,
        limit: usize,) -> Result<(String, u64, ;
// pub
fn read_tail(&self, stream: StreamType, limit: usize) -> Vec<String>;
// pub
fn stdout_spool_path(&self) -> &PathBuf;
// pub
fn stderr_spool_path(&self) -> &PathBuf;
// pub
async fn promote_to_artifact_store(&self,
        artifact_store: &dyn ArtifactStore,
        _mission_id: MissionId,
  ;
// pub
async fn finalize(&self,
        artifact_store: Option<&Arc<dyn ArtifactStore>>,) -> Result<Option<ArtifactId>, String>;
```

---

### `src/process/supervisor.rs` {#src-process-supervisor-rs}

- **Source Link:** [`src/process/supervisor.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/process/supervisor.rs)
- **Lines of Code:** 279 (10443 bytes)
- **Runtime Properties:** 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Supervised foreground command runner with timeouts and cancellation (TL-02, Law 8, per D-13, D-14).

#### Types & Trait Declarations
- **Structs (1):** `ProcessSupervisor`
- **Enums (1):** `ProcessError`

#### Key Functions & Signatures (7 shown)
```rust
// private
fn default() -> Self;
// pub
fn new(default_timeout: Duration, grace_period: Duration) -> Self;
// pub
async fn run_command(&self,
        program: &str,
        args: &[String],
        cwd: &Path,
        env_builder: Opt;
// pub
async fn run_supervised(&self,
        mut cmd: Command,
        timeout_dur: Duration,
        token: Option<&Cancellat;
// pub
fn execute_direct_argv(program: &str, args: &[String], cwd: &Path) -> Command;
// pub
fn execute_shell_string(shell_str: &str, cwd: &Path) -> Command;
// pub
fn try_execute_shell_string(shell_str: &str,
    cwd: &Path,) -> Result<Command, crate::platform::shell::ShellError>;
```

---

### `src/process/tree.rs` {#src-process-tree-rs}

- **Source Link:** [`src/process/tree.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/process/tree.rs)
- **Lines of Code:** 155 (5983 bytes)
- **Runtime Properties:** 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Supervised process-tree isolation and two-phase cancellation (TL-02, Law 8, per D-14).  Enforces: - Group-scoped isolation so descendant child processes cannot escape. - Two-phase escalation (graceful request, grace period, forceful fallback). - Pre-signal `try_wait()` to prevent identifier-recycling hazards. - Complete descendant reaping to eliminate orphan/zombie processes.  The native mechanism lives in the platform boundary. This controller states the runtime guarantee and delegates enforcement to it.

#### Types & Trait Declarations
- **Structs (1):** `ProcessTreeController`

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn new(pid: u32) -> Self;
// pub
fn with_job(pid: u32, job: Option<Arc<JobHandle>>) -> Self;
// pub
fn pid(&self) -> u32;
// pub
fn job_handle(&self) -> Option<&Arc<JobHandle>>;
// pub
fn configure_command(cmd: &mut Command);
// pub
fn spawn_isolated(cmd: Command) -> Result<(Child, Self), std::io::Error>;
// pub
fn spawn_isolated_with_budget(mut cmd: Command,
        budget: Option<&ResourceBudget>,) -> Result<(Child, Self), std::;
// pub
async fn terminate_supervised(&self,
        child: &mut Child,
        grace_period: Duration,) -> Result<std::process:;
// pub
async fn terminate_by_pid(pid: u32, grace_period: Duration) -> Result<(), std::io::Error>;
// pub
async fn kill_process_group(pid: u32,
        grace_period: Duration,) -> Result<(), std::io::Error>;
```

---

### `src/process/types.rs` {#src-process-types-rs}

- **Source Link:** [`src/process/types.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/process/types.rs)
- **Lines of Code:** 40 (1152 bytes)

#### Primary Responsibility
Process and background job core types (CTL-01, CTL-02).

#### Types & Trait Declarations
- **Structs (4):** `JobDescriptor`, `JobOutputChunk`, `JobStatusInfo`, `ProcessOutput`

---
