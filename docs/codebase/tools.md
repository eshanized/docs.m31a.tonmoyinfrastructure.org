# Model Tools & Catalog

> **Architectural Layer:** L2 Tools  
> **Source Directory:** `src/tools`  
> **File Count:** 18 source files  

Central catalog of 28 core tools and extended tools (fs, git, qa, repo, web, etc.).

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [agent.rs](#src-tools-agent-rs) | 142 | `DelegateTaskInput, DelegateTaskOutput, DelegateTaskTool` | Multi-agent delegation model-facing tool (Issue 13). |
| [mod.rs](#src-tools-artifact-mod-rs) | 142 | `CreateArtifactInput, CreateArtifactOutput, CreateArtifactTool` | Immutable artifact storage model-facing tools (TL-02, D-07). |
| [definition.rs](#src-tools-definition-rs) | 428 | `AdaptStrategyInput, AdaptStrategyOutput, AdaptStrategyTool` | Typed tool contracts, AnyTool object-safe adapter, and wire schema gen... |
| [error.rs](#src-tools-error-rs) | 133 | `ToolError` | Strongly typed tool execution error contract (TL-04, D-10). |
| [filter.rs](#src-tools-filter-rs) | 515 | `FilterCriteria, ToolAuthorityScope, ToolFilter` | Deterministic multi-stage model-visible tool filtering and pruning (TL... |
| [editor.rs](#src-tools-fs-editor-rs) | 957 | `EditSuccess, RobustFileEditor, EditDiagnostic` | Robust file editing primitive supporting line-range replacement, struc... |
| [mod.rs](#src-tools-fs-mod-rs) | 1623 | `ApplyPatchInput, ApplyPatchOutput, ApplyPatchTool` | Filesystem model-facing tools consuming FileSystemService (TL-02, D-07... |
| [workspace_patch.rs](#src-tools-fs-workspace_patch-rs) | 686 | `PatchHunk, WorkspacePatchEngine, WorkspacePatchReport` | Multi-file workspace diff and patch application engine (Issue 14).  Pa... |
| [mod.rs](#src-tools-git-mod-rs) | 762 | `GitAddInput, GitAddOutput, GitAddTool` | Git version control model-facing tools consuming GitService (TL-02, D-... |
| [mod.rs](#src-tools-mod-rs) | 44 | `Functions/Traits` | Core model-facing tools, typed schemas, and filtering subsystem.  TL-0... |
| [mod.rs](#src-tools-process-mod-rs) | 334 | `JobOutputInput, JobOutputTool, JobStatusInput` | Process and background job model-facing tools (TL-02, D-07, D-13). |
| [mod.rs](#src-tools-qa-mod-rs) | 412 | `FlexibleVecVisitor, RunFormatterInput, RunFormatterTool` | Quality assurance and verification model-facing tools (TL-02, D-07). |
| [registry.rs](#src-tools-registry-rs) | 201 | `ToolRegistry` | Central tool catalog registry managing model-facing tools (TL-02, D-07... |
| [mod.rs](#src-tools-repo-mod-rs) | 573 | `LspFindReferencesInput, LspFindReferencesOutput, LspFindReferencesTool` | Repository intelligence model-facing tools consuming RepositoryService... |
| [risk.rs](#src-tools-risk-rs) | 294 | `EffectiveRisk, RiskClass` | Baseline risk classification and dynamic effective risk evaluation (TL... |
| [skill.rs](#src-tools-skill-rs) | 153 | `SkillSummaryDto, SkillsInspectInput, SkillsInspectOutput` | Model-available specialized skills tools consuming SkillRegistry. |
| [terminal.rs](#src-tools-terminal-rs) | 398 | `TerminalReadStreamInput, TerminalReadStreamOutput, TerminalReadStreamTool` | Terminal session model-facing tools (CTL-01, CTL-02, TL-02). |
| [web.rs](#src-tools-web-rs) | 151 | `WebFetchInput, WebFetchOutput, WebFetchTool` | Web search and URL fetching tools (CTL-02, PRD §04). |

---

### `src/tools/agent.rs` {#src-tools-agent-rs}

- **Source Link:** [`src/tools/agent.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/agent.rs)
- **Lines of Code:** 142 (5050 bytes)

#### Primary Responsibility
Multi-agent delegation model-facing tool (Issue 13).

#### Types & Trait Declarations
- **Structs (3):** `DelegateTaskInput`, `DelegateTaskOutput`, `DelegateTaskTool`

#### Key Functions & Signatures (6 shown)
```rust
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
```

---

### `src/tools/artifact/mod.rs` {#src-tools-artifact-mod-rs}

- **Source Link:** [`src/tools/artifact/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/artifact/mod.rs)
- **Lines of Code:** 142 (4063 bytes)

#### Primary Responsibility
Immutable artifact storage model-facing tools (TL-02, D-07).

#### Types & Trait Declarations
- **Structs (6):** `CreateArtifactInput`, `CreateArtifactOutput`, `CreateArtifactTool`, `ReadArtifactInput`, `ReadArtifactOutput`, `ReadArtifactTool`

#### Key Functions & Signatures (13 shown)
```rust
// private
fn get_artifacts(ctx: &ToolExecutionContext) -> Result<Arc<dyn ArtifactStoreService>, ToolError>;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
```

---

### `src/tools/definition.rs` {#src-tools-definition-rs}

- **Source Link:** [`src/tools/definition.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/definition.rs)
- **Lines of Code:** 428 (13713 bytes)
- **Runtime Properties:** 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Typed tool contracts, AnyTool object-safe adapter, and wire schema generator (TL-01, D-05).

#### Types & Trait Declarations
- **Structs (9):** `AdaptStrategyInput`, `AdaptStrategyOutput`, `AdaptStrategyTool`, `CompleteInput`, `CompleteOutput`, `CompleteTool`, `ResourceLimits`, `ToolAdapter`, `ToolExecutionContext`
- **Traits (2):** `AnyTool`, `TypedTool`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn new(timeout_secs: u64, max_output_bytes: usize) -> Self;
// pub
fn effective(declared: &ResourceLimits,
        _configured: &crate::config::ResourcesConfig,) -> ResourceLimits;
// pub
fn effective_default(configured: &crate::config::ResourcesConfig) -> ResourceLimits;
// pub
fn new(capability_registry: Arc<CapabilityRegistry>,
        workspace_root: PathBuf,
        cancellation_token: Cancel;
// pub
fn with_role_envelope(mut self, envelope: CapabilityEnvelope) -> Self;
// pub
fn with_mission_id(mut self, mission_id: MissionId) -> Self;
// pub
fn with_task_id(mut self, task_id: TaskId) -> Self;
// pub
fn with_agent_id(mut self, agent_id: AgentId) -> Self;
// pub
fn with_agent_role(mut self, role: crate::state_machine::agent::AgentRole) -> Self;
// pub
fn with_autonomy_mode(mut self, mode: crate::state_machine::AutonomyMode) -> Self;
// pub
fn with_policy_hash(mut self, hash: impl Into<String>) -> Self;
// pub
fn with_task_repo(mut self,
        repo: crate::persistence::sqlite::repositories::SqliteTaskRepository,) -> Self;
// pub
fn with_wait_for_approval(mut self, wait: bool) -> Self;
// private
fn id(&self) -> &str;
```

---

### `src/tools/error.rs` {#src-tools-error-rs}

- **Source Link:** [`src/tools/error.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/error.rs)
- **Lines of Code:** 133 (4035 bytes)

#### Primary Responsibility
Strongly typed tool execution error contract (TL-04, D-10).

#### Types & Trait Declarations
- **Enums (1):** `ToolError`

#### Key Functions & Signatures (7 shown)
```rust
// pub
fn validation(message: impl Into<String>, hint: Option<String>) -> Self;
// pub
fn resource_not_found(resource: impl Into<String>, hint: Option<String>) -> Self;
// pub
fn precondition_failed(message: impl Into<String>, hint: Option<String>) -> Self;
// pub
fn permission_denied(message: impl Into<String>, hint: Option<String>) -> Self;
// pub
fn execution_failed(message: impl Into<String>,
        exit_code: Option<i32>,
        hint: Option<String>,) -> Self;
// pub
fn capability_unavailable(family: impl Into<String>, hint: Option<String>) -> Self;
// private
fn from(err: CapabilityError) -> Self;
```

---

### `src/tools/filter.rs` {#src-tools-filter-rs}

- **Source Link:** [`src/tools/filter.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/filter.rs)
- **Lines of Code:** 515 (18094 bytes)
- **Runtime Properties:** 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Deterministic multi-stage model-visible tool filtering and pruning (TL-05, D-06).

#### Types & Trait Declarations
- **Structs (3):** `FilterCriteria`, `ToolAuthorityScope`, `ToolFilter`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(capability_registry: Arc<CapabilityRegistry>) -> Self;
// pub
fn with_role_envelope(mut self, envelope: &'a CapabilityEnvelope) -> Self;
// pub
fn with_task_requirements(mut self, requirements: &'a [CapabilityRequirement]) -> Self;
// pub
fn with_autonomy_mode(mut self, mode: AutonomyMode) -> Self;
// pub
fn with_denied_tools(mut self,
        denied: impl IntoIterator<Item = impl Into<String>>,) -> Self;
// pub
fn with_context_budget(mut self, bytes: usize) -> Self;
// pub
fn new(registry: Arc<ToolRegistry>) -> Self;
// pub
fn filter_tools(&self, criteria: &FilterCriteria) -> Vec<Arc<dyn AnyTool>>;
// pub
fn filter_to_wire_format(&self, criteria: &FilterCriteria) -> Vec<serde_json::Value>;
// private
fn tool_allowed_by_envelope(tool: &dyn AnyTool, envelope: &CapabilityEnvelope) -> bool;
// private
fn tool_satisfies_task_requirements(tool: &dyn AnyTool,
    requirements: &[CapabilityRequirement],) -> bool;
// private
fn match_tool_to_cap_pattern(tool: &dyn AnyTool, pattern: &str) -> bool;
// private
fn match_suffix(suffix: &str, is_mutating: bool, tool: &dyn AnyTool) -> bool;
// private
fn family_names(fam: &CapabilityFamily) -> &'static [&'static str];
// pub
fn new(role: crate::state_machine::agent::AgentRole,
        capability_registry: Arc<CapabilityRegistry>,
        tool_;
```

---

### `src/tools/fs/editor.rs` {#src-tools-fs-editor-rs}

- **Source Link:** [`src/tools/fs/editor.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/fs/editor.rs)
- **Lines of Code:** 957 (34879 bytes)

#### Primary Responsibility
Robust file editing primitive supporting line-range replacement, structured diffs, safe insertion/deletion, and ambiguous match rejection (P3-A, AGENTS.md Rule 5 &amp; 6).

#### Types & Trait Declarations
- **Structs (2):** `EditSuccess`, `RobustFileEditor`
- **Enums (3):** `EditDiagnostic`, `EditMode`, `FileEditOp`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn detect_line_ending(content: &str) -> &'static str;
// pub
fn apply(original: &str, op: &FileEditOp) -> Result<EditSuccess, EditDiagnostic>;
// pub
fn normalize_escapes(s: &str) -> String;
// private
fn apply_substring(original: &str,
        old_content: &str,
        new_content: &str,) -> Result<EditSuccess, EditDia;
// pub
fn apply_line_range(original: &str,
        start_line: usize,
        end_line: usize,
        new_content: &str,
     ;
// pub
fn apply_insertion(original: &str,
        line_number: usize,
        content: &str,
        after: bool,) -> Result<Ed;
// pub
fn apply_deletion(original: &str,
        start_line: usize,
        end_line: usize,
        expected_old: Option<&str>;
// pub
fn apply_unified_diff(original: &str, patch: &str) -> Result<EditSuccess, EditDiagnostic>;
// private
fn check_shrinkage(original: &str, new_content: &str) -> Result<(), EditDiagnostic>;
// private
fn leading_indent(line: &str) -> &str;
// private
fn find_line_trimmed_matches(orig_lines: &[&str], target_lines: &[&str]) -> Vec<usize>;
// private
fn find_nearest_slice(orig_lines: &[&str], target_lines: &[&str]) -> Option<(usize, usize)>;
// private
fn line_similarity(a: &str, b: &str) -> usize;
// private
fn test_unique_trimmed_line_match_when_substring_appears_multiple_times();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_unique_trimmed_line_match_when_substring_appears_multiple_times`

---

### `src/tools/fs/mod.rs` {#src-tools-fs-mod-rs}

- **Source Link:** [`src/tools/fs/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/fs/mod.rs)
- **Lines of Code:** 1623 (52985 bytes)
- **Runtime Properties:** 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Filesystem model-facing tools consuming FileSystemService (TL-02, D-07).

#### Types & Trait Declarations
- **Structs (41):** `ApplyPatchInput`, `ApplyPatchOutput`, `ApplyPatchTool`, `ApplyWorkspacePatchInput`, `ApplyWorkspacePatchOutput`, `ApplyWorkspacePatchTool`, `CopyFileInput`, `CopyFileOutput`, `CopyFileTool`, `CreateDirectoryInput`, `CreateDirectoryOutput`, `CreateDirectoryTool`, `DeleteFileInput`, `DeleteFileOutput`, `DeleteFileTool`, `EditFileInput`, `EditFileOutput`, `EditFileTool`, `FlexibleUsizeVisitor`, `GlobInput`, `GlobOutput`, `GlobTool`, `GrepInput`, `GrepMatch`, `GrepOutput`, `GrepTool`, `ListFilesInput`, `ListFilesOutput`, `ListFilesTool`, `MoveFileInput`, `MoveFileOutput`, `MoveFileTool`, `ReadFileInput`, `ReadFileOutput`, `ReadFileTool`, `RenameFileInput`, `RenameFileOutput`, `RenameFileTool`, `WriteFileInput`, `WriteFileOutput`, `WriteFileTool`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn get_fs(ctx: &ToolExecutionContext) -> Result<Arc<dyn FileSystemService>, ToolError>;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
// pub(crate)
fn normalize_file_content(path: &str, content: &str) -> String;
// pub(crate)
fn normalize_edit_content(_path: &str, content: &str) -> String;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
```

#### Unit Verification (7 inline tests)
Tests defined within module:
`test_write_file_new_file_succeeds`, `test_write_file_preserves_whitespace_fidelity`, `test_write_file_catastrophic_shrinkage_rejected`, `test_write_file_normal_update_succeeds`, `test_edit_file_success`, `test_edit_file_old_content_empty_rejected`, `test_edit_file_not_found_returns_clear_error`

---

### `src/tools/fs/workspace_patch.rs` {#src-tools-fs-workspace_patch-rs}

- **Source Link:** [`src/tools/fs/workspace_patch.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/fs/workspace_patch.rs)
- **Lines of Code:** 686 (25627 bytes)

#### Primary Responsibility
Multi-file workspace diff and patch application engine (Issue 14).  Parses and safely applies multi-file unified git diffs, supporting file creation, file deletion, renames, and modifications with dry-run atomicity and whitespace tolerance.

#### Types & Trait Declarations
- **Structs (3):** `PatchHunk`, `WorkspacePatchEngine`, `WorkspacePatchReport`
- **Enums (3):** `FilePatchAction`, `PatchDiagnostic`, `RollbackOp`

#### Key Functions & Signatures (11 shown)
```rust
// pub
fn parse(diff: &str) -> Result<Vec<FilePatchAction>, PatchDiagnostic>;
// private
fn parse_hunk(lines: &[&str], i: &mut usize) -> Result<PatchHunk, PatchDiagnostic>;
// pub
async fn test_applicable(fs: &dyn FileSystemService,
        actions: &[FilePatchAction],) -> Result<Vec<(String, Option;
// pub
async fn apply_workspace_patch(fs: &dyn FileSystemService,
        patch: &str,) -> Result<WorkspacePatchReport, PatchDi;
// private
async fn execute_rollback(fs: &dyn FileSystemService, rollbacks: Vec<RollbackOp>);
// private
fn apply_hunks(original: &str,
        file_path: &str,
        hunks: &[PatchHunk],) -> Result<String, PatchDiagnostic>;
// private
fn clean_diff_path(raw: &str) -> String;
// private
fn parse_range(range_str: &str) -> (usize, usize);
// private
fn find_hunk_position(haystack: &[&str],
    needle: &[&str],
    search_start: usize,
    expected_start: usize,) -> Op;
// private
fn test_parse_multi_file_patch();
// private
fn main();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_parse_multi_file_patch`

---

### `src/tools/git/mod.rs` {#src-tools-git-mod-rs}

- **Source Link:** [`src/tools/git/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/git/mod.rs)
- **Lines of Code:** 762 (20351 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Git version control model-facing tools consuming GitService (TL-02, D-07).

#### Types & Trait Declarations
- **Structs (34):** `GitAddInput`, `GitAddOutput`, `GitAddTool`, `GitBranchInput`, `GitBranchTool`, `GitCheckoutInput`, `GitCheckoutOutput`, `GitCheckoutTool`, `GitCommitInput`, `GitCommitOutput`, `GitCommitTool`, `GitDiffInput`, `GitDiffOutput`, `GitDiffTool`, `GitLogInput`, `GitLogOutput`, `GitLogTool`, `GitShowInput`, `GitShowOutput`, `GitShowTool`, `GitStatusInput`, `GitStatusTool`, `PrCommentInput`, `PrCommentOutput`, `PrCommentTool`, `PrCreateInput`, `PrCreateOutput`, `PrCreateTool`, `PrListChecksInput`, `PrListChecksOutput`, `PrListChecksTool`, `PrStatusInput`, `PrStatusOutput`, `PrStatusTool`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn get_git(ctx: &ToolExecutionContext) -> Result<Arc<dyn GitService>, ToolError>;
// private
fn pipeline_git_gate(ctx: &ToolExecutionContext,
    tool_id: &str,
    op: crate::git::GitOperation,
    additional: Ve;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        _input: Self::Input,) -> Result<Self::Output, ToolEr;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
// private
fn id(&self) -> &str;
```

---

### `src/tools/mod.rs` {#src-tools-mod-rs}

- **Source Link:** [`src/tools/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/mod.rs)
- **Lines of Code:** 44 (1647 bytes)

#### Primary Responsibility
Core model-facing tools, typed schemas, and filtering subsystem.  TL-01: Strongly typed tool definitions and derived JSON schemas. TL-02: 28 core model-facing tools across 6 functional domains. TL-05: Multi-stage deterministic model-visible filtering.

---

### `src/tools/process/mod.rs` {#src-tools-process-mod-rs}

- **Source Link:** [`src/tools/process/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/process/mod.rs)
- **Lines of Code:** 334 (9569 bytes)

#### Primary Responsibility
Process and background job model-facing tools (TL-02, D-07, D-13).

#### Types & Trait Declarations
- **Structs (11):** `JobOutputInput`, `JobOutputTool`, `JobStatusInput`, `JobStatusTool`, `JobStopInput`, `JobStopOutput`, `JobStopTool`, `RunCommandInput`, `RunCommandTool`, `StartJobInput`, `StartJobTool`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn get_process(ctx: &ToolExecutionContext) -> Result<Arc<dyn ProcessService>, ToolError>;
// private
fn get_jobs(ctx: &ToolExecutionContext) -> Result<Arc<dyn JobService>, ToolError>;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
// private
fn id(&self) -> &str;
```

---

### `src/tools/qa/mod.rs` {#src-tools-qa-mod-rs}

- **Source Link:** [`src/tools/qa/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/qa/mod.rs)
- **Lines of Code:** 412 (14088 bytes)

#### Primary Responsibility
Quality assurance and verification model-facing tools (TL-02, D-07).

#### Types & Trait Declarations
- **Structs (7):** `FlexibleVecVisitor`, `RunFormatterInput`, `RunFormatterTool`, `RunLinterInput`, `RunLinterTool`, `RunTestsInput`, `RunTestsTool`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn get_verification(ctx: &ToolExecutionContext) -> Result<Arc<dyn VerificationService>, ToolError>;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
```

---

### `src/tools/registry.rs` {#src-tools-registry-rs}

- **Source Link:** [`src/tools/registry.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/registry.rs)
- **Lines of Code:** 201 (7509 bytes)

#### Primary Responsibility
Central tool catalog registry managing model-facing tools (TL-02, D-07).

#### Types & Trait Declarations
- **Structs (1):** `ToolRegistry`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn register(&mut self, tool: T);
// pub
fn register_any(&mut self, tool: Arc<dyn AnyTool>);
// pub
fn get(&self, id: &str) -> Option<Arc<dyn AnyTool>>;
// pub
fn list_tools(&self) -> Vec<Arc<dyn AnyTool>>;
// pub
fn len(&self) -> usize;
// pub
fn is_empty(&self) -> bool;
// pub
fn capabilities(&self) -> Option<&Arc<CapabilityRegistry>>;
// pub
fn new_default(capabilities: Arc<CapabilityRegistry>) -> Self;
// pub
fn register_agentic_tools(&mut self);
// pub
fn register_repository_intelligence(&mut self);
// pub
fn register_web_tools(&mut self);
// pub
fn register_extended_filesystem_tools(&mut self);
// pub
fn register_lsp_tools(&mut self);
```

---

### `src/tools/repo/mod.rs` {#src-tools-repo-mod-rs}

- **Source Link:** [`src/tools/repo/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/repo/mod.rs)
- **Lines of Code:** 573 (15822 bytes)

#### Primary Responsibility
Repository intelligence model-facing tools consuming RepositoryService (TL-02, D-07).

#### Types & Trait Declarations
- **Structs (27):** `LspFindReferencesInput`, `LspFindReferencesOutput`, `LspFindReferencesTool`, `LspGotoDefinitionInput`, `LspGotoDefinitionOutput`, `LspGotoDefinitionTool`, `LspHoverInput`, `LspHoverOutput`, `LspHoverTool`, `LspSymbolsInput`, `LspSymbolsOutput`, `LspSymbolsTool`, `RepoDependenciesInput`, `RepoDependenciesOutput`, `RepoDependenciesTool`, `RepoImpactInput`, `RepoImpactOutput`, `RepoImpactTool`, `RepoOverviewInput`, `RepoOverviewOutput`, `RepoOverviewTool`, `RepoSearchInput`, `RepoSearchOutput`, `RepoSearchTool`, `RepoSymbolsInput`, `RepoSymbolsOutput`, `RepoSymbolsTool`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn get_repo(ctx: &ToolExecutionContext) -> Result<Arc<dyn RepositoryService>, ToolError>;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
```

---

### `src/tools/risk.rs` {#src-tools-risk-rs}

- **Source Link:** [`src/tools/risk.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/risk.rs)
- **Lines of Code:** 294 (11294 bytes)

#### Primary Responsibility
Baseline risk classification and dynamic effective risk evaluation (TL-01, D-08).

#### Types & Trait Declarations
- **Structs (1):** `EffectiveRisk`
- **Enums (1):** `RiskClass`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(base_risk: RiskClass) -> Self;
// pub
fn from_candidate(base_risk: RiskClass,
        candidate_risk: RiskClass,
        reason: impl Into<String>,) -> Self;
// pub
fn base_risk(&self) -> RiskClass;
// pub
fn effective_risk(&self) -> RiskClass;
// pub
fn reasons(&self) -> &[String];
// pub
fn escalate(&mut self, candidate: RiskClass, reason: impl Into<String>);
// pub
fn evaluate_file_target(base_risk: RiskClass,
        lexical_path: &Path,
        effective_target: Option<&Path>,) -> ;
// pub
fn evaluate_file_path(base_risk: RiskClass, path: &Path) -> Self;
// pub
fn is_sensitive_path(path: &Path) -> bool;
// pub
fn is_runtime_managed_temp_path(path: &Path) -> bool;
// private
fn is_sensitive_temp_alias(path: &Path) -> bool;
// private
fn is_sensitive_path_inner(path: &Path) -> bool;
// private
fn test_risk_order();
// private
fn test_effective_risk_never_decreases();
// private
fn test_sensitive_path_escalation();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_risk_order`, `test_effective_risk_never_decreases`, `test_sensitive_path_escalation`

---

### `src/tools/skill.rs` {#src-tools-skill-rs}

- **Source Link:** [`src/tools/skill.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/skill.rs)
- **Lines of Code:** 153 (4515 bytes)

#### Primary Responsibility
Model-available specialized skills tools consuming SkillRegistry.

#### Types & Trait Declarations
- **Structs (7):** `SkillSummaryDto`, `SkillsInspectInput`, `SkillsInspectOutput`, `SkillsInspectTool`, `SkillsListInput`, `SkillsListOutput`, `SkillsListTool`

#### Key Functions & Signatures (12 shown)
```rust
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        _input: Self::Input,) -> Result<Self::Output, ToolEr;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
```

---

### `src/tools/terminal.rs` {#src-tools-terminal-rs}

- **Source Link:** [`src/tools/terminal.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/terminal.rs)
- **Lines of Code:** 398 (11095 bytes)

#### Primary Responsibility
Terminal session model-facing tools (CTL-01, CTL-02, TL-02).

#### Types & Trait Declarations
- **Structs (17):** `TerminalReadStreamInput`, `TerminalReadStreamOutput`, `TerminalReadStreamTool`, `TerminalResizeInput`, `TerminalResizeOutput`, `TerminalResizeTool`, `TerminalSessionStatusInput`, `TerminalSessionStatusTool`, `TerminalStartSessionInput`, `TerminalStartSessionOutput`, `TerminalStartSessionTool`, `TerminalTerminateSessionInput`, `TerminalTerminateSessionOutput`, `TerminalTerminateSessionTool`, `TerminalWriteInputInput`, `TerminalWriteInputOutput`, `TerminalWriteInputTool`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn get_terminal(ctx: &ToolExecutionContext) -> Result<Arc<dyn TerminalService>, ToolError>;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
fn resource_limits(&self) -> ResourceLimits;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
```

---

### `src/tools/web.rs` {#src-tools-web-rs}

- **Source Link:** [`src/tools/web.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tools/web.rs)
- **Lines of Code:** 151 (4043 bytes)

#### Primary Responsibility
Web search and URL fetching tools (CTL-02, PRD §04).

#### Types & Trait Declarations
- **Structs (6):** `WebFetchInput`, `WebFetchOutput`, `WebFetchTool`, `WebSearchInput`, `WebSearchOutput`, `WebSearchTool`

#### Key Functions & Signatures (12 shown)
```rust
// private
fn default_max_results() -> usize;
// private
fn default_timeout_secs() -> u64;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
// private
fn id(&self) -> &str;
// private
fn description(&self) -> &str;
// private
fn required_capabilities(&self) -> &[CapabilityFamily];
// private
fn base_risk(&self) -> RiskClass;
// private
async fn execute(&self,
        ctx: &ToolExecutionContext,
        input: Self::Input,) -> Result<Self::Output, ToolErr;
```

---
