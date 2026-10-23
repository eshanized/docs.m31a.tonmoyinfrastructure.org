# Sandbox & Confinement

> **Architectural Layer:** L1 Sandbox  
> **Source Directory:** `src/sandbox`  
> **File Count:** 13 source files  

Filesystem sandboxing, network destination policies, and resource confinement.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [capabilities.rs](#src-sandbox-capabilities-rs) | 88 | `SandboxCapabilities` | Explicit runtime sandbox capabilities matrix (SND-02, SND-03, D-05).  ... |
| [enforcement.rs](#src-sandbox-enforcement-rs) | 186 | `ProcessEnforcementRecord, SandboxEnforcement, EnforcementDimensionStatus` | Runtime-authoritative sandbox enforcement policy (SND-04).  The deploy... |
| [limits.rs](#src-sandbox-limits-rs) | 63 | `ResourceLimits` | Resource limits contract and pre-execution hook application (SND-01, D... |
| [mod.rs](#src-sandbox-mod-rs) | 26 | `Functions/Traits` | Sandbox provider subsystem and confinement runtime (SND-01, SND-02, SN... |
| [mode.rs](#src-sandbox-mode-rs) | 125 | `SandboxMode` | Authoritative sandbox mode vocabulary and lifecycle transitions (SND-0... |
| [plan.rs](#src-sandbox-plan-rs) | 238 | `SandboxPlan, NetworkConfinement, SandboxError` | Sandbox execution plan, network confinement modes, and fail-closed val... |
| [probe.rs](#src-sandbox-probe-rs) | 99 | `PlatformProbe` | Platform introspection and sandbox capability detection probe (SND-02,... |
| [provider.rs](#src-sandbox-provider-rs) | 62 | `SandboxExecutionHandle` | Pluggable sandbox provider contract and execution lifecycle handle (SN... |
| [bubblewrap.rs](#src-sandbox-providers-bubblewrap-rs) | 319 | `BubblewrapSandboxProvider` | Linux bubblewrap unprivileged namespace sandbox provider (SND-01, SND-... |
| [macos.rs](#src-sandbox-providers-macos-rs) | 157 | `SeatbeltSandboxProvider` | Native macOS Seatbelt sandbox provider (SND-02, SND-03).  Enforces: - ... |
| [mod.rs](#src-sandbox-providers-mod-rs) | 11 | `Functions/Traits` | Concrete sandbox providers (Linux bubblewrap, macOS Seatbelt, Windows ... |
| [process.rs](#src-sandbox-providers-process-rs) | 111 | `ProcessIsolationProvider` | Process-level fallback isolation provider (SND-02, SND-03).  Non-negot... |
| [windows.rs](#src-sandbox-providers-windows-rs) | 163 | `WindowsSandboxProvider` | Native Windows Job Object sandbox provider (SND-02, SND-03).  Enforces... |

---

### `src/sandbox/capabilities.rs` {#src-sandbox-capabilities-rs}

- **Source Link:** [`src/sandbox/capabilities.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/sandbox/capabilities.rs)
- **Lines of Code:** 88 (3310 bytes)

#### Primary Responsibility
Explicit runtime sandbox capabilities matrix (SND-02, SND-03, D-05).  Non-negotiable invariant: Unsupported sandbox guarantees are NEVER represented as implemented guarantees. If a requested capability cannot be satisfied by the provider, the execution must fail closed immediately.

#### Types & Trait Declarations
- **Structs (1):** `SandboxCapabilities`

#### Key Functions & Signatures (5 shown)
```rust
// pub
fn none() -> Self;
// pub
fn all() -> Self;
// pub
fn supports_fs_isolation(&self) -> bool;
// pub
fn supports_net_isolation(&self) -> bool;
// pub
fn supports_process_isolation(&self) -> bool;
```

---

### `src/sandbox/enforcement.rs` {#src-sandbox-enforcement-rs}

- **Source Link:** [`src/sandbox/enforcement.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/sandbox/enforcement.rs)
- **Lines of Code:** 186 (6833 bytes)

#### Primary Responsibility
Runtime-authoritative sandbox enforcement policy (SND-04).  The deployment configuration's `sandbox_mode` (`strict` &#124; `standard` &#124; `permissive` &#124; `disabled`) is the SOLE authority for whether execution is isolated. Execution backends MUST derive their behavior from the resolved [`SandboxEnforcement`], never from hardcoded `sandbox_required = false`.  ```text strict     → isolation required; network denied (fail closed if unavailable) standard   → isolation required; network denied (fail closed if unavailable) permissive → isolation best-effort; network denied whenever sandboxed disabled   → no sandboxing (explicit operator opt-out; autonomous execution requiring isolation still fails closed upstream) ```  The `M31A_REQUIRE_SANDBOX` environment variable can only STRENGTHEN this policy (request isolation when the deployment allows fallback); it can never weaken a compiled `required` policy into unisolated execution.

#### Types & Trait Declarations
- **Structs (2):** `ProcessEnforcementRecord`, `SandboxEnforcement`
- **Enums (1):** `EnforcementDimensionStatus`

#### Key Functions & Signatures (12 shown)
```rust
// private
fn default() -> Self;
// pub
fn is_active(&self) -> bool;
// pub
fn display_label(&self) -> &'static str;
// private
fn default() -> Self;
// pub
fn from_sandbox_mode(mode: &str) -> Self;
// pub
fn from_mode(mode: super::SandboxMode) -> Self;
// pub
fn env_requires_sandbox() -> bool;
// pub
fn effective_required(&self) -> bool;
// private
fn strict_and_standard_require_isolation_with_denied_network();
// private
fn unknown_mode_fails_closed_to_strict();
// private
fn disabled_never_requires();
// private
fn permissive_sandboxes_isolated_when_available();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`strict_and_standard_require_isolation_with_denied_network`, `unknown_mode_fails_closed_to_strict`, `disabled_never_requires`, `permissive_sandboxes_isolated_when_available`

---

### `src/sandbox/limits.rs` {#src-sandbox-limits-rs}

- **Source Link:** [`src/sandbox/limits.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/sandbox/limits.rs)
- **Lines of Code:** 63 (2275 bytes)

#### Primary Responsibility
Resource limits contract and pre-execution hook application (SND-01, D-08).

#### Types & Trait Declarations
- **Structs (1):** `ResourceLimits`

#### Key Functions & Signatures (3 shown)
```rust
// private
fn default() -> Self;
// pub
fn new(timeout_ms: u64, max_output_bytes: usize) -> Self;
// pub
fn apply_pre_exec_limits(limits: &ResourceLimits) -> Result<(), std::io::Error>;
```

---

### `src/sandbox/mod.rs` {#src-sandbox-mod-rs}

- **Source Link:** [`src/sandbox/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/sandbox/mod.rs)
- **Lines of Code:** 26 (1125 bytes)

#### Primary Responsibility
Sandbox provider subsystem and confinement runtime (SND-01, SND-02, SND-03).  Non-negotiable invariants: - "The model proposes. The runtime decides." (Model output is untrusted). - Pluggable `SandboxProvider` abstraction with explicit `SandboxCapabilities` matrix. - Unsupported sandbox guarantees are NEVER represented as implemented guarantees. - Execution boundaries fail closed if requested capabilities are unsatisfied. - Network confinement is deny-by-default (--unshare-net).

---

### `src/sandbox/mode.rs` {#src-sandbox-mode-rs}

- **Source Link:** [`src/sandbox/mode.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/sandbox/mode.rs)
- **Lines of Code:** 125 (3928 bytes)

#### Primary Responsibility
Authoritative sandbox mode vocabulary and lifecycle transitions (SND-04).

#### Types & Trait Declarations
- **Enums (1):** `SandboxMode`

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// pub
fn strength_rank(&self) -> u8;
// pub
fn can_transition_monotonically_to(&self, target: SandboxMode) -> bool;
// pub
fn is_more_restrictive_than(&self, other: SandboxMode) -> bool;
// pub
fn next_wizard_mode(&self) -> Self;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn test_sandbox_mode_roundtrip();
// private
fn test_wizard_cycle_covers_all_modes();
// private
fn test_invalid_mode_rejected();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_sandbox_mode_roundtrip`, `test_wizard_cycle_covers_all_modes`, `test_invalid_mode_rejected`

---

### `src/sandbox/plan.rs` {#src-sandbox-plan-rs}

- **Source Link:** [`src/sandbox/plan.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/sandbox/plan.rs)
- **Lines of Code:** 238 (8596 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Sandbox execution plan, network confinement modes, and fail-closed validation (SND-02, SND-03, D-05).

#### Types & Trait Declarations
- **Structs (1):** `SandboxPlan`
- **Enums (3):** `NetworkConfinement`, `SandboxError`, `SandboxViolation`

#### Key Functions & Signatures (11 shown)
```rust
// pub
fn new(workspace_root: PathBuf) -> Self;
// pub
fn with_working_dir(mut self, working_dir: PathBuf) -> Self;
// pub
fn with_fs_isolation(mut self, required: bool) -> Self;
// pub
fn with_net_isolation(mut self, required: bool) -> Self;
// pub
fn with_network_confinement(mut self, mode: NetworkConfinement) -> Self;
// pub
fn with_resource_limits(mut self, limits: ResourceLimits) -> Self;
// pub
fn with_env_var(mut self, key: impl Into<String>, value: impl Into<String>) -> Self;
// pub
fn with_extra_ro_mount(mut self, path: PathBuf) -> Self;
// pub
fn is_denied_extra_ro_mount(path: &std::path::Path) -> bool;
// pub
fn validate_extra_ro_mounts(&self) -> Result<(), SandboxError>;
// pub
fn validate_against(&self, caps: &SandboxCapabilities) -> Result<(), SandboxError>;
```

---

### `src/sandbox/probe.rs` {#src-sandbox-probe-rs}

- **Source Link:** [`src/sandbox/probe.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/sandbox/probe.rs)
- **Lines of Code:** 99 (3526 bytes)

#### Primary Responsibility
Platform introspection and sandbox capability detection probe (SND-02, SND-03).  Detection facts come from the platform boundary. This probe keeps the historical `SandboxCapabilities` shape so existing policy and provider selection logic observes no behavior change on Linux.

#### Types & Trait Declarations
- **Structs (1):** `PlatformProbe`

#### Key Functions & Signatures (5 shown)
```rust
// pub
fn detect_bwrap_path() -> Option<PathBuf>;
// private
fn verify_bwrap_executable(path: &Path) -> bool;
// pub
fn probe_user_namespaces() -> bool;
// pub
fn probe_cgroups_v2() -> bool;
// pub
fn probe_platform_capabilities() -> SandboxCapabilities;
```

---

### `src/sandbox/provider.rs` {#src-sandbox-provider-rs}

- **Source Link:** [`src/sandbox/provider.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/sandbox/provider.rs)
- **Lines of Code:** 62 (2189 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Pluggable sandbox provider contract and execution lifecycle handle (SND-02, D-05).

#### Types & Trait Declarations
- **Structs (1):** `SandboxExecutionHandle`
- **Traits (1):** `SandboxProvider`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn new(id: impl Into<String>, workspace_root: PathBuf, temp_dir: Option<PathBuf>) -> Self;
// private
fn id(&self) -> &str;
// private
fn capabilities(&self) -> SandboxCapabilities;
// private
async fn prepare(&self, plan: &SandboxPlan) -> Result<SandboxExecutionHandle, SandboxError>;
// private
fn build_command(&self,
        plan: &SandboxPlan,
        handle: &SandboxExecutionHandle,
        program: &str,
    ;
// private
async fn cleanup(&self, handle: &SandboxExecutionHandle) -> Result<(), SandboxError>;
```

---

### `src/sandbox/providers/bubblewrap.rs` {#src-sandbox-providers-bubblewrap-rs}

- **Source Link:** [`src/sandbox/providers/bubblewrap.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/sandbox/providers/bubblewrap.rs)
- **Lines of Code:** 319 (11101 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Linux bubblewrap unprivileged namespace sandbox provider (SND-01, SND-02, D-06, D-07).

#### Types & Trait Declarations
- **Structs (1):** `BubblewrapSandboxProvider`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn new(bwrap_path: PathBuf) -> Self;
// pub
fn build_command_args(&self,
        plan: &SandboxPlan,
        private_tmp: &Path,
        program: &str,
        args;
// pub
fn build_command(&self,
        plan: &SandboxPlan,
        handle: &SandboxExecutionHandle,
        program: &str,
    ;
// private
fn id(&self) -> &str;
// private
fn capabilities(&self) -> SandboxCapabilities;
// private
async fn prepare(&self, plan: &SandboxPlan) -> Result<SandboxExecutionHandle, SandboxError>;
// private
fn build_command(&self,
        plan: &SandboxPlan,
        handle: &SandboxExecutionHandle,
        program: &str,
    ;
// private
async fn cleanup(&self, handle: &SandboxExecutionHandle) -> Result<(), SandboxError>;
```

---

### `src/sandbox/providers/macos.rs` {#src-sandbox-providers-macos-rs}

- **Source Link:** [`src/sandbox/providers/macos.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/sandbox/providers/macos.rs)
- **Lines of Code:** 157 (5268 bytes)

#### Primary Responsibility
Native macOS Seatbelt sandbox provider (SND-02, SND-03).  Enforces: - Workspace directory write isolation via `sandbox-exec` Seatbelt profiles. - Network denial egress boundary when configured. - Process group isolation and POSIX resource limits via platform contract. - Deny-by-default environment sanitization. - Private temporary directory per execution.

#### Types & Trait Declarations
- **Structs (1):** `SeatbeltSandboxProvider`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn new() -> Self;
// private
fn id(&self) -> &str;
// private
fn capabilities(&self) -> SandboxCapabilities;
// private
async fn prepare(&self, plan: &SandboxPlan) -> Result<SandboxExecutionHandle, SandboxError>;
// private
fn build_command(&self,
        plan: &SandboxPlan,
        handle: &SandboxExecutionHandle,
        program: &str,
    ;
// private
async fn cleanup(&self, handle: &SandboxExecutionHandle) -> Result<(), SandboxError>;
// private
fn test_seatbelt_provider_capabilities();
// private
async fn test_seatbelt_provider_prepare_validates_plan();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_seatbelt_provider_capabilities`, `test_seatbelt_provider_prepare_validates_plan`

---

### `src/sandbox/providers/mod.rs` {#src-sandbox-providers-mod-rs}

- **Source Link:** [`src/sandbox/providers/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/sandbox/providers/mod.rs)
- **Lines of Code:** 11 (361 bytes)

#### Primary Responsibility
Concrete sandbox providers (Linux bubblewrap, macOS Seatbelt, Windows Job Object, and fallback process isolation).

---

### `src/sandbox/providers/process.rs` {#src-sandbox-providers-process-rs}

- **Source Link:** [`src/sandbox/providers/process.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/sandbox/providers/process.rs)
- **Lines of Code:** 111 (3681 bytes)

#### Primary Responsibility
Process-level fallback isolation provider (SND-02, SND-03).  Non-negotiable invariant (SND-03, D-05): Explicitly declares the absence of filesystem and network isolation. If a plan requires filesystem or network confinement, it strictly fails closed with `CapabilitiesUnsatisfied` and never performs silent fallback.

#### Types & Trait Declarations
- **Structs (1):** `ProcessIsolationProvider`

#### Key Functions & Signatures (7 shown)
```rust
// pub
fn new() -> Self;
// pub
fn build_command(&self,
        plan: &SandboxPlan,
        program: &str,
        args: &[String],) -> Result<Command, ;
// private
fn id(&self) -> &str;
// private
fn capabilities(&self) -> SandboxCapabilities;
// private
async fn prepare(&self, plan: &SandboxPlan) -> Result<SandboxExecutionHandle, SandboxError>;
// private
fn build_command(&self,
        plan: &SandboxPlan,
        _handle: &SandboxExecutionHandle,
        program: &str,
   ;
// private
async fn cleanup(&self, _handle: &SandboxExecutionHandle) -> Result<(), SandboxError>;
```

---

### `src/sandbox/providers/windows.rs` {#src-sandbox-providers-windows-rs}

- **Source Link:** [`src/sandbox/providers/windows.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/sandbox/providers/windows.rs)
- **Lines of Code:** 163 (5999 bytes)

#### Primary Responsibility
Native Windows Job Object sandbox provider (SND-02, SND-03).  Enforces: - Job Object containment boundary (tree termination + memory/CPU/process count limits). - Workspace directory containment validation (via platform Windows path security). - Deny-by-default environment sanitization. - Private temporary directory per execution. - Credential protection via Windows DACL enforcement.

#### Types & Trait Declarations
- **Structs (1):** `WindowsSandboxProvider`

#### Key Functions & Signatures (9 shown)
```rust
// pub
fn new() -> Self;
// private
fn id(&self) -> &str;
// private
fn capabilities(&self) -> SandboxCapabilities;
// private
async fn prepare(&self, plan: &SandboxPlan) -> Result<SandboxExecutionHandle, SandboxError>;
// private
fn build_command(&self,
        plan: &SandboxPlan,
        handle: &SandboxExecutionHandle,
        program: &str,
    ;
// private
async fn cleanup(&self, handle: &SandboxExecutionHandle) -> Result<(), SandboxError>;
// private
fn test_windows_provider_capabilities();
// private
async fn test_windows_provider_prepare_validates_plan();
// private
fn test_windows_provider_build_command_sets_cwd();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_windows_provider_capabilities`, `test_windows_provider_prepare_validates_plan`, `test_windows_provider_build_command_sets_cwd`

---
