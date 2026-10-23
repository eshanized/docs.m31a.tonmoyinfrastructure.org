# Platform Abstractions

> **Architectural Layer:** L1 Platform  
> **Source Directory:** `src/platform`  
> **File Count:** 17 source files  

Cross-platform OS primitives (Linux, macOS, Windows), process control, and path handling.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [capabilities.rs](#src-platform-capabilities-rs) | 279 | `CapabilityShortfall, PlatformCapabilities, Capability` | Typed host capability model.  Callers ask whether the host can actuall... |
| [errors.rs](#src-platform-errors-rs) | 226 | `PlatformError` | Stable native-operation error taxonomy.  Raw operating-system failures... |
| [filesystem.rs](#src-platform-filesystem-rs) | 362 | `HostFilesystem` | Host filesystem primitives behind one portable surface.  Containment c... |
| [macos.rs](#src-platform-macos-rs) | 366 | `ProcBsdInfoPartial` | Native macOS backend behind the platform contract.  Mechanisms used: -... |
| [mod.rs](#src-platform-mod-rs) | 253 | `PlatformInfo, PlatformServices, PlatformFamily` | Operating-system abstraction boundary for the runtime.  The runtime st... |
| [permissions.rs](#src-platform-permissions-rs) | 103 | `FileSecurityOutcome` | Credential-bearing file protection behind a portable contract.  The se... |
| [process.rs](#src-platform-process-rs) | 398 | `PlatformProcessError` | Native process-tree contract.  The runtime guarantee is that a termina... |
| [resources.rs](#src-platform-resources-rs) | 280 | `ResourceBudget, LimitOutcome` | Semantic resource budgets separated from enforcement mechanisms.  The ... |
| [sandbox.rs](#src-platform-sandbox-rs) | 189 | `SandboxShortfall, IsolationLevel, SandboxReadiness` | Capability-based sandbox vocabulary.  Higher layers request an isolati... |
| [shell.rs](#src-platform-shell-rs) | 205 | `ShellAvailability, ShellError, ShellRequest` | Native shell selection behind an explicit contract.  Direct argument-v... |
| [terminal.rs](#src-platform-terminal-rs) | 141 | `TerminalCapabilities, TerminalBackend` | Terminal and console boundary.  Runtime layers need dimensions, raw-mo... |
| [acl.rs](#src-platform-windows-acl-rs) | 122 | `AclOutcome` | Windows credential-file protection via security descriptors.  Unix mod... |
| [conpty.rs](#src-platform-windows-conpty-rs) | 164 | `ConsoleSize, PseudoConsole` | Windows Console Pseudo-console (ConPTY) backend surface.  ConPTY is th... |
| [job.rs](#src-platform-windows-job-rs) | 471 | `FileTime, IoCounters, JobAttributes` | Windows Job Object backend for process-tree control and limits.  Job O... |
| [mod.rs](#src-platform-windows-mod-rs) | 147 | `Functions/Traits` | Windows native backend aggregator.  Re-exports the focused Windows mec... |
| [path.rs](#src-platform-windows-path-rs) | 274 | `Functions/Traits` | Windows path security: containment without string-prefix traps.  Windo... |
| [shell.rs](#src-platform-windows-shell-rs) | 207 | `ShellBackend` | Native Windows shell backends.  Direct argument-vector execution is al... |

---

### `src/platform/capabilities.rs` {#src-platform-capabilities-rs}

- **Source Link:** [`src/platform/capabilities.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/capabilities.rs)
- **Lines of Code:** 279 (10221 bytes)

#### Primary Responsibility
Typed host capability model.  Callers ask whether the host can actually enforce a requirement instead of branching on the operating-system name. A capability can be fully present, absent, degraded, explicitly unsupported on this backend, or still unknown when probing was impossible.  Linux: probes bubblewrap, cgroups, user namespaces macOS: probes libproc, setrlimit, sandbox-exec/Seatbelt, PTY Windows: probes Job Objects, ConPTY, cmd.exe/PowerShell, ACLs

#### Types & Trait Declarations
- **Structs (2):** `CapabilityShortfall`, `PlatformCapabilities`
- **Enums (2):** `Capability`, `CapabilityState`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn usable(&self) -> bool;
// pub
fn degraded_usable(&self) -> bool;
// pub
fn probe_host() -> Self;
// pub
fn foundation_for(family: PlatformFamily) -> Self;
// private
fn linux_host() -> Self;
// private
fn macos_foundation() -> Self;
// private
fn windows_foundation() -> Self;
// private
fn generic_unix() -> Self;
// private
fn unknown() -> Self;
// pub
fn state_of(&self, capability: Capability) -> CapabilityState;
// pub
fn require(&self, capability: Capability) -> Result<(), CapabilityShortfall>;
// pub
fn sandboxing_label(&self) -> &'static str;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn probe_host_returns_usable_on_linux();
// private
fn foundation_profiles_distinct();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`probe_host_returns_usable_on_linux`, `foundation_profiles_distinct`

---

### `src/platform/errors.rs` {#src-platform-errors-rs}

- **Source Link:** [`src/platform/errors.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/errors.rs)
- **Lines of Code:** 226 (9536 bytes)
- **Runtime Properties:** 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Stable native-operation error taxonomy.  Raw operating-system failures vary across hosts. Callers match on this type for control flow and keep the underlying message for diagnostics. Secrets are never embedded in these values; display strings carry only the operation, the category, and the non-sensitive detail.

#### Types & Trait Declarations
- **Enums (1):** `PlatformError`

#### Key Functions & Signatures (12 shown)
```rust
// pub
fn category(&self) -> &'static str;
// pub
fn operation(&self) -> &str;
// pub
fn retryable(&self) -> bool;
// pub
fn fail_closed(&self) -> bool;
// pub
fn diagnostic(&self) -> String;
// pub
fn telemetry_event(&self) -> &'static str;
// pub
fn recovery(&self) -> &'static str;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn from_io(operation: &str, err: &std::io::Error) -> PlatformError;
// private
fn unsupported_is_not_retryable_and_fails_closed();
// private
fn cancelled_is_control_flow_not_integrity_failure();
// private
fn io_translation_preserves_categories();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`unsupported_is_not_retryable_and_fails_closed`, `cancelled_is_control_flow_not_integrity_failure`, `io_translation_preserves_categories`

---

### `src/platform/filesystem.rs` {#src-platform-filesystem-rs}

- **Source Link:** [`src/platform/filesystem.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/filesystem.rs)
- **Lines of Code:** 362 (12145 bytes)

#### Primary Responsibility
Host filesystem primitives behind one portable surface.  Containment checks and canonicalization stay centralized in their owning modules. This module supplies only the operating-system facts those checks need: where temporary data lives, which device discards output, and how two paths compare for identity on the current host.  Windows path security uses the dedicated windows/path module to resist prefix tricks, case folding, UNC, drive letters, reserved names, and reparse-point redirection. macOS uses Unix permission semantics with platform-probed behavior.

#### Types & Trait Declarations
- **Structs (1):** `HostFilesystem`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn temp_root() -> PathBuf;
// pub
fn fresh_temp_dir(prefix: &str) -> Result<tempfile::TempDir, std::io::Error>;
// pub
fn null_device() -> &'static str;
// pub
fn default_path_value() -> String;
// pub
fn confinement_staging_dir() -> PathBuf;
// pub
fn has_cgroup_controllers() -> bool;
// pub
fn has_user_namespaces() -> bool;
// pub
fn paths_identical(left: &Path, right: &Path) -> bool;
// pub
fn validate_containment(workspace: &Path, candidate: &Path) -> Result<PathBuf, String>;
// pub
fn needs_canonicalization(path: &Path) -> bool;
// pub
fn available_space_bytes(path: &Path) -> Option<u64>;
// private
fn GetDiskFreeSpaceExW(lpDirectoryName: *const u16,
                    lpFreeBytesAvailableToCaller: *mut u64,
        ;
// pub
fn find_executable(name: &str) -> Option<PathBuf>;
// pub
fn windows_executable_candidates(name: &str, pathext: &str) -> Vec<String>;
// private
fn temp_root_is_non_empty();
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`temp_root_is_non_empty`, `null_device_is_correct_for_host`, `paths_identical_case_insensitive_on_windows`, `containment_rejects_escape`, `test_windows_executable_candidates`, `test_find_executable_finds_system_command`

---

### `src/platform/macos.rs` {#src-platform-macos-rs}

- **Source Link:** [`src/platform/macos.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/macos.rs)
- **Lines of Code:** 366 (12743 bytes)

#### Primary Responsibility
Native macOS backend behind the platform contract.  Mechanisms used: - process groups via `setpgid` / `kill(-pgid, ...)` for tree control, with `libproc` identity checks against identifier recycling; - POSIX `setrlimit` for CPU, address-space, file-descriptor, and process budgets where the kernel honors them; - Unix owner-only mode bits for credential-bearing files; - `sandbox-exec` with Seatbelt profiles as an optional filesystem isolation backend where the deployment still provides it; - POSIX shell and PTY-backed terminals shared with other Unix hosts.  Pure helpers (profile rendering, budget mapping, availability parsing) compile on every host so contract tests exercise them natively. Raw system bindings are confined to `target_os = "macos"` sections.

#### Types & Trait Declarations
- **Structs (1):** `ProcBsdInfoPartial`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn supports_starttime_protection() -> bool;
// pub
fn process_backend_name() -> &'static str;
// pub
fn read_process_starttime(pid: u32) -> Option<u64>;
// private
fn macos_proc_starttime(pid: u32) -> Option<u64>;
// private
fn proc_pidinfo(pid: i32,
            flavor: i32,
            arg: u64,
            buffer: *mut std::ffi::c_void,
    ;
// pub
fn macos_pid_alive(pid: u32) -> bool;
// pub
fn macos_enforceable_limits(budget: &ResourceBudget) -> (Vec<String>, Vec<String>);
// pub
fn validate_macos_budget(budget: &ResourceBudget) -> Result<LimitOutcome, LimitOutcome>;
// pub
fn sandbox_exec_candidates() -> Vec<PathBuf>;
// pub
fn find_sandbox_exec() -> Option<PathBuf>;
// pub
fn sandbox_availability() -> CapabilityState;
// pub
fn seatbelt_profile_for_workspace(workspace: &Path, temp_root: &Path) -> String;
// pub
fn sandbox_exec_command(workspace: &Path,
    program: &str,
    args: &[String],) -> Option<std::process::Command>;
// pub
fn native_shell_program() -> Option<&'static str>;
// pub
fn terminal_backend_name() -> &'static str;
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`seatbelt_profile_confines_writes_to_workspace`, `macos_budget_mapping_is_typed`, `macos_probe_never_claims_full_sandbox`, `starttime_probe_is_safe_off_macos`

---

### `src/platform/mod.rs` {#src-platform-mod-rs}

- **Source Link:** [`src/platform/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/mod.rs)
- **Lines of Code:** 253 (9215 bytes)

#### Primary Responsibility
Operating-system abstraction boundary for the runtime.  The runtime states requirements (terminate a worker tree, enforce a memory budget, create a private file). Each operating system supplies the mechanism underneath that requirement. Higher layers depend on the contracts in this module rather than on raw system calls, fixed filesystem paths, or shell names so native backends can vary without rewriting runtime logic.  Layout concentrates system conditionals here. Callers outside this directory treat the public functions as the single source of truth for host identity, capability reporting, and native behavior selection.

#### Types & Trait Declarations
- **Structs (2):** `PlatformInfo`, `PlatformServices`
- **Enums (1):** `PlatformFamily`

#### Key Functions & Signatures (10 shown)
```rust
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// pub
fn host() -> Self;
// pub
fn summary(&self) -> String;
// pub
fn host() -> Self;
// pub
fn process_backend_name(&self) -> &'static str;
// private
fn current_rust_target() -> &'static str;
// pub
fn host() -> Self;
// pub
fn for_family(family: PlatformFamily) -> Self;
// private
fn platform_info_host_is_consistent();
// private
fn platform_services_host_probes_capabilities();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`platform_info_host_is_consistent`, `platform_services_host_probes_capabilities`

---

### `src/platform/permissions.rs` {#src-platform-permissions-rs}

- **Source Link:** [`src/platform/permissions.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/permissions.rs)
- **Lines of Code:** 103 (3310 bytes)

#### Primary Responsibility
Credential-bearing file protection behind a portable contract.  The security requirement is that private files are reachable only under the intended owner policy. Unix enforces owner-only mode bits (0o600). Windows restricts the file DACL to owner and administrators with inheritance disabled. Hosts without the primitive must say so explicitly instead of reporting success while leaving the file broadly readable.

#### Types & Trait Declarations
- **Enums (1):** `FileSecurityOutcome`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn ensure_private_file(path: &Path) -> Result<FileSecurityOutcome, std::io::Error>;
// private
fn unix_enforce(path: &Path) -> Result<FileSecurityOutcome, std::io::Error>;
// pub
fn supports_private_files() -> bool;
// pub
fn enforcement_description() -> &'static str;
// private
fn supports_files_on_targets();
// private
fn description_is_non_empty();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`supports_files_on_targets`, `description_is_non_empty`

---

### `src/platform/process.rs` {#src-platform-process-rs}

- **Source Link:** [`src/platform/process.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/process.rs)
- **Lines of Code:** 398 (12407 bytes)

#### Primary Responsibility
Native process-tree contract.  The runtime guarantee is that a terminated child execution leaves no uncontrolled descendant running after the operation reports completion. Linux uses process groups; macOS uses process groups with libproc identity checks; Windows uses Job Objects. Other backends report their honest foundation state instead of pretending a plain child kill provides equivalent isolation.

#### Types & Trait Declarations
- **Enums (1):** `PlatformProcessError`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn from(value: std::io::Error) -> Self;
// pub
fn supports_tree_termination() -> bool;
// pub
fn backend_name() -> &'static str;
// pub
fn configure_isolation(cmd: &mut Command);
// pub
fn spawn_isolated(mut cmd: Command) -> Result<(Child, u32), std::io::Error>;
// pub
async fn terminate_supervised_child(child: &mut Child,
    pid: u32,
    grace_period: Duration,) -> Result<std::process;
// pub
async fn terminate_process_tree_by_pid(pid: u32,
    grace_period: Duration,) -> Result<(), PlatformProcessError>;
// private
async fn terminate_unix_tree(child: &mut Child,
    pid: u32,
    grace_period: Duration,) -> Result<std::process::ExitS;
// private
async fn terminate_macos_tree(child: &mut Child,
    pid: u32,
    grace_period: Duration,) -> Result<std::process::Exit;
// private
async fn terminate_macos_tree_by_pid(pid: u32,
    grace_period: Duration,) -> Result<(), PlatformProcessError>;
// private
async fn terminate_unix_tree_by_pid(pid: u32,
    grace_period: Duration,) -> Result<(), PlatformProcessError>;
// pub
fn is_process_alive(pid: u32) -> bool;
// pub
async fn is_binary_available(cmd: &str) -> bool;
// pub
fn read_process_starttime(pid: u32) -> Option<u64>;
// pub
fn supports_starttime_protection() -> bool;
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`backend_name_matches_host`, `supports_tree_termination_on_targets`, `configure_isolation_compiles_on_all_hosts`, `read_process_starttime_safe_off_target`

---

### `src/platform/resources.rs` {#src-platform-resources-rs}

- **Source Link:** [`src/platform/resources.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/resources.rs)
- **Lines of Code:** 280 (9399 bytes)

#### Primary Responsibility
Semantic resource budgets separated from enforcement mechanisms.  The runtime declares what a step may consume. The host reports what it actually enforced. Callers must propagate the outcome instead of assuming a limit took effect.  Linux: POSIX rlimits + cgroups v2 macOS: POSIX rlimits (RLIMIT_CPU, RLIMIT_AS, RLIMIT_NOFILE, RLIMIT_NPROC) Windows: Job Objects (CPU rate, memory, active process count)

#### Types & Trait Declarations
- **Structs (1):** `ResourceBudget`
- **Enums (1):** `LimitOutcome`

#### Key Functions & Signatures (11 shown)
```rust
// private
fn default() -> Self;
// pub
fn validate_budget(budget: &ResourceBudget) -> Result<(), LimitOutcome>;
// pub
fn host_enforcement_profile() -> LimitOutcome;
// pub
fn apply_pre_exec_limits(budget: &ResourceBudget) -> Result<LimitOutcome, std::io::Error>;
// pub
fn apply_pre_exec_limits(budget: &ResourceBudget) -> Result<LimitOutcome, std::io::Error>;
// pub
fn apply_pre_exec_limits(_budget: &ResourceBudget) -> Result<LimitOutcome, std::io::Error>;
// pub
fn apply_pre_exec_limits(_budget: &ResourceBudget) -> Result<LimitOutcome, std::io::Error>;
// pub
fn install_pre_exec_hook(cmd: &mut tokio::process::Command, budget: ResourceBudget);
// private
fn validate_rejects_zero_limits();
// private
fn default_budget_is_valid();
// private
fn profile_reports_applied_on_supported_hosts();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`validate_rejects_zero_limits`, `default_budget_is_valid`, `profile_reports_applied_on_supported_hosts`

---

### `src/platform/sandbox.rs` {#src-platform-sandbox-rs}

- **Source Link:** [`src/platform/sandbox.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/sandbox.rs)
- **Lines of Code:** 189 (6703 bytes)

#### Primary Responsibility
Capability-based sandbox vocabulary.  Higher layers request an isolation level. This module maps the request onto what the host probe actually found. The bubblewrap binary remains a Linux implementation detail; macOS uses Seatbelt/sandbox-exec; Windows uses Job Object process containment. The runtime reasons about filesystem or network isolation, never about a binary name.

#### Types & Trait Declarations
- **Structs (1):** `SandboxShortfall`
- **Enums (2):** `IsolationLevel`, `SandboxReadiness`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn needs_filesystem(&self) -> bool;
// pub
fn needs_network(&self) -> bool;
// pub
fn backend_name(capabilities: &PlatformCapabilities) -> &'static str;
// pub
fn describe_isolation(capabilities: &PlatformCapabilities) -> Vec<IsolationLevel>;
// pub
fn check_isolation_available(capabilities: &PlatformCapabilities,
    required: IsolationLevel,) -> Result<SandboxReadin;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn describe_isolation_includes_process_isolation_when_tree_control_available();
// private
fn filesystem_isolation_degraded_allows_degraded_readiness();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`describe_isolation_includes_process_isolation_when_tree_control_available`, `filesystem_isolation_degraded_allows_degraded_readiness`

---

### `src/platform/shell.rs` {#src-platform-shell-rs}

- **Source Link:** [`src/platform/shell.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/shell.rs)
- **Lines of Code:** 205 (5598 bytes)

#### Primary Responsibility
Native shell selection behind an explicit contract.  Direct argument-vector execution is always preferred because it never interprets metacharacters. Shell-string execution exists only for explicitly authorized steps and must resolve the interpreter through this module so higher layers never assume a fixed shell name.  Linux/macOS/Unix: POSIX `sh -c` Windows: `cmd.exe /D /S /C` (default) or `powershell.exe -NoProfile -NonInteractive -Command`

#### Types & Trait Declarations
- **Enums (3):** `ShellAvailability`, `ShellError`, `ShellRequest`

#### Key Functions & Signatures (11 shown)
```rust
// pub
fn native_shell_program() -> Option<&'static str>;
// pub
fn backend_name() -> &'static str;
// pub
fn shell_availability() -> ShellAvailability;
// pub
fn build_shell_command(shell_str: &str,
    cwd: &Path,) -> Result<tokio::process::Command, ShellError>;
// pub
fn try_build_powershell_command(shell_str: &str,
    cwd: &Path,) -> Result<tokio::process::Command, ShellError>;
// pub
fn try_build_pwsh_command(shell_str: &str,
    cwd: &Path,) -> Result<tokio::process::Command, ShellError>;
// pub
fn is_shell_program(program: &str) -> bool;
// private
fn native_shell_program_on_unix();
// private
fn native_shell_program_on_windows();
// private
fn build_shell_command_compiles();
// private
fn is_shell_program_recognizes_known();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`native_shell_program_on_unix`, `native_shell_program_on_windows`, `build_shell_command_compiles`, `is_shell_program_recognizes_known`

---

### `src/platform/terminal.rs` {#src-platform-terminal-rs}

- **Source Link:** [`src/platform/terminal.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/terminal.rs)
- **Lines of Code:** 141 (3922 bytes)

#### Primary Responsibility
Terminal and console boundary.  Runtime layers need dimensions, raw-mode control, and PTY availability. Unix (Linux/macOS) supplies PTY-backed terminals; Windows uses ConPTY.

#### Types & Trait Declarations
- **Structs (1):** `TerminalCapabilities`
- **Enums (1):** `TerminalBackend`

#### Key Functions & Signatures (9 shown)
```rust
// pub
fn probe_host() -> Self;
// pub
fn unix_foundation() -> Self;
// pub
fn unavailable() -> Self;
// pub
fn windows_foundation() -> Self;
// pub
fn supports_pty(&self) -> bool;
// pub
fn backend_name() -> &'static str;
// pub
fn pty_available() -> bool;
// private
fn probe_host_returns_foundation_on_unix();
// private
fn backend_name_is_non_empty();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`probe_host_returns_foundation_on_unix`, `backend_name_is_non_empty`

---

### `src/platform/windows/acl.rs` {#src-platform-windows-acl-rs}

- **Source Link:** [`src/platform/windows/acl.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/windows/acl.rs)
- **Lines of Code:** 122 (3797 bytes)

#### Primary Responsibility
Windows credential-file protection via security descriptors.  Unix mode bits do not exist on Windows. Protection means restricting the file discretionary access list to the owner and local administrators and disabling inheritance from the parent directory. Enforcement state stays typed so callers fail closed when the primitive is unavailable.

#### Types & Trait Declarations
- **Enums (1):** `AclOutcome`

#### Key Functions & Signatures (9 shown)
```rust
// pub
fn intended_acl_description() -> &'static str;
// pub
fn ensure_private_file_windows(path: &Path) -> Result<AclOutcome, std::io::Error>;
// pub
fn supports_private_files() -> bool;
// private
fn SetNamedSecurityInfoW(object_name: *const u16,
            object_type: u32,
            security_info: Dword,
      ;
// private
fn to_wide(path: &Path) -> Vec<u16>;
// pub
fn restrict_to_owner(path: &Path) -> Result<AclOutcome, std::io::Error>;
// pub
fn _handle_touch(_h: Handle);
// private
fn acl_intent_is_explicit();
// private
fn off_windows_reports_unsupported();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`acl_intent_is_explicit`

---

### `src/platform/windows/conpty.rs` {#src-platform-windows-conpty-rs}

- **Source Link:** [`src/platform/windows/conpty.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/windows/conpty.rs)
- **Lines of Code:** 164 (5056 bytes)

#### Primary Responsibility
Windows Console Pseudo-console (ConPTY) backend surface.  ConPTY is the native terminal facility: a pseudo-console object backs a terminal session with dimensions, input, output, resize, and termination. Raw handle plumbing is Windows-only; capability types and availability reasoning compile everywhere so contract tests stay meaningful.

#### Types & Trait Declarations
- **Structs (2):** `ConsoleSize`, `PseudoConsole`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(cols: u16, rows: u16) -> Self;
// pub
fn valid(&self) -> bool;
// pub
fn conpty_available() -> bool;
// pub
fn terminal_capabilities() -> crate::platform::terminal::TerminalCapabilities;
// private
fn CreatePseudoConsole(size: u32,
            input: *mut std::ffi::c_void,
            output: *mut std::ffi::c_void,
 ;
// private
fn ResizePseudoConsole(console: Hpc, size: u32) -> HResult;
// private
fn ClosePseudoConsole(console: Hpc);
// private
fn pack_size(size: ConsoleSize) -> u32;
// pub
fn conpty_present() -> bool;
// private
fn GetModuleHandleA(name: *const u8) -> *mut std::ffi::c_void;
// private
fn GetProcAddress(module: *mut std::ffi::c_void,
                name: *const u8,) -> *mut std::ffi::c_void;
// pub
fn resize(&self, size: ConsoleSize) -> HResult;
// private
fn drop(&mut self);
// pub
fn _touch_types(_c: ConsoleSize);
// private
fn console_size_validation();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`console_size_validation`

---

### `src/platform/windows/job.rs` {#src-platform-windows-job-rs}

- **Source Link:** [`src/platform/windows/job.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/windows/job.rs)
- **Lines of Code:** 471 (17151 bytes)

#### Primary Responsibility
Windows Job Object backend for process-tree control and limits.  Job Objects are the native execution boundary: every supervised descendant joins the job at spawn time and the whole tree terminates as one unit. Limit mapping is pure and tested on every host; handle management and system calls are confined to `cfg(windows)` so the logic stays reviewable without a Windows runner.

#### Types & Trait Declarations
- **Structs (8):** `FileTime`, `IoCounters`, `JobAttributes`, `JobHandle`, `JobLimitDescription`, `JobObjectBasicLimitInformation`, `JobObjectExtendedLimitInformation`, `ProcessEntry32W`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn describe_job_limits(budget: &ResourceBudget) -> JobLimitDescription;
// pub
fn tree_guarantee() -> &'static str;
// pub
fn create_kill_on_close() -> Result<Self, String>;
// pub
fn create_with_limits(_budget: &ResourceBudget) -> Result<Self, String>;
// pub
fn apply_limits(&self, _budget: &ResourceBudget) -> Result<(), String>;
// pub
fn assign_child(&self, _child: &tokio::process::Child) -> Result<(), String>;
// pub
fn terminate(&self, _exit_code: u32) -> Result<(), String>;
// private
fn CreateJobObjectW(attributes: *const JobAttributes, name: *const u16) -> Handle;
// private
fn SetInformationJobObject(job: Handle,
            info_class: u32,
            info: *const std::ffi::c_void,
        ;
// private
fn AssignProcessToJobObject(job: Handle, process: Handle) -> Bool;
// private
fn TerminateJobObject(job: Handle, exit_code: u32) -> Bool;
// private
fn CloseHandle(object: Handle) -> Bool;
// private
fn GetLastError() -> Dword;
// private
fn GetCurrentProcess() -> Handle;
// pub
fn create_kill_on_close() -> Result<Self, String>;
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`limit_mapping_names_windows_mechanisms`, `empty_budget_maps_to_no_limits`

---

### `src/platform/windows/mod.rs` {#src-platform-windows-mod-rs}

- **Source Link:** [`src/platform/windows/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/windows/mod.rs)
- **Lines of Code:** 147 (4780 bytes)

#### Primary Responsibility
Windows native backend aggregator.  Re-exports the focused Windows mechanisms (process containment via Job Objects, path security, shell backends, credential-file ACLs, ConPTY terminals) and provides the genuine capability probe used on Windows hosts. Pure reasoning compiles everywhere; system bindings stay behind `cfg(windows)`.

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn read_process_starttime(pid: u32) -> Option<u64>;
// pub
fn terminate_process_tree_fallback(pid: u32, exit_code: u32) -> Result<(), String>;
// pub
fn probe_capabilities() -> PlatformCapabilities;
// pub
fn windows_shell_present() -> bool;
// private
fn windows_shell_present_native() -> bool;
// pub
fn process_backend_name() -> &'static str;
// pub
fn shell_backend_name() -> &'static str;
// pub
fn sandbox_backend_name() -> &'static str;
```

---

### `src/platform/windows/path.rs` {#src-platform-windows-path-rs}

- **Source Link:** [`src/platform/windows/path.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/windows/path.rs)
- **Lines of Code:** 274 (9047 bytes)

#### Primary Responsibility
Windows path security: containment without string-prefix traps.  Windows paths admit drive letters, UNC shares, alternate separators, case-insensitive comparison, reserved device names, and reparse-point redirection. Lexical comparison alone cannot establish containment. This module centralizes every check so callers never reimplement prefix logic. All helpers are pure and exercised on every host.

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn is_reserved_name(path: &Path) -> bool;
// pub
fn normalize_separators(input: &str) -> String;
// pub
fn is_unc_path(input: &str) -> bool;
// pub
fn drive_letter(input: &str) -> Option<char>;
// pub
fn is_absolute_windows_path(input: &str) -> bool;
// pub
fn lexical_normalize_windows(input: &str) -> String;
// private
fn components_equal(left: &str, right: &str) -> bool;
// pub
fn is_within_workspace(workspace: &str, candidate: &str) -> bool;
// pub
fn validate_containment(workspace: &Path, candidate: &Path) -> Result<PathBuf, String>;
// pub
fn needs_canonicalization(path: &Path) -> bool;
// pub
fn paths_identical_windows(left: &Path, right: &Path) -> bool;
// pub
fn strip_extended_prefix(path: &str) -> &str;
// private
fn _component_touchstone(p: &Path) -> Vec<Component<'_>>;
// private
fn drive_letter_mismatch_never_contains();
// private
fn prefix_trick_is_rejected();
```

#### Unit Verification (7 inline tests)
Tests defined within module:
`drive_letter_mismatch_never_contains`, `prefix_trick_is_rejected`, `case_insensitive_containment`, `dotdot_escape_is_rejected`, `unc_hosts_must_match`, `reserved_names_rejected`, `separators_unified`

---

### `src/platform/windows/shell.rs` {#src-platform-windows-shell-rs}

- **Source Link:** [`src/platform/windows/shell.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/platform/windows/shell.rs)
- **Lines of Code:** 207 (6403 bytes)

#### Primary Responsibility
Native Windows shell backends.  Direct argument-vector execution is always preferred. Shell-string execution exists only for explicitly authorized steps and resolves the interpreter here so higher layers never embed `cmd.exe` or PowerShell syntax assumptions. Quoting helpers preserve argument boundaries; they are pure and exercised on every host.

#### Types & Trait Declarations
- **Enums (1):** `ShellBackend`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn program(&self) -> &'static str;
// pub
fn wrapper_args(&self) -> &'static [&'static str];
// pub
fn preferred_backend() -> ShellBackend;
// pub
fn is_windows_shell_program(program: &str) -> bool;
// pub
fn contains_cmd_metachars(input: &str) -> bool;
// pub
fn contains_powershell_metachars(input: &str) -> bool;
// pub
fn quote_cmd_arg(arg: &str) -> String;
// pub
fn quote_powershell_arg(arg: &str) -> String;
// pub
fn build_cmd_command(shell_str: &str, cwd: &Path) -> tokio::process::Command;
// pub
fn build_powershell_command(shell_str: &str, cwd: &Path) -> tokio::process::Command;
// pub
fn build_pwsh_command(shell_str: &str, cwd: &Path) -> tokio::process::Command;
// pub
fn argv_preserves_boundaries(args: &[String]) -> bool;
// private
fn cmd_quoting_preserves_spaces_and_metachars();
// private
fn cmd_empty_arg_is_quoted();
// private
fn powershell_single_quotes_escape();
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`cmd_quoting_preserves_spaces_and_metachars`, `cmd_empty_arg_is_quoted`, `powershell_single_quotes_escape`, `shell_detection_covers_known_names`, `shell_backend_pwsh_properties`

---
