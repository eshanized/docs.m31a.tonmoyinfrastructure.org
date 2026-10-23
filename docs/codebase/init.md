# Initialization & Doctor

> **Architectural Layer:** L9 Initialization  
> **Source Directory:** `src/init`  
> **File Count:** 4 source files  

Workspace setup wizard, environment diagnostic probes, and lifecycle bootstrapping.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [doctor.rs](#src-init-doctor-rs) | 429 | `DiagnosticProbe, DoctorEngine, DiagnosticStatus` | Doctor Diagnostics &amp; Environment Precondition Probes (FRX-02, D-02... |
| [instance.rs](#src-init-instance-rs) | 591 | `WorkspaceInstance, WorkspaceInstanceStore, OnboardingReason` | Persistent Workspace-Instance Lifecycle — canonical startup authority.... |
| [lifecycle.rs](#src-init-lifecycle-rs) | 486 | `InitManager, InitSentinel, InitError` | Durable Initialization Lifecycle State Machine (FRX-01, FRX-02, D-01).... |
| [mod.rs](#src-init-mod-rs) | 19 | `Functions/Traits` | Initialization, onboarding lifecycle, and doctor diagnostics (FRX-01–F... |

---

### `src/init/doctor.rs` {#src-init-doctor-rs}

- **Source Link:** [`src/init/doctor.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/init/doctor.rs)
- **Lines of Code:** 429 (16744 bytes)

#### Primary Responsibility
Doctor Diagnostics &amp; Environment Precondition Probes (FRX-02, D-02).  Evaluates host environment readiness across git, repository trust, disk space, SQLite permissions, container sandboxing, and network egress.

#### Types & Trait Declarations
- **Structs (2):** `DiagnosticProbe`, `DoctorEngine`
- **Enums (1):** `DiagnosticStatus`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn badge(&self) -> &'static str;
// pub
fn new() -> Self;
// pub
fn with_mock_mode(mut self, mock: bool) -> Self;
// pub
fn check_git_installed(&self) -> DiagnosticProbe;
// pub
fn check_git_repository(&self, workspace_path: &Path) -> DiagnosticProbe;
// pub
fn check_disk_space(&self, workspace_path: &Path) -> DiagnosticProbe;
// pub
fn check_sqlite_availability(&self, workspace_path: &Path) -> DiagnosticProbe;
// pub
fn check_sandbox_support(&self) -> DiagnosticProbe;
// pub
fn check_network_egress(&self) -> DiagnosticProbe;
// pub
fn check_git_installed_with_options(&self, git_enabled: bool) -> DiagnosticProbe;
// pub
fn check_git_repository_with_options(&self,
        workspace_path: &Path,
        git_enabled: bool,) -> DiagnosticProb;
// pub
fn run_all_with_git_enabled(&self,
        workspace_path: &Path,
        git_enabled: bool,) -> Vec<DiagnosticProbe>;
// pub
fn run_all(&self, workspace_path: &Path) -> Vec<DiagnosticProbe>;
// pub
fn has_blocking_failures(&self, probes: &[DiagnosticProbe]) -> bool;
// pub
fn has_warnings(&self, probes: &[DiagnosticProbe]) -> bool;
```

---

### `src/init/instance.rs` {#src-init-instance-rs}

- **Source Link:** [`src/init/instance.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/init/instance.rs)
- **Lines of Code:** 591 (23379 bytes)

#### Primary Responsibility
Persistent Workspace-Instance Lifecycle — canonical startup authority.  OpenCode-style instance semantics, implemented idiomatically in Rust:  - a workspace instance is deterministically bound to its canonical workspace root (never a fresh identity per process); - the instance is resolved (loaded or created) once per process and cached for the process lifetime; - initialization state is durable (`.m31a/init.json` bootstrap sentinel + canonical SQLite `system_state` record) and survives process restarts; - the onboarding decision depends ONLY on persistent workspace state, never on "a new process just started".  Startup authority chain:  ```text resolve_workspace_instance() -&gt; StartupDecision::&#123;Initialized &#124; NeedsOnboarding&#125; -&gt; optional first-run onboarding (exactly once) -&gt; persist_successful_onboarding() -&gt; refresh/reload instance state -&gt; AppRuntime against that instance -&gt; CLI/TUI projections (receive resolved state; never re-check) ```  All production startup paths MUST go through [`resolve_startup`]. Direct `InitManager::new` + `is_onboarded` checks in startup code are a regression (see `tests/workspace_instance_lifecycle.rs`).

#### Types & Trait Declarations
- **Structs (2):** `WorkspaceInstance`, `WorkspaceInstanceStore`
- **Enums (2):** `OnboardingReason`, `StartupDecision`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn normalize_lexically(path: &Path) -> PathBuf;
// pub
fn canonicalize_workspace_root(input: &Path) -> PathBuf;
// pub
fn workspace_instance_id(canonical_root: &Path) -> String;
// pub
fn workspace_root(&self) -> &Path;
// pub
fn data_dir(&self) -> &Path;
// pub
fn instance_id(&self) -> &str;
// pub
fn state(&self) -> &InitState;
// pub
fn sentinel_present(&self) -> bool;
// pub
fn db_initialized(&self) -> bool;
// pub
fn is_initialized(&self) -> bool;
// pub
fn is_onboarded(&self) -> bool;
// pub
fn needs_onboarding(&self) -> bool;
// pub
fn onboarding_reason(&self) -> Option<OnboardingReason>;
// pub
fn instance(&self) -> &WorkspaceInstance;
// pub
fn needs_onboarding(&self) -> bool;
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`canonicalization_is_stable_for_relative_and_absolute_inputs`, `instance_id_is_deterministic_per_workspace`

---

### `src/init/lifecycle.rs` {#src-init-lifecycle-rs}

- **Source Link:** [`src/init/lifecycle.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/init/lifecycle.rs)
- **Lines of Code:** 486 (19058 bytes)

#### Primary Responsibility
Durable Initialization Lifecycle State Machine (FRX-01, FRX-02, D-01).  Tracks cold startup through UNINITIALIZED, CHECKING, CONFIGURING, VERIFYING, READY, and ONBOARDED states with bootstrap sentinel and SQLite backing.

#### Types & Trait Declarations
- **Structs (2):** `InitManager`, `InitSentinel`
- **Enums (3):** `InitError`, `InitState`, `SetupStep`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn step_number(&self) -> usize;
// pub
fn total_steps() -> usize;
// pub
fn next(&self) -> Option<Self>;
// pub
fn prev(&self) -> Option<Self>;
// pub
fn title(&self) -> &'static str;
// pub
fn label(&self) -> String;
// private
fn default_init_state_version() -> u32;
// private
fn default() -> Self;
// pub
fn new(workspace_root: impl Into<PathBuf>) -> Result<Self, InitError>;
// pub
fn is_sentinel_present(&self) -> bool;
// pub
fn current_state(&self) -> &InitState;
// pub
fn is_onboarded(&self) -> bool;
// pub
fn is_initialized(&self) -> bool;
// pub
fn persist_sentinel(&mut self) -> Result<(), InitError>;
// pub
fn transition_to(&mut self, next: InitState) -> Result<(), InitError>;
```

---

### `src/init/mod.rs` {#src-init-mod-rs}

- **Source Link:** [`src/init/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/init/mod.rs)
- **Lines of Code:** 19 (795 bytes)

#### Primary Responsibility
Initialization, onboarding lifecycle, and doctor diagnostics (FRX-01–FRX-03).  Provides the durable initialization state machine, pre-SQLite bootstrap sentinel, and host environment diagnostic probes.

---
