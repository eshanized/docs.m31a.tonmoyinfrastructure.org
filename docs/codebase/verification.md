# Verification & Nyquist Gate

> **Architectural Layer:** L7 Verification  
> **Source Directory:** `src/verification`  
> **File Count:** 15 source files  

7-tier verification hierarchy, evidence snapshot matching, and completion gate.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [adapter.rs](#src-verification-adapter-rs) | 285 | `Declared, DeclaredAdapter, ProjectAdapter` | Verification Project Adapter (CFG-01..04).  Provides language and buil... |
| [diagnostician.rs](#src-verification-diagnostician-rs) | 1170 | `DiagnosticHypothesis, DiagnosticReport, DiagnosticianContext` | Tier 7 Model-Based Diagnostician Agent with Fresh Context (D-05, VER-0... |
| [diagnostics.rs](#src-verification-diagnostics-rs) | 527 | `DiagnosticItem, DiagnosticSpan, DiagnosticSeverity` | Structured compiler and linter diagnostics subsystem (Issue 11).  Pars... |
| [executor.rs](#src-verification-executor-rs) | 290 | `ApprovedVerificationCommand` | Governed verification executor (P0-02).  Verification is execution. Ve... |
| [gate.rs](#src-verification-gate-rs) | 1372 | `EvidenceCompletionGate, ToolCapabilityClass` | Evidence-Backed Completion Gate with Cryptographic Snapshot Binding (V... |
| [hierarchy.rs](#src-verification-hierarchy-rs) | 784 | `VerificationHierarchyEngine` | 7-Tier Verification Hierarchy Engine (VER-01, D-01).  Evaluates the ve... |
| [mod.rs](#src-verification-mod-rs) | 42 | `Functions/Traits` | Verification subsystem (VER-01–VER-05).  Provides the 7-tier verificat... |
| [reviewer.rs](#src-verification-reviewer-rs) | 628 | `IndependentReviewer, RawVerdict, ReviewFinding` | Tier 6 Independent Reviewer Agent with Fresh Context &amp; Read-Only S... |
| [compiler.rs](#src-verification-runners-compiler-rs) | 235 | `CompilerRunner` | Tier 2 Compiler &amp; Type Checker Verification Runner (VER-01).  Invo... |
| [deterministic.rs](#src-verification-runners-deterministic-rs) | 157 | `DeterministicRunner` | Tier 1 Deterministic Verification Runner (VER-01).  Validates manifest... |
| [diff_invariants.rs](#src-verification-runners-diff_invariants-rs) | 141 | `DiffInvariantsRunner` | Tier 5 Diff &amp; Invariant Verification Runner (VER-01, VER-03).  Rec... |
| [mod.rs](#src-verification-runners-mod-rs) | 31 | `Functions/Traits` | Verification runner adapters for executing concrete verification tiers... |
| [static_analysis.rs](#src-verification-runners-static_analysis-rs) | 163 | `StaticAnalysisRunner` | Tier 4 Static Analysis &amp; Linter Verification Runner (VER-01, VER-0... |
| [tests.rs](#src-verification-runners-tests-rs) | 271 | `TestRunner` | Tier 3 Automated Test Suite Verification Runner (VER-01, VER-03).  Inv... |
| [types.rs](#src-verification-types-rs) | 619 | `CompilerDiagnosticItem, CompletionGateDecision, FailureEvidence` | Domain types and models for the 7-tier verification hierarchy and comp... |

---

### `src/verification/adapter.rs` {#src-verification-adapter-rs}

- **Source Link:** [`src/verification/adapter.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/verification/adapter.rs)
- **Lines of Code:** 285 (11477 bytes)

#### Primary Responsibility
Verification Project Adapter (CFG-01..04).  Provides language and build system adaptation across: - Rust (`Cargo.toml`, `cargo check`, `cargo test`, `cargo clippy -- -D warnings`) - Python (`pyproject.toml`, `python3 -m py_compile`, `pytest`, `ruff check`) - Node (`package.json`, `npm run build`, `npm test`, `npm run lint`) - Go (`go.mod`, `go vet ./...`, `go test ./...`, `golangci-lint run`) - Custom (explicitly specified in `[workspace.verification]` configuration)

#### Types & Trait Declarations
- **Structs (3):** `Declared`, `DeclaredAdapter`, `ProjectAdapter`
- **Enums (1):** `ProjectType`

#### Key Functions & Signatures (13 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// pub
fn from_str_relaxed(s: &str) -> Option<Self>;
// private
fn default() -> Self;
// private
fn load_declared(project_type: ProjectType) -> Self;
// private
fn parse_declared(project_type: ProjectType, toml_str: &str) -> Result<Self, String>;
// pub
fn adapter_for(project_type: ProjectType) -> Self;
// pub
fn rust_defaults() -> Self;
// pub
fn python_defaults() -> Self;
// pub
fn node_defaults() -> Self;
// pub
fn go_defaults() -> Self;
// pub
fn custom_defaults() -> Self;
// pub
fn detect(workspace_root: &Path,
        verification_config: Option<&WorkspaceVerificationConfig>,
        project_type;
// private
fn test_adapter_auto_detection();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_adapter_auto_detection`

---

### `src/verification/diagnostician.rs` {#src-verification-diagnostician-rs}

- **Source Link:** [`src/verification/diagnostician.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/verification/diagnostician.rs)
- **Lines of Code:** 1170 (43336 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Tier 7 Model-Based Diagnostician Agent with Fresh Context (D-05, VER-01).  Invoked ONLY when earlier tiers or deterministic failure rules produce ambiguous failure output or unresolvable loops. Operates in an isolated agent session with fresh context compiled exclusively from durable error diagnostics and repository evidence, explicitly excluding conversational scratchpads.

#### Types & Trait Declarations
- **Structs (6):** `DiagnosticHypothesis`, `DiagnosticReport`, `DiagnosticianContext`, `ModelDiagnostician`, `RawDiagnosticReport`, `RawHypothesis`
- **Enums (1):** `RecoveryRecommendation`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn parse_model_output(output: &str) -> Result<Self, String>;
// private
fn from(hyp: DiagnosticHypothesis) -> Self;
// private
fn from(rep: DiagnosticReport) -> Self;
// pub
fn parse_model_output(output: &str) -> Result<Self, String>;
// pub
fn new(error_message: impl Into<String>,
        exit_code: Option<i32>,
        stdout_snippet: Option<String>,
       ;
// pub
fn with_task_info(mut self,
        title: impl Into<String>,
        description: impl Into<String>,) -> Self;
// pub
fn with_failure_evidence(mut self, evidence: FailureEvidence) -> Self;
// pub
fn with_recent_diff(mut self, diff: impl Into<String>) -> Self;
// pub
fn with_affected_symbols(mut self, symbols: Vec<String>) -> Self;
// pub
fn with_caller_callee(mut self, neighborhood: Vec<String>) -> Self;
// pub
fn with_attempts(mut self, count: usize, prior: Vec<DiagnosticHypothesis>) -> Self;
// pub
fn compile_prompt(&self,
        catalog: &dyn PromptCatalog,
        compiler: &dyn PromptCompiler,) -> Result<Effectiv;
// pub
fn compile_system_prompt(&self,
        catalog: &dyn PromptCatalog,
        compiler: &dyn PromptCompiler,) -> String;
// pub
fn compile_user_prompt(&self,
        catalog: &dyn PromptCatalog,
        compiler: &dyn PromptCompiler,) -> String;
```

#### Unit Verification (9 inline tests)
Tests defined within module:
`test_diagnostician_read_only_capability_envelope`, `test_fresh_context_compilation_excludes_transcript`, `test_simulated_diagnosis`, `test_diagnostician_prompt_os_compilation`, `test_diagnostic_report_parsing_markdown`, `test_correlate_cascading_compiler_errors_to_root_cause`, `test_baseline_test_failures_vs_regressions`, `test_heuristic_repair_proposal_synthesis`, `test_structured_fix_operation_yields_repair_proposal`

---

### `src/verification/diagnostics.rs` {#src-verification-diagnostics-rs}

- **Source Link:** [`src/verification/diagnostics.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/verification/diagnostics.rs)
- **Lines of Code:** 527 (19232 bytes)

#### Primary Responsibility
Structured compiler and linter diagnostics subsystem (Issue 11).  Parses raw diagnostic streams from Rust, TypeScript/JS, Python, and Go into canonical, strongly-typed diagnostics with source spans, severity, error codes, and suggested replacements.

#### Types & Trait Declarations
- **Structs (2):** `DiagnosticItem`, `DiagnosticSpan`
- **Enums (1):** `DiagnosticSeverity`

#### Key Functions & Signatures (8 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn render_for_prompt(&self) -> String;
// pub
fn parse_rust_diagnostics(output: &str) -> Vec<DiagnosticItem>;
// private
fn parse_cargo_json_message(msg: &serde_json::Value) -> Option<DiagnosticItem>;
// pub
fn parse_typescript_diagnostics(output: &str) -> Vec<DiagnosticItem>;
// pub
fn parse_python_diagnostics(output: &str) -> Vec<DiagnosticItem>;
// pub
fn parse_go_diagnostics(output: &str) -> Vec<DiagnosticItem>;
// pub
fn parse_diagnostics(output: &str, language_hint: Option<&str>) -> Vec<DiagnosticItem>;
```

---

### `src/verification/executor.rs` {#src-verification-executor-rs}

- **Source Link:** [`src/verification/executor.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/verification/executor.rs)
- **Lines of Code:** 290 (11472 bytes)
- **Runtime Properties:** 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Governed verification executor (P0-02).  Verification is execution. Verification commands (compiler / test / linter strings, project-adapter overrides, `AutomatedTest&#123;command&#125;`) must therefore pass through the SAME authoritative execution boundary as every other child process — never a parallel direct-spawn path.  Conceptual flow enforced here:  ```text verification configuration → argv parsing + shell-metachar rejection (no shell is ever invoked) → check_command_safety (protected paths, git redirection) → validate_working_directory (workspace containment, symlink-safe) → sanitized EnvironmentBuilder (env_clear; no secrets, no loaders) → ProcessSupervisor::run_supervised (process-group isolation, timeout, cancellation) → verification result (parsed by the calling runner) ```  There is exactly ONE authoritative execution boundary (`ProcessSupervisor` + `EnvironmentBuilder` + `ProcessTreeController`). This module contains no second copy of that logic; it only validates verification-specific configuration and delegates execution.

#### Types & Trait Declarations
- **Structs (1):** `ApprovedVerificationCommand`

#### Key Functions & Signatures (11 shown)
```rust
// pub
fn program(&self) -> &str;
// pub
fn args(&self) -> &[String];
// pub
fn approve_verification_command(command: &str,
    workspace_root: &Path,
    extra_env: Vec<(String, String);
// pub
async fn execute_approved(approved: &ApprovedVerificationCommand,
    timeout: Duration,
    cancellation: Option<&Cance;
// pub
async fn execute_governed_verification(command: &str,
    workspace_root: &Path,
    timeout: Duration,
    extra_env: V;
// private
fn ws() -> std::path::PathBuf;
// private
fn shell_injection_rejected();
// private
fn workspace_escape_rejected();
// private
fn worktree_roots_under_m31a_approve();
// private
fn credential_env_rejected();
// private
fn benign_extra_env_approved();
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`shell_injection_rejected`, `workspace_escape_rejected`, `worktree_roots_under_m31a_approve`, `credential_env_rejected`, `benign_extra_env_approved`

---

### `src/verification/gate.rs` {#src-verification-gate-rs}

- **Source Link:** [`src/verification/gate.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/verification/gate.rs)
- **Lines of Code:** 1372 (51776 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
Evidence-Backed Completion Gate with Cryptographic Snapshot Binding (VER-04, VER-05, D-04, Law 6).  Enforces Law 6 ("The model proposes. The runtime decides."): No task or mission may transition to Succeeded on model self-report alone. The runtime independently queries SQLite verification_checks and requirement_check_coverage, verifies external artifact existence and SHA-256 hashes in FsArtifactStore, confirms that the workspace snapshot matches the verified baseline, and persists authoritative completion gate decisions.  Canonical `ToolCapabilityClass` replaces scattered literal tool-name matching with capability-based classification.

#### Types & Trait Declarations
- **Structs (1):** `EvidenceCompletionGate`
- **Enums (1):** `ToolCapabilityClass`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn extract_json_path_candidates(val: &serde_json::Value, out: &mut Vec<String>);
// pub
fn classify(tool_name: &str) -> Self;
// pub
fn is_mutation(&self) -> bool;
// pub
fn is_verification(&self) -> bool;
// pub
fn extract_mutation_paths(tool_name: &str, params: &serde_json::Value) -> Vec<String>;
// pub
fn new(pool: SqlitePool,
        artifact_store: Arc<dyn ArtifactStore>,
        workspace_root: impl Into<PathBuf>,) ->;
// pub
fn with_hierarchy_engine(mut self,
        hierarchy: Arc<crate::verification::hierarchy::VerificationHierarchyEngine>,);
// pub
async fn evaluate_task_completion(&self,
        mission_id: MissionId,
        task_id: TaskId,
        current_snapsho;
// pub
async fn evaluate_session_completion(&self,
        session_id: SessionId,
        turns: &[crate::interaction::session:;
// pub
async fn evaluate_session_completion_with_intent(&self,
        session_id: SessionId,
        turns: &[crate::interacti;
// pub
async fn evaluate_mission_completion(&self,
        mission_id: MissionId,
        current_snapshot_hash: &str,) -> Resu;
// pub
fn capture_current_snapshot_hash(&self,
        mission_id: MissionId,
        task_id: Option<TaskId>,) -> Result<Strin;
// pub
async fn list_check_ids_for_mission(pool: &SqlitePool,
        mission_id: MissionId,) -> Result<Vec<CheckId>, sqlx::Err;
// pub
async fn get_check_by_id(&self,
        check_id: CheckId,) -> Result<Option<VerificationCheck>, sqlx::Error>;
// pub
async fn list_all_checks(&self) -> Result<Vec<VerificationCheck>, sqlx::Error>;
```

---

### `src/verification/hierarchy.rs` {#src-verification-hierarchy-rs}

- **Source Link:** [`src/verification/hierarchy.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/verification/hierarchy.rs)
- **Lines of Code:** 784 (29517 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
7-Tier Verification Hierarchy Engine (VER-01, D-01).  Evaluates the verification hierarchy as a gated dependency graph: Tier 1 (Deterministic) -&gt; Tier 2 (Compiler) -&gt; Tier 3 (Tests) / Tier 4 (Static Analysis) -&gt; Tier 5 (Diff/Invariants) -&gt; Tier 6 (Independent Review) -&gt; Tier 7 (Model Diagnosis).  Enforces fail-fast gating: failure in an earlier tier (e.g. Tier 2 Compiler) immediately blocks downstream dependent tiers (Tiers 3, 4, 6) from executing, eliminating token and time waste.

#### Types & Trait Declarations
- **Structs (1):** `VerificationHierarchyEngine`

#### Key Functions & Signatures (8 shown)
```rust
// private
fn default() -> Self;
// pub
fn production() -> Self;
// pub
fn for_workspace(workspace_root: &Path,
        verification_config: Option<&crate::config::WorkspaceVerificationConfig>;
// pub
fn for_workspace_with_config(workspace_root: &Path,
        config: &crate::config::ResolvedConfiguration,) -> Self;
// pub
fn new(tier1: Arc<dyn VerificationRunner>,
        tier2: Arc<dyn VerificationRunner>,
        tier3: Arc<dyn Verificati;
// pub
async fn execute_hierarchy(&self,
        mission_id: MissionId,
        task_id: TaskId,
        workspace_root: &Path,;
// pub
async fn execute_hierarchy_for_task(&self,
        mission_id: MissionId,
        task_id: TaskId,
        workspace_roo;
// pub
async fn evaluate_strategy(&self,
        mission_id: MissionId,
        task_id: TaskId,
        workspace_root: &Path,;
```

---

### `src/verification/mod.rs` {#src-verification-mod-rs}

- **Source Link:** [`src/verification/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/verification/mod.rs)
- **Lines of Code:** 42 (1472 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Verification subsystem (VER-01–VER-05).  Provides the 7-tier verification hierarchy engine, concrete runner adapters, Tier 6 independent reviewer agent with fresh-context read-only isolation, and evidence-backed completion gate with cryptographic snapshot binding.

---

### `src/verification/reviewer.rs` {#src-verification-reviewer-rs}

- **Source Link:** [`src/verification/reviewer.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/verification/reviewer.rs)
- **Lines of Code:** 628 (23495 bytes)
- **Runtime Properties:** 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Tier 6 Independent Reviewer Agent with Fresh Context &amp; Read-Only Sandbox (VER-02, VER-03, D-02, D-03).  Executes an isolated review agent under a strict `CapabilityEnvelope::read_only` policy. Compiles prompts exclusively from authoritative durable state (requirements, diff, test results), explicitly excluding implementer transcripts, thoughts, and conversational scratchpads. Emits a typed `ReviewVerdict` mapped to runtime `VerificationCheck`.

#### Types & Trait Declarations
- **Structs (5):** `IndependentReviewer`, `RawVerdict`, `ReviewFinding`, `ReviewVerdict`, `ReviewerAgentContext`
- **Enums (3):** `ReviewDecision`, `ReviewFindingSeverity`, `ReviewerExecutionError`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(task_title: impl Into<String>,
        task_description: impl Into<String>,
        acceptance_criteria: Vec<Stri;
// pub
fn compile_prompt(&self,
        catalog: &dyn PromptCatalog,
        compiler: &dyn PromptCompiler,) -> Result<Effectiv;
// pub
fn compile_system_prompt(&self,
        catalog: &dyn PromptCatalog,
        compiler: &dyn PromptCompiler,) -> String;
// pub
fn compile_user_prompt(&self,
        catalog: &dyn PromptCatalog,
        compiler: &dyn PromptCompiler,) -> String;
// pub
fn is_fresh_context(&self) -> bool;
// pub
fn parse_model_output(output: &str,
        mission_id: MissionId,
        task_id: TaskId,
        snapshot_hash: &str,;
// pub(crate)
fn extract_json_payload(raw: &str) -> &str;
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_catalog(mut self, catalog: Arc<dyn PromptCatalog>) -> Self;
// pub
fn with_compiler(mut self, compiler: Arc<dyn PromptCompiler>) -> Self;
// pub
fn with_model_caller(mut self, caller: Arc<dyn ModelCaller>) -> Self;
// pub
fn with_simulated_verdict(mut self, verdict: ReviewVerdict) -> Self;
// pub
fn with_simulated_error(mut self, err: ReviewerExecutionError) -> Self;
// pub
fn evaluate_risk_mandate(is_mission_completion: bool,
        is_security_or_architecture: bool,
        modifies_critic;
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_reviewer_read_only_capability_envelope`, `test_reviewer_risk_mandate_evaluation`, `test_fresh_context_compilation_excludes_transcript`

---

### `src/verification/runners/compiler.rs` {#src-verification-runners-compiler-rs}

- **Source Link:** [`src/verification/runners/compiler.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/verification/runners/compiler.rs)
- **Lines of Code:** 235 (8654 bytes)

#### Primary Responsibility
Tier 2 Compiler &amp; Type Checker Verification Runner (VER-01).  Invokes compiler diagnostics (`cargo check`), parses `rustc` error codes (`error[E0...]`), and reports structured compilation outcomes.

#### Types & Trait Declarations
- **Structs (1):** `CompilerRunner`

#### Key Functions & Signatures (9 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_timeout_secs(mut self, secs: u64) -> Self;
// pub
fn with_command(cmd: impl Into<String>) -> Self;
// pub
fn with_simulated(exit_code: i32,
        stdout: impl Into<String>,
        stderr: impl Into<String>,) -> Self;
// pub
fn parse_compiler_output(exit_code: i32,
        stdout: &str,
        stderr: &str,) -> (CheckStatus, Vec<String>, Stri;
// private
async fn execute(&self,
        mission_id: MissionId,
        task_id: TaskId,
        workspace_root: &Path,
        s;
// private
fn test_parse_compiler_output_success();
// private
fn test_parse_compiler_output_rustc_error();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_parse_compiler_output_success`, `test_parse_compiler_output_rustc_error`

---

### `src/verification/runners/deterministic.rs` {#src-verification-runners-deterministic-rs}

- **Source Link:** [`src/verification/runners/deterministic.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/verification/runners/deterministic.rs)
- **Lines of Code:** 157 (4697 bytes)

#### Primary Responsibility
Tier 1 Deterministic Verification Runner (VER-01).  Validates manifest file existence (`Cargo.toml`), workspace structure (`src/`), and deterministic format/syntax invariants without spending compiler or model tokens.

#### Types & Trait Declarations
- **Structs (1):** `DeterministicRunner`

#### Key Functions & Signatures (7 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_manifest(manifest: impl Into<String>) -> Self;
// pub
fn with_manifest_and_source(manifest: impl Into<String>,
        source_dir: Option<String>,) -> Self;
// private
async fn execute(&self,
        mission_id: MissionId,
        task_id: TaskId,
        workspace_root: &Path,
        s;
// private
async fn test_deterministic_runner_success();
// private
async fn test_deterministic_runner_missing_manifest();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_deterministic_runner_success`, `test_deterministic_runner_missing_manifest`

---

### `src/verification/runners/diff_invariants.rs` {#src-verification-runners-diff_invariants-rs}

- **Source Link:** [`src/verification/runners/diff_invariants.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/verification/runners/diff_invariants.rs)
- **Lines of Code:** 141 (5073 bytes)

#### Primary Responsibility
Tier 5 Diff &amp; Invariant Verification Runner (VER-01, VER-03).  Reconciles workspace state against `RepositoryBaseline` using `repo::drift::detect_drift`, enforcing authorized mutation scopes and preventing unexpected workspace drift.

#### Types & Trait Declarations
- **Structs (1):** `DiffInvariantsRunner`

#### Key Functions & Signatures (5 shown)
```rust
// pub
fn new() -> Self;
// pub
fn with_baseline(mut self, baseline: RepositoryBaseline) -> Self;
// pub
fn with_authorized_mutations(mut self,
        mutations: impl IntoIterator<Item = String>,) -> Self;
// pub
fn with_simulated(mut self, status: CheckStatus, summary: impl Into<String>) -> Self;
// private
async fn execute(&self,
        mission_id: MissionId,
        task_id: TaskId,
        workspace_root: &Path,
        s;
```

---

### `src/verification/runners/mod.rs` {#src-verification-runners-mod-rs}

- **Source Link:** [`src/verification/runners/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/verification/runners/mod.rs)
- **Lines of Code:** 31 (882 bytes)

#### Primary Responsibility
Verification runner adapters for executing concrete verification tiers (VER-01, VER-03).

#### Types & Trait Declarations
- **Traits (1):** `VerificationRunner`

#### Key Functions & Signatures (1 shown)
```rust
// private
async fn execute(&self,
        mission_id: MissionId,
        task_id: TaskId,
        workspace_root: &Path,
        s;
```

---

### `src/verification/runners/static_analysis.rs` {#src-verification-runners-static_analysis-rs}

- **Source Link:** [`src/verification/runners/static_analysis.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/verification/runners/static_analysis.rs)
- **Lines of Code:** 163 (5557 bytes)

#### Primary Responsibility
Tier 4 Static Analysis &amp; Linter Verification Runner (VER-01, VER-03).  Invokes linter diagnostics (`cargo clippy -- -D warnings`), parses warnings and errors, and reports static analysis compliance.

#### Types & Trait Declarations
- **Structs (1):** `StaticAnalysisRunner`

#### Key Functions & Signatures (6 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_command(cmd: impl Into<String>) -> Self;
// pub
fn with_simulated(exit_code: i32,
        stdout: impl Into<String>,
        stderr: impl Into<String>,) -> Self;
// pub
fn parse_linter_output(exit_code: i32,
        _stdout: &str,
        stderr: &str,) -> (CheckStatus, String);
// private
async fn execute(&self,
        mission_id: MissionId,
        task_id: TaskId,
        workspace_root: &Path,
        s;
```

---

### `src/verification/runners/tests.rs` {#src-verification-runners-tests-rs}

- **Source Link:** [`src/verification/runners/tests.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/verification/runners/tests.rs)
- **Lines of Code:** 271 (10050 bytes)

#### Primary Responsibility
Tier 3 Automated Test Suite Verification Runner (VER-01, VER-03).  Invokes automated test commands (`cargo test`), parses test failures, panics, and assertion outcomes, and stores evidence in `ArtifactStore`.

#### Types & Trait Declarations
- **Structs (1):** `TestRunner`

#### Key Functions & Signatures (10 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_timeout_secs(mut self, secs: u64) -> Self;
// pub
fn with_artifact_store(mut self, store: Arc<dyn ArtifactStore>) -> Self;
// pub
fn with_command(mut self, cmd: impl Into<String>) -> Self;
// pub
fn with_simulated(mut self,
        exit_code: i32,
        stdout: impl Into<String>,
        stderr: impl Into<String>;
// pub
fn parse_test_output(exit_code: i32,
        stdout: &str,
        stderr: &str,) -> (CheckStatus, Vec<String>, String);
// private
async fn execute(&self,
        mission_id: MissionId,
        task_id: TaskId,
        workspace_root: &Path,
        s;
// private
fn test_parse_test_output_passed();
// private
fn test_parse_test_output_failed();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_parse_test_output_passed`, `test_parse_test_output_failed`

---

### `src/verification/types.rs` {#src-verification-types-rs}

- **Source Link:** [`src/verification/types.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/verification/types.rs)
- **Lines of Code:** 619 (19077 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Domain types and models for the 7-tier verification hierarchy and completion gate (VER-01, VER-04, D-01, D-04).

#### Types & Trait Declarations
- **Structs (6):** `CompilerDiagnosticItem`, `CompletionGateDecision`, `FailureEvidence`, `RequirementCheckCoverage`, `TestFailureItem`, `VerificationCheck`
- **Enums (3):** `CheckStatus`, `CheckTier`, `EvidenceEpistemicStatus`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn as_u8(&self) -> u8;
// pub
fn from_u8(val: u8) -> Option<Self>;
// pub
fn name(&self) -> &'static str;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// pub
fn is_passed(&self) -> bool;
// pub
fn is_failed(&self) -> bool;
// pub
fn is_blocked(&self) -> bool;
// pub
fn is_not_applicable(&self) -> bool;
// pub
fn as_str(&self) -> &'static str;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn new(mission_id: MissionId,
        task_id: TaskId,
        tier: CheckTier,
        status: CheckStatus,
        com;
// pub
fn passed(mission_id: MissionId,
        task_id: TaskId,
        tier: CheckTier,
        command_or_tool: impl Into<St;
// pub
fn failed(mission_id: MissionId,
        task_id: TaskId,
        tier: CheckTier,
        command_or_tool: impl Into<St;
// pub
fn blocked(mission_id: MissionId,
        task_id: TaskId,
        tier: CheckTier,
        snapshot_hash: impl Into<Str;
```

---
