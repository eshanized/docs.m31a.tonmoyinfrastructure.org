# Capability Registry & Providers

> **Architectural Layer:** L2 Capabilities  
> **Source Directory:** `src/capability`  
> **File Count:** 38 source files  

Typed capabilities, health monitoring, provider implementations (fs, git, lsp, terminal, web, etc.).

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [error.rs](#src-capability-error-rs) | 80 | `CapabilityError` | Capability errors and failure classification (D-02, CTL-01). |
| [family.rs](#src-capability-family-rs) | 135 | `CapabilityFamily` | Core capability families enum (CTL-01, D-01). |
| [health.rs](#src-capability-health-rs) | 283 | `CapabilityHealthTracker, HealthConfig, HealthTransitionRecord` | Capability health state machine and transition tracker (CTL-03, D-02). |
| [instance.rs](#src-capability-instance-rs) | 63 | `CapabilityInstance` | Capability instance metadata and descriptor (CTL-03). |
| [mod.rs](#src-capability-mod-rs) | 25 | `Functions/Traits` | Capabilities and tool execution runtime subsystem.  Owns the 15 core c... |
| [permissions.rs](#src-capability-permissions-rs) | 300 | `CapabilityPermissions, CapabilityOperation` | Strongly typed capability permissions and resource scoping (CTL-03, D-... |
| [cli_git.rs](#src-capability-providers-cli_git-rs) | 494 | `CliGitProvider, DisabledGitProvider` | CLI-based Git capability provider running host git (CTL-02, D-01, D-03... |
| [event_bus.rs](#src-capability-providers-event_bus-rs) | 70 | `EventBusProvider` | Telemetry and events capability provider wrapping EventBus (CTL-02, D-... |
| [fs_artifacts.rs](#src-capability-providers-fs_artifacts-rs) | 130 | `FsArtifactStoreProvider` | Artifact store capability provider wrapping FsArtifactStore (CTL-02, D... |
| [local_fs.rs](#src-capability-providers-local_fs-rs) | 705 | `LocalFileSystemProvider` | Local filesystem capability provider with strict workspace path contai... |
| [local_lsp.rs](#src-capability-providers-local_lsp-rs) | 514 | `LocalLspProcessClient, PersistentLspSession, LspOutgoingMessage` | local lsp persistent stdio process provider. |
| [local_memory.rs](#src-capability-providers-local_memory-rs) | 83 | `LocalMemoryProvider, MemoryEntry` | Local in-memory contextual memory capability provider (CTL-02, D-01, D... |
| [local_network.rs](#src-capability-providers-local_network-rs) | 58 | `LocalNetworkProvider` | Network capability provider for connectivity check and DNS lookup (CTL... |
| [local_process.rs](#src-capability-providers-local_process-rs) | 400 | `LocalJobProvider, LocalProcessProvider` | Local process, shell, and background job capability providers (CTL-01,... |
| [local_sandbox.rs](#src-capability-providers-local_sandbox-rs) | 120 | `LocalSandboxProvider` | Subsystem component |
| [local_terminal.rs](#src-capability-providers-local_terminal-rs) | 385 | `LocalTerminalProvider, TerminalSessionHandle` | Local terminal session capability provider (CTL-02, D-01, D-03). |
| [local_verification.rs](#src-capability-providers-local_verification-rs) | 131 | `LocalVerificationProvider` | Local verification and QA capability provider (CTL-02, D-01, D-03).  V... |
| [local_web.rs](#src-capability-providers-local_web-rs) | 325 | `LocalWebProvider` | Web capability provider backed by reqwest (CTL-02, D-01, D-03). |
| [mod.rs](#src-capability-providers-mod-rs) | 31 | `Functions/Traits` | Native local capability providers (CTL-02, D-01, D-03). |
| [model_caller.rs](#src-capability-providers-model_caller-rs) | 72 | `ModelCallerProvider` | Model capability provider wrapping ModelCaller (CTL-02, D-01, D-03). |
| [repo_graph.rs](#src-capability-providers-repo_graph-rs) | 147 | `RepositoryGraphProvider` | Repository graph capability provider wrapping BoundedQueryEngine (CTL-... |
| [registry.rs](#src-capability-registry-rs) | 608 | `CapabilityRegistry` | Central capability registry (CTL-01, CTL-02, CTL-03). |
| [artifacts.rs](#src-capability-traits-artifacts-rs) | 24 | `Functions/Traits` | Immutable artifact storage service trait (CTL-01, CTL-02). |
| [fs.rs](#src-capability-traits-fs-rs) | 64 | `FileMetadata` | File system capability service trait (CTL-01, CTL-02). |
| [git.rs](#src-capability-traits-git-rs) | 122 | `GitBranchInfo, GitCommitInfo, GitStatusResult` | Git version control service trait (CTL-01, CTL-02). |
| [jobs.rs](#src-capability-traits-jobs-rs) | 54 | `Functions/Traits` | Background jobs supervision service trait (CTL-01, CTL-02). |
| [memory.rs](#src-capability-traits-memory-rs) | 19 | `Functions/Traits` | Contextual memory service trait (CTL-01, CTL-02). |
| [mod.rs](#src-capability-traits-mod-rs) | 35 | `Functions/Traits` | The 15 core capability service traits (CTL-01, CTL-02). |
| [model.rs](#src-capability-traits-model-rs) | 32 | `ModelInvocationRequest, ModelInvocationResponse` | Model inference service trait (CTL-01, CTL-02). |
| [network.rs](#src-capability-traits-network-rs) | 14 | `Functions/Traits` | Network connectivity and resolution service trait (CTL-01, CTL-02). |
| [process.rs](#src-capability-traits-process-rs) | 23 | `Functions/Traits` | Supervised process execution service trait (CTL-01, CTL-02). |
| [repo.rs](#src-capability-traits-repo-rs) | 44 | `CodeSearchResult` | Repository graph and code navigation service trait (CTL-01, CTL-02). |
| [sandbox.rs](#src-capability-traits-sandbox-rs) | 55 | `SandboxConfig, SandboxHandle` | Sandbox boundary and environment service trait (CTL-01, CTL-02). |
| [shell.rs](#src-capability-traits-shell-rs) | 26 | `ShellOutput` | Bounded shell execution service trait (CTL-01, CTL-02). |
| [telemetry.rs](#src-capability-traits-telemetry-rs) | 24 | `Functions/Traits` | Telemetry and metrics recording service trait (CTL-01, CTL-02). |
| [terminal.rs](#src-capability-traits-terminal-rs) | 106 | `TerminalSessionConfig, TerminalSessionStatus` | Terminal session service trait (CTL-01, CTL-02). |
| [verification.rs](#src-capability-traits-verification-rs) | 43 | `VerificationReport, VerificationTarget, VerificationKind` | Verification and QA service trait (CTL-01, CTL-02). |
| [web.rs](#src-capability-traits-web-rs) | 41 | `WebFetchResult, WebSearchResult` | Web access and external search service trait (CTL-01, CTL-02). |

---

### `src/capability/error.rs` {#src-capability-error-rs}

- **Source Link:** [`src/capability/error.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/error.rs)
- **Lines of Code:** 80 (2461 bytes)

#### Primary Responsibility
Capability errors and failure classification (D-02, CTL-01).

#### Types & Trait Declarations
- **Enums (1):** `CapabilityError`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn is_infrastructure(&self) -> bool;
// pub
fn is_semantic(&self) -> bool;
// private
fn from(err: std::io::Error) -> Self;
```

---

### `src/capability/family.rs` {#src-capability-family-rs}

- **Source Link:** [`src/capability/family.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/family.rs)
- **Lines of Code:** 135 (4221 bytes)

#### Primary Responsibility
Core capability families enum (CTL-01, D-01).

#### Types & Trait Declarations
- **Enums (1):** `CapabilityFamily`

#### Key Functions & Signatures (4 shown)
```rust
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn test_all_15_families_present();
// private
fn test_family_round_trip();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_all_15_families_present`, `test_family_round_trip`

---

### `src/capability/health.rs` {#src-capability-health-rs}

- **Source Link:** [`src/capability/health.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/health.rs)
- **Lines of Code:** 283 (10574 bytes)

#### Primary Responsibility
Capability health state machine and transition tracker (CTL-03, D-02).

#### Types & Trait Declarations
- **Structs (3):** `CapabilityHealthTracker`, `HealthConfig`, `HealthTransitionRecord`
- **Enums (1):** `CapabilityHealthState`

#### Key Functions & Signatures (13 shown)
```rust
// pub
fn is_admissible(&self) -> bool;
// pub
fn is_healthy(&self) -> bool;
// private
fn default() -> Self;
// pub
fn new(config: HealthConfig) -> Self;
// pub
fn with_initial_state(config: HealthConfig, state: CapabilityHealthState) -> Self;
// pub
fn current_state(&mut self) -> CapabilityHealthState;
// pub
fn peek_state(&self) -> CapabilityHealthState;
// pub
fn record_success(&mut self);
// pub
fn record_failure(&mut self, is_infrastructure_fault: bool, reason: impl Into<String>);
// private
fn transition_to(&mut self, new_state: CapabilityHealthState, reason: String);
// pub
fn history(&self) -> &[HealthTransitionRecord];
// private
fn test_health_state_transitions();
// private
fn test_half_open_failure_returns_to_unavailable();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_health_state_transitions`, `test_half_open_failure_returns_to_unavailable`

---

### `src/capability/instance.rs` {#src-capability-instance-rs}

- **Source Link:** [`src/capability/instance.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/instance.rs)
- **Lines of Code:** 63 (2178 bytes)

#### Primary Responsibility
Capability instance metadata and descriptor (CTL-03).

#### Types & Trait Declarations
- **Structs (1):** `CapabilityInstance`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn new(id: impl Into<String>,
        name: impl Into<String>,
        version: impl Into<String>,
        family: Capab;
// pub
fn with_metadata(mut self, key: impl Into<String>, value: impl Into<String>) -> Self;
// pub
fn with_health(mut self, health: CapabilityHealthState) -> Self;
```

---

### `src/capability/mod.rs` {#src-capability-mod-rs}

- **Source Link:** [`src/capability/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/mod.rs)
- **Lines of Code:** 25 (808 bytes)

#### Primary Responsibility
Capabilities and tool execution runtime subsystem.  Owns the 15 core capability family definitions, capability instance descriptors, operational health tracking, strongly typed permissions, and central registry (CTL-01, CTL-02, CTL-03).  Core principle: The model proposes. The runtime decides.

---

### `src/capability/permissions.rs` {#src-capability-permissions-rs}

- **Source Link:** [`src/capability/permissions.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/permissions.rs)
- **Lines of Code:** 300 (10464 bytes)

#### Primary Responsibility
Strongly typed capability permissions and resource scoping (CTL-03, D-04).

#### Types & Trait Declarations
- **Structs (1):** `CapabilityPermissions`
- **Enums (1):** `CapabilityOperation`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn new(operations: impl IntoIterator<Item = CapabilityOperation>) -> Self;
// pub
fn with_path_scope(mut self, path: impl Into<PathBuf>) -> Self;
// pub
fn with_domains(mut self, domains: Vec<String>) -> Self;
// pub
fn with_max_risk(mut self, risk: RiskClass) -> Self;
// pub
fn read_only() -> Self;
// pub
fn full_access() -> Self;
// pub
fn permits_operation(&self, op: CapabilityOperation) -> bool;
// pub
fn permits_path(&self, target_path: &Path) -> bool;
// pub
fn permits_domain(&self, domain: &str) -> bool;
// pub
fn permits_risk(&self, risk: RiskClass) -> bool;
// pub
fn validate(&self,
        op: CapabilityOperation,
        path: Option<&Path>,
        domain: Option<&str>,
        r;
// pub
fn intersect(&self, other: &CapabilityPermissions) -> CapabilityPermissions;
// private
fn test_permissions_operation_check();
// private
fn test_permissions_path_validation();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_permissions_operation_check`, `test_permissions_path_validation`, `test_permissions_intersection`

---

### `src/capability/providers/cli_git.rs` {#src-capability-providers-cli_git-rs}

- **Source Link:** [`src/capability/providers/cli_git.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/providers/cli_git.rs)
- **Lines of Code:** 494 (17254 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
CLI-based Git capability provider running host git (CTL-02, D-01, D-03).

#### Types & Trait Declarations
- **Structs (2):** `CliGitProvider`, `DisabledGitProvider`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(workspace_root: impl Into<PathBuf>) -> Self;
// private
async fn run_git(&self, args: &[&str]) -> Result<String, CapabilityError>;
// private
async fn status(&self) -> Result<GitStatusResult, CapabilityError>;
// private
async fn diff(&self, staged: bool) -> Result<String, CapabilityError>;
// private
async fn log(&self, max_count: usize) -> Result<Vec<GitCommitInfo>, CapabilityError>;
// private
async fn show(&self, revision: &str) -> Result<String, CapabilityError>;
// private
async fn branch(&self) -> Result<GitBranchInfo, CapabilityError>;
// private
async fn checkout(&self,
        branch_or_commit: &str,
        gate: &GitGate,) -> Result<(), CapabilityError>;
// private
async fn add(&self, paths: &[PathBuf], gate: &GitGate) -> Result<(), CapabilityError>;
// private
async fn commit(&self, message: &str, gate: &GitGate) -> Result<String, CapabilityError>;
// private
async fn add_all(&self, gate: &GitGate) -> Result<(), CapabilityError>;
// private
async fn reset(&self, paths: &[&str], gate: &GitGate) -> Result<(), CapabilityError>;
// private
async fn commit_with_trailers(&self,
        message: &str,
        trailers: &crate::git::trailers::CommitTrailers,
   ;
// private
async fn merge(&self,
        branch: &str,
        no_edit: bool,
        gate: &GitGate,) -> Result<String, Capability;
// private
async fn merge_abort(&self, gate: &GitGate) -> Result<(), CapabilityError>;
```

---

### `src/capability/providers/event_bus.rs` {#src-capability-providers-event_bus-rs}

- **Source Link:** [`src/capability/providers/event_bus.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/providers/event_bus.rs)
- **Lines of Code:** 70 (1790 bytes)

#### Primary Responsibility
Telemetry and events capability provider wrapping EventBus (CTL-02, D-01, D-03).

#### Types & Trait Declarations
- **Structs (1):** `EventBusProvider`

#### Key Functions & Signatures (6 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_bus(bus: Arc<dyn EventBus>) -> Self;
// pub
fn bus(&self) -> Option<&Arc<dyn EventBus>>;
// private
async fn record_event(&self,
        event_name: &str,
        attributes: HashMap<String, String>,) -> Result<(), Capab;
// private
async fn record_metric(&self,
        metric_name: &str,
        value: f64,
        unit: &str,) -> Result<(), Capabili;
```

---

### `src/capability/providers/fs_artifacts.rs` {#src-capability-providers-fs_artifacts-rs}

- **Source Link:** [`src/capability/providers/fs_artifacts.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/providers/fs_artifacts.rs)
- **Lines of Code:** 130 (4212 bytes)

#### Primary Responsibility
Artifact store capability provider wrapping FsArtifactStore (CTL-02, D-01, D-03).

#### Types & Trait Declarations
- **Structs (1):** `FsArtifactStoreProvider`

#### Key Functions & Signatures (7 shown)
```rust
// pub
fn new(base_dir: impl AsRef<Path>) -> Self;
// pub
fn from_arc(store: Arc<dyn ArtifactStore>) -> Self;
// pub
fn from_service(service: Arc<ArtifactService>) -> Self;
// pub
fn with_service(mut self, service: Arc<ArtifactService>) -> Self;
// private
async fn store_artifact(&self,
        artifact_id: &str,
        data: &[u8],
        extension: &str,) -> Result<PathB;
// private
async fn load_artifact(&self,
        artifact_id: &str,
        extension: &str,) -> Result<Vec<u8>, CapabilityError>;
// private
async fn test_artifact_provider();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_artifact_provider`

---

### `src/capability/providers/local_fs.rs` {#src-capability-providers-local_fs-rs}

- **Source Link:** [`src/capability/providers/local_fs.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/providers/local_fs.rs)
- **Lines of Code:** 705 (27396 bytes)

#### Primary Responsibility
Local filesystem capability provider with strict workspace path containment (CTL-02, D-01, D-03).

#### Types & Trait Declarations
- **Structs (1):** `LocalFileSystemProvider`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(workspace_root: impl Into<PathBuf>) -> Result<Self, CapabilityError>;
// pub
fn workspace_root(&self) -> &Path;
// pub
fn resolve_and_verify(&self, path: &Path) -> Result<PathBuf, CapabilityError>;
// private
fn reject_final_symlink_for_mutation(workspace_root: &Path,
    user_path: &Path,
    op: &str,) -> Result<PathBuf, Capa;
// private
fn verify_open_fd(fd: std::os::unix::io::RawFd,
    workspace_root: &Path,
    user_path: &Path,
    op: &str,) -> Resul;
// pub
fn strip_verbatim_prefix(path: &Path) -> PathBuf;
// private
fn normalize_path(path: &Path) -> PathBuf;
// private
async fn read_file(&self,
        path: &Path,
        offset: Option<u64>,
        limit: Option<usize>,) -> Result<Vec;
// private
async fn write_file(&self, path: &Path, content: &[u8]) -> Result<usize, CapabilityError>;
// private
async fn edit_file(&self,
        path: &Path,
        old_content: &str,
        new_content: &str,) -> Result<(), Capa;
// private
async fn list_files(&self,
        path: &Path,
        recursive: bool,) -> Result<Vec<PathBuf>, CapabilityError>;
// private
async fn file_metadata(&self, path: &Path) -> Result<FileMetadata, CapabilityError>;
// private
async fn delete_file(&self, path: &Path) -> Result<(), CapabilityError>;
// private
async fn create_directory(&self, path: &Path) -> Result<(), CapabilityError>;
// private
async fn move_file(&self, src: &Path, dst: &Path) -> Result<(), CapabilityError>;
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_workspace_containment`, `test_fs_operations`

---

### `src/capability/providers/local_lsp.rs` {#src-capability-providers-local_lsp-rs}

- **Source Link:** [`src/capability/providers/local_lsp.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/providers/local_lsp.rs)
- **Lines of Code:** 514 (17838 bytes)

#### Primary Responsibility
local lsp persistent stdio process provider.

#### Types & Trait Declarations
- **Structs (2):** `LocalLspProcessClient`, `PersistentLspSession`
- **Enums (2):** `LspOutgoingMessage`, `LspSessionState`

#### Key Functions & Signatures (13 shown)
```rust
// pub
async fn start(workspace_root: &Path,
        cmd_bin: &str,
        cmd_args: &[&str],) -> Result<Self, String>;
// pub
fn workspace_root(&self) -> &Path;
// pub
fn cmd_bin(&self) -> &str;
// pub
fn cmd_args(&self) -> &[String];
// pub
async fn is_alive(&self) -> bool;
// pub
async fn state(&self) -> LspSessionState;
// pub
async fn query(&self,
        method: &str,
        params: serde_json::Value,
        timeout: Duration,) -> Result<ser;
// pub
async fn did_open(&self,
        file_path: &Path,
        content: &str,
        language_id: &str,) -> Result<(), Stri;
// pub
async fn did_change(&self, file_path: &Path, content: &str) -> Result<(), String>;
// pub
async fn did_close(&self, file_path: &Path) -> Result<(), String>;
// pub
async fn shutdown(&self) -> Result<(), String>;
// pub
async fn open_documents(&self) -> HashMap<String, i32>;
// pub
async fn query_stdio(workspace_root: &Path,
        cmd_bin: &str,
        cmd_args: &[&str],
        method: &str,
    ;
```

---

### `src/capability/providers/local_memory.rs` {#src-capability-providers-local_memory-rs}

- **Source Link:** [`src/capability/providers/local_memory.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/providers/local_memory.rs)
- **Lines of Code:** 83 (2229 bytes)

#### Primary Responsibility
Local in-memory contextual memory capability provider (CTL-02, D-01, D-03).

#### Types & Trait Declarations
- **Structs (2):** `LocalMemoryProvider`, `MemoryEntry`

#### Key Functions & Signatures (5 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// private
async fn store_memory(&self,
        key: &str,
        value: &str,
        ttl_secs: Option<u64>,) -> Result<(), Capab;
// private
async fn recall_memory(&self, key: &str) -> Result<Option<String>, CapabilityError>;
// private
async fn test_local_memory_provider();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_local_memory_provider`

---

### `src/capability/providers/local_network.rs` {#src-capability-providers-local_network-rs}

- **Source Link:** [`src/capability/providers/local_network.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/providers/local_network.rs)
- **Lines of Code:** 58 (2020 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Network capability provider for connectivity check and DNS lookup (CTL-02, D-01, D-03).

#### Types & Trait Declarations
- **Structs (1):** `LocalNetworkProvider`

#### Key Functions & Signatures (4 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// private
async fn check_connectivity(&self, host: &str, port: u16) -> Result<bool, CapabilityError>;
// private
async fn resolve_host(&self, host: &str) -> Result<Vec<String>, CapabilityError>;
```

---

### `src/capability/providers/local_process.rs` {#src-capability-providers-local_process-rs}

- **Source Link:** [`src/capability/providers/local_process.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/providers/local_process.rs)
- **Lines of Code:** 400 (15183 bytes)

#### Primary Responsibility
Local process, shell, and background job capability providers (CTL-01, CTL-02, TL-02).

#### Types & Trait Declarations
- **Structs (2):** `LocalJobProvider`, `LocalProcessProvider`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(workspace_root: PathBuf) -> Self;
// pub
fn with_supervisor(workspace_root: PathBuf, supervisor: Arc<ProcessSupervisor>) -> Self;
// pub
fn with_sandbox(workspace_root: PathBuf,
        supervisor: Arc<ProcessSupervisor>,
        sandbox: Option<Arc<dyn San;
// pub
fn with_enforcement(mut self, enforcement: crate::sandbox::SandboxEnforcement) -> Self;
// pub
fn set_sandbox_required(&mut self, required: bool);
// pub
fn is_sandbox_required(&self) -> bool;
// private
fn is_network_isolated(&self) -> bool;
// pub
fn sandbox_provider(&self) -> Option<Arc<dyn SandboxProvider>>;
// private
async fn spawn_command(&self,
        program: &str,
        args: &[String],
        working_dir: Option<&Path>,
      ;
// private
async fn terminate_process(&self, pid: u32) -> Result<(), CapabilityError>;
// private
async fn execute_bounded_shell(&self,
        command: &str,
        working_dir: Option<&Path>,
        timeout_secs: u;
// pub
fn new(workspace_root: PathBuf, supervisor: Arc<JobSupervisor>) -> Self;
// pub
fn supervisor(&self) -> &Arc<JobSupervisor>;
// private
async fn start_job(&self,
        command: &str,
        args: &[String],) -> Result<JobDescriptor, CapabilityError>;
// private
async fn start_job_scoped(&self,
        mission_id: crate::ids::MissionId,
        task_id: TaskId,
        agent_id: c;
```

---

### `src/capability/providers/local_sandbox.rs` {#src-capability-providers-local_sandbox-rs}

- **Source Link:** [`src/capability/providers/local_sandbox.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/providers/local_sandbox.rs)
- **Lines of Code:** 120 (4270 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (1):** `LocalSandboxProvider`

#### Key Functions & Signatures (7 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_provider(provider: Arc<dyn SandboxProvider>) -> Self;
// pub
fn provider(&self) -> Arc<dyn SandboxProvider>;
// private
fn capabilities(&self) -> Option<SandboxCapabilities>;
// private
async fn prepare_environment(&self,
        config: &SandboxConfig,) -> Result<SandboxHandle, CapabilityError>;
// private
async fn cleanup_sandbox(&self, handle: &SandboxHandle) -> Result<(), CapabilityError>;
```

---

### `src/capability/providers/local_terminal.rs` {#src-capability-providers-local_terminal-rs}

- **Source Link:** [`src/capability/providers/local_terminal.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/providers/local_terminal.rs)
- **Lines of Code:** 385 (12896 bytes)

#### Primary Responsibility
Local terminal session capability provider (CTL-02, D-01, D-03).

#### Types & Trait Declarations
- **Structs (2):** `LocalTerminalProvider`, `TerminalSessionHandle`

#### Key Functions & Signatures (12 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_workspace(workspace_root: impl Into<PathBuf>) -> Self;
// private
async fn spawn_session_internal(&self,
        session_id: &str,
        config: TerminalSessionConfig,) -> Result<Termi;
// private
async fn start_session(&self,
        session_id: &str,
        config: TerminalSessionConfig,) -> Result<(), Capability;
// private
async fn write_input(&self, session_id: &str, input: &[u8]) -> Result<(), CapabilityError>;
// private
async fn read_stream(&self,
        session_id: &str,
        timeout_ms: u64,) -> Result<Vec<u8>, CapabilityError>;
// private
async fn resize(&self, session_id: &str, cols: u16, rows: u16) -> Result<(), CapabilityError>;
// private
async fn terminate_session(&self, session_id: &str) -> Result<(), CapabilityError>;
// private
async fn session_status(&self,
        session_id: &str,) -> Result<TerminalSessionStatus, CapabilityError>;
// private
async fn cleanup_agent_sessions(&self,
        agent_id: &crate::ids::AgentId,) -> Result<(), CapabilityError>;
// private
async fn cleanup_mission_sessions(&self,
        mission_id: &crate::ids::MissionId,) -> Result<(), CapabilityError>;
```

---

### `src/capability/providers/local_verification.rs` {#src-capability-providers-local_verification-rs}

- **Source Link:** [`src/capability/providers/local_verification.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/providers/local_verification.rs)
- **Lines of Code:** 131 (5934 bytes)

#### Primary Responsibility
Local verification and QA capability provider (CTL-02, D-01, D-03).  Verification commands execute through the same production security boundaries as agent process execution — workspace containment, command safety, environment scrubbing, timeout with kill, and bounded output. There is no "verification is trusted" exemption: verification commands operate on potentially model-modified state and must remain strictly contained.

#### Types & Trait Declarations
- **Structs (1):** `LocalVerificationProvider`

#### Key Functions & Signatures (2 shown)
```rust
// pub
fn new(workspace_root: impl Into<PathBuf>) -> Self;
// private
async fn run_verification(&self,
        target: &VerificationTarget,) -> Result<VerificationReport, CapabilityError>;
```

---

### `src/capability/providers/local_web.rs` {#src-capability-providers-local_web-rs}

- **Source Link:** [`src/capability/providers/local_web.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/providers/local_web.rs)
- **Lines of Code:** 325 (13774 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Web capability provider backed by reqwest (CTL-02, D-01, D-03).

#### Types & Trait Declarations
- **Structs (1):** `LocalWebProvider`

#### Key Functions & Signatures (6 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_policy(destination_policy: NetworkDestinationPolicy) -> Self;
// private
async fn fetch_url(&self,
        url: &str,
        timeout_secs: u64,) -> Result<WebFetchResult, CapabilityError>;
// private
async fn search_web(&self,
        query: &str,
        max_results: usize,) -> Result<Vec<WebSearchResult>, CapabilityE;
// private
fn clean_html(input: &str) -> String;
```

---

### `src/capability/providers/mod.rs` {#src-capability-providers-mod-rs}

- **Source Link:** [`src/capability/providers/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/providers/mod.rs)
- **Lines of Code:** 31 (1052 bytes)

#### Primary Responsibility
Native local capability providers (CTL-02, D-01, D-03).

---

### `src/capability/providers/model_caller.rs` {#src-capability-providers-model_caller-rs}

- **Source Link:** [`src/capability/providers/model_caller.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/providers/model_caller.rs)
- **Lines of Code:** 72 (2281 bytes)

#### Primary Responsibility
Model capability provider wrapping ModelCaller (CTL-02, D-01, D-03).

#### Types & Trait Declarations
- **Structs (1):** `ModelCallerProvider`

#### Key Functions & Signatures (2 shown)
```rust
// pub
fn new(caller: Arc<dyn ModelCaller>, default_model: impl Into<String>) -> Self;
// private
async fn invoke_model(&self,
        request: &ModelInvocationRequest,) -> Result<ModelInvocationResponse, CapabilityErr;
```

---

### `src/capability/providers/repo_graph.rs` {#src-capability-providers-repo_graph-rs}

- **Source Link:** [`src/capability/providers/repo_graph.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/providers/repo_graph.rs)
- **Lines of Code:** 147 (5537 bytes)

#### Primary Responsibility
Repository graph capability provider wrapping BoundedQueryEngine (CTL-02, D-01, D-03).

#### Types & Trait Declarations
- **Structs (1):** `RepositoryGraphProvider`

#### Key Functions & Signatures (7 shown)
```rust
// pub
fn new(workspace_root: impl Into<PathBuf>,
        engine: Option<Arc<BoundedQueryEngine>>,) -> Self;
// private
async fn query_symbols(&self, query: &str) -> Result<Vec<RepositorySymbol>, CapabilityError>;
// private
async fn query_dependencies(&self,
        symbol_id: &str,) -> Result<Vec<RepositorySymbol>, CapabilityError>;
// private
async fn search_code(&self, query: &str) -> Result<Vec<CodeSearchResult>, CapabilityError>;
// private
async fn find_tests(&self, target: &str) -> Result<Vec<String>, CapabilityError>;
// private
async fn analyze_impact(&self,
        changed_files: &[String],) -> Result<crate::repo::query::ChangeImpactReport, Capa;
// private
async fn get_overview(&self) -> Result<crate::repo::types::IndexStatus, CapabilityError>;
```

---

### `src/capability/registry.rs` {#src-capability-registry-rs}

- **Source Link:** [`src/capability/registry.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/registry.rs)
- **Lines of Code:** 608 (22870 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Central capability registry (CTL-01, CTL-02, CTL-03).

#### Types & Trait Declarations
- **Structs (1):** `CapabilityRegistry`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn new_with_auth(auth_authority: Arc<crate::git::AuthorizationAuthority>) -> Self;
// pub
fn with_health_config(health_config: HealthConfig) -> Self;
// pub
fn with_health_config_and_auth(health_config: HealthConfig,
        auth_authority: Arc<crate::git::AuthorizationAuthori;
// pub
fn production(workspace_root: impl AsRef<Path>,
        bus: Option<Arc<dyn crate::events::EventBus>>,
        model_cal;
// pub
fn production_with_auth(workspace_root: impl AsRef<Path>,
        bus: Option<Arc<dyn crate::events::EventBus>>,
       ;
// pub
fn register_instance(&self, instance: CapabilityInstance);
// pub
fn deregister_instance(&self, id: &str) -> Option<CapabilityInstance>;
// pub
fn sync_git_capability(&self,
        workspace_root: impl AsRef<Path>,
        enabled: bool,
        provider: Arc<dyn;
// pub
fn get_instance(&self, id: &str) -> Option<CapabilityInstance>;
// pub
fn list_capabilities(&self) -> Vec<CapabilityInstance>;
// pub
fn is_available(&self, family: &CapabilityFamily) -> bool;
// pub
fn record_success(&self, instance_id: &str);
// pub
fn record_failure(&self,
        instance_id: &str,
        is_infra_fault: bool,
        reason: impl Into<String>,);
```

---

### `src/capability/traits/artifacts.rs` {#src-capability-traits-artifacts-rs}

- **Source Link:** [`src/capability/traits/artifacts.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/traits/artifacts.rs)
- **Lines of Code:** 24 (769 bytes)

#### Primary Responsibility
Immutable artifact storage service trait (CTL-01, CTL-02).

#### Types & Trait Declarations
- **Traits (1):** `ArtifactStoreService`

#### Key Functions & Signatures (2 shown)
```rust
// private
async fn store_artifact(&self,
        artifact_id: &str,
        data: &[u8],
        extension: &str,) -> Result<PathB;
// private
async fn load_artifact(&self,
        artifact_id: &str,
        extension: &str,) -> Result<Vec<u8>, CapabilityError>;
```

---

### `src/capability/traits/fs.rs` {#src-capability-traits-fs-rs}

- **Source Link:** [`src/capability/traits/fs.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/traits/fs.rs)
- **Lines of Code:** 64 (2313 bytes)

#### Primary Responsibility
File system capability service trait (CTL-01, CTL-02).

#### Types & Trait Declarations
- **Structs (1):** `FileMetadata`
- **Traits (1):** `FileSystemService`

#### Key Functions & Signatures (10 shown)
```rust
// private
async fn read_file(&self,
        path: &Path,
        offset: Option<u64>,
        limit: Option<usize>,) -> Result<Vec;
// private
async fn write_file(&self, path: &Path, content: &[u8]) -> Result<usize, CapabilityError>;
// private
async fn edit_file(&self,
        path: &Path,
        old_content: &str,
        new_content: &str,) -> Result<(), Capa;
// private
async fn list_files(&self,
        path: &Path,
        recursive: bool,) -> Result<Vec<PathBuf>, CapabilityError>;
// private
async fn file_metadata(&self, path: &Path) -> Result<FileMetadata, CapabilityError>;
// private
async fn delete_file(&self, path: &Path) -> Result<(), CapabilityError>;
// private
async fn create_directory(&self, path: &Path) -> Result<(), CapabilityError>;
// private
async fn move_file(&self, src: &Path, dst: &Path) -> Result<(), CapabilityError>;
// private
async fn rename_file(&self, src: &Path, dst: &Path) -> Result<(), CapabilityError>;
// private
async fn copy_file(&self, src: &Path, dst: &Path) -> Result<u64, CapabilityError>;
```

---

### `src/capability/traits/git.rs` {#src-capability-traits-git-rs}

- **Source Link:** [`src/capability/traits/git.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/traits/git.rs)
- **Lines of Code:** 122 (4173 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Git version control service trait (CTL-01, CTL-02).

#### Types & Trait Declarations
- **Structs (3):** `GitBranchInfo`, `GitCommitInfo`, `GitStatusResult`
- **Traits (1):** `GitService`

#### Key Functions & Signatures (15 shown)
```rust
// private
async fn status(&self) -> Result<GitStatusResult, CapabilityError>;
// private
async fn diff(&self, staged: bool) -> Result<String, CapabilityError>;
// private
async fn log(&self, max_count: usize) -> Result<Vec<GitCommitInfo>, CapabilityError>;
// private
async fn show(&self, revision: &str) -> Result<String, CapabilityError>;
// private
async fn branch(&self) -> Result<GitBranchInfo, CapabilityError>;
// private
async fn checkout(&self,
        branch_or_commit: &str,
        gate: &crate::git::GitGate,) -> Result<(), CapabilityEr;
// private
async fn add(&self,
        paths: &[PathBuf],
        gate: &crate::git::GitGate,) -> Result<(), CapabilityError>;
// private
async fn commit(&self,
        message: &str,
        gate: &crate::git::GitGate,) -> Result<String, CapabilityError>;
// private
async fn add_all(&self, gate: &crate::git::GitGate) -> Result<(), CapabilityError>;
// private
async fn reset(&self,
        paths: &[&str],
        gate: &crate::git::GitGate,) -> Result<(), CapabilityError>;
// private
async fn commit_with_trailers(&self,
        message: &str,
        trailers: &crate::git::trailers::CommitTrailers,
   ;
// private
async fn merge(&self,
        branch: &str,
        no_edit: bool,
        gate: &crate::git::GitGate,) -> Result<String;
// private
async fn merge_abort(&self, gate: &crate::git::GitGate) -> Result<(), CapabilityError>;
// private
async fn restore_head(&self,
        path: &str,
        gate: &crate::git::GitGate,) -> Result<(), CapabilityError>;
// private
async fn status_porcelain(&self) -> Result<String, CapabilityError>;
```

---

### `src/capability/traits/jobs.rs` {#src-capability-traits-jobs-rs}

- **Source Link:** [`src/capability/traits/jobs.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/traits/jobs.rs)
- **Lines of Code:** 54 (2094 bytes)

#### Primary Responsibility
Background jobs supervision service trait (CTL-01, CTL-02).

#### Types & Trait Declarations
- **Traits (1):** `JobService`

#### Key Functions & Signatures (5 shown)
```rust
// private
async fn start_job(&self,
        command: &str,
        args: &[String],) -> Result<JobDescriptor, CapabilityError>;
// private
async fn start_job_scoped(&self,
        _mission_id: crate::ids::MissionId,
        _task_id: crate::ids::TaskId,
     ;
// private
async fn get_status(&self, job_id: &str) -> Result<JobStatusInfo, CapabilityError>;
// private
async fn get_output(&self,
        job_id: &str,
        offset: u64,
        limit: usize,) -> Result<JobOutputChunk, C;
// private
async fn stop_job(&self, job_id: &str) -> Result<(), CapabilityError>;
```

---

### `src/capability/traits/memory.rs` {#src-capability-traits-memory-rs}

- **Source Link:** [`src/capability/traits/memory.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/traits/memory.rs)
- **Lines of Code:** 19 (613 bytes)

#### Primary Responsibility
Contextual memory service trait (CTL-01, CTL-02).

#### Types & Trait Declarations
- **Traits (1):** `MemoryService`

#### Key Functions & Signatures (2 shown)
```rust
// private
async fn store_memory(&self,
        key: &str,
        value: &str,
        ttl_secs: Option<u64>,) -> Result<(), Capab;
// private
async fn recall_memory(&self, key: &str) -> Result<Option<String>, CapabilityError>;
```

---

### `src/capability/traits/mod.rs` {#src-capability-traits-mod-rs}

- **Source Link:** [`src/capability/traits/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/traits/mod.rs)
- **Lines of Code:** 35 (1137 bytes)

#### Primary Responsibility
The 15 core capability service traits (CTL-01, CTL-02).

---

### `src/capability/traits/model.rs` {#src-capability-traits-model-rs}

- **Source Link:** [`src/capability/traits/model.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/traits/model.rs)
- **Lines of Code:** 32 (1007 bytes)

#### Primary Responsibility
Model inference service trait (CTL-01, CTL-02).

#### Types & Trait Declarations
- **Structs (2):** `ModelInvocationRequest`, `ModelInvocationResponse`
- **Traits (1):** `ModelService`

#### Key Functions & Signatures (1 shown)
```rust
// private
async fn invoke_model(&self,
        request: &ModelInvocationRequest,) -> Result<ModelInvocationResponse, CapabilityErr;
```

---

### `src/capability/traits/network.rs` {#src-capability-traits-network-rs}

- **Source Link:** [`src/capability/traits/network.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/traits/network.rs)
- **Lines of Code:** 14 (565 bytes)

#### Primary Responsibility
Network connectivity and resolution service trait (CTL-01, CTL-02).

#### Types & Trait Declarations
- **Traits (1):** `NetworkService`

#### Key Functions & Signatures (2 shown)
```rust
// private
async fn check_connectivity(&self, host: &str, port: u16) -> Result<bool, CapabilityError>;
// private
async fn resolve_host(&self, host: &str) -> Result<Vec<String>, CapabilityError>;
```

---

### `src/capability/traits/process.rs` {#src-capability-traits-process-rs}

- **Source Link:** [`src/capability/traits/process.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/traits/process.rs)
- **Lines of Code:** 23 (758 bytes)

#### Primary Responsibility
Supervised process execution service trait (CTL-01, CTL-02).

#### Types & Trait Declarations
- **Traits (1):** `ProcessService`

#### Key Functions & Signatures (2 shown)
```rust
// private
async fn spawn_command(&self,
        program: &str,
        args: &[String],
        working_dir: Option<&Path>,
      ;
// private
async fn terminate_process(&self, pid: u32) -> Result<(), CapabilityError>;
```

---

### `src/capability/traits/repo.rs` {#src-capability-traits-repo-rs}

- **Source Link:** [`src/capability/traits/repo.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/traits/repo.rs)
- **Lines of Code:** 44 (1695 bytes)

#### Primary Responsibility
Repository graph and code navigation service trait (CTL-01, CTL-02).

#### Types & Trait Declarations
- **Structs (1):** `CodeSearchResult`
- **Traits (1):** `RepositoryService`

#### Key Functions & Signatures (6 shown)
```rust
// private
async fn query_symbols(&self, query: &str) -> Result<Vec<RepositorySymbol>, CapabilityError>;
// private
async fn query_dependencies(&self,
        symbol_id: &str,) -> Result<Vec<RepositorySymbol>, CapabilityError>;
// private
async fn search_code(&self, query: &str) -> Result<Vec<CodeSearchResult>, CapabilityError>;
// private
async fn find_tests(&self, target: &str) -> Result<Vec<String>, CapabilityError>;
// private
async fn analyze_impact(&self,
        changed_files: &[String],) -> Result<ChangeImpactReport, CapabilityError>;
// private
async fn get_overview(&self) -> Result<IndexStatus, CapabilityError>;
```

---

### `src/capability/traits/sandbox.rs` {#src-capability-traits-sandbox-rs}

- **Source Link:** [`src/capability/traits/sandbox.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/traits/sandbox.rs)
- **Lines of Code:** 55 (1799 bytes)

#### Primary Responsibility
Sandbox boundary and environment service trait (CTL-01, CTL-02).

#### Types & Trait Declarations
- **Structs (2):** `SandboxConfig`, `SandboxHandle`
- **Traits (1):** `SandboxService`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn to_sandbox_plan(&self) -> SandboxPlan;
// private
fn capabilities(&self) -> Option<SandboxCapabilities>;
// private
async fn prepare_environment(&self,
        config: &SandboxConfig,) -> Result<SandboxHandle, CapabilityError>;
// private
async fn cleanup_sandbox(&self, handle: &SandboxHandle) -> Result<(), CapabilityError>;
```

---

### `src/capability/traits/shell.rs` {#src-capability-traits-shell-rs}

- **Source Link:** [`src/capability/traits/shell.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/traits/shell.rs)
- **Lines of Code:** 26 (785 bytes)

#### Primary Responsibility
Bounded shell execution service trait (CTL-01, CTL-02).

#### Types & Trait Declarations
- **Structs (1):** `ShellOutput`
- **Traits (1):** `ShellService`

#### Key Functions & Signatures (1 shown)
```rust
// private
async fn execute_bounded_shell(&self,
        command: &str,
        working_dir: Option<&Path>,
        timeout_secs: u;
```

---

### `src/capability/traits/telemetry.rs` {#src-capability-traits-telemetry-rs}

- **Source Link:** [`src/capability/traits/telemetry.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/traits/telemetry.rs)
- **Lines of Code:** 24 (751 bytes)

#### Primary Responsibility
Telemetry and metrics recording service trait (CTL-01, CTL-02).

#### Types & Trait Declarations
- **Traits (1):** `TelemetryService`

#### Key Functions & Signatures (2 shown)
```rust
// private
async fn record_event(&self,
        event_name: &str,
        attributes: HashMap<String, String>,) -> Result<(), Capab;
// private
async fn record_metric(&self,
        metric_name: &str,
        value: f64,
        unit: &str,) -> Result<(), Capabili;
```

---

### `src/capability/traits/terminal.rs` {#src-capability-traits-terminal-rs}

- **Source Link:** [`src/capability/traits/terminal.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/traits/terminal.rs)
- **Lines of Code:** 106 (3299 bytes)

#### Primary Responsibility
Terminal session service trait (CTL-01, CTL-02).

#### Types & Trait Declarations
- **Structs (2):** `TerminalSessionConfig`, `TerminalSessionStatus`
- **Traits (1):** `TerminalService`

#### Key Functions & Signatures (9 shown)
```rust
// private
fn default() -> Self;
// private
async fn start_session(&self,
        session_id: &str,
        config: TerminalSessionConfig,) -> Result<(), Capability;
// private
async fn write_input(&self, session_id: &str, input: &[u8]) -> Result<(), CapabilityError>;
// private
async fn read_stream(&self,
        session_id: &str,
        timeout_ms: u64,) -> Result<Vec<u8>, CapabilityError>;
// private
async fn resize(&self, session_id: &str, cols: u16, rows: u16) -> Result<(), CapabilityError>;
// private
async fn terminate_session(&self, session_id: &str) -> Result<(), CapabilityError>;
// private
async fn session_status(&self,
        session_id: &str,) -> Result<TerminalSessionStatus, CapabilityError>;
// private
async fn cleanup_agent_sessions(&self,
        _agent_id: &crate::ids::AgentId,) -> Result<(), CapabilityError>;
// private
async fn cleanup_mission_sessions(&self,
        _mission_id: &crate::ids::MissionId,) -> Result<(), CapabilityError>;
```

---

### `src/capability/traits/verification.rs` {#src-capability-traits-verification-rs}

- **Source Link:** [`src/capability/traits/verification.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/traits/verification.rs)
- **Lines of Code:** 43 (1278 bytes)

#### Primary Responsibility
Verification and QA service trait (CTL-01, CTL-02).

#### Types & Trait Declarations
- **Structs (2):** `VerificationReport`, `VerificationTarget`
- **Enums (1):** `VerificationKind`
- **Traits (1):** `VerificationService`

#### Key Functions & Signatures (1 shown)
```rust
// private
async fn run_verification(&self,
        target: &VerificationTarget,) -> Result<VerificationReport, CapabilityError>;
```

---

### `src/capability/traits/web.rs` {#src-capability-traits-web-rs}

- **Source Link:** [`src/capability/traits/web.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/capability/traits/web.rs)
- **Lines of Code:** 41 (1185 bytes)

#### Primary Responsibility
Web access and external search service trait (CTL-01, CTL-02).

#### Types & Trait Declarations
- **Structs (2):** `WebFetchResult`, `WebSearchResult`
- **Traits (1):** `WebService`

#### Key Functions & Signatures (2 shown)
```rust
// private
async fn fetch_url(&self,
        url: &str,
        timeout_secs: u64,) -> Result<WebFetchResult, CapabilityError>;
// private
async fn search_web(&self,
        query: &str,
        max_results: usize,) -> Result<Vec<WebSearchResult>, CapabilityE;
```

---
