# Pipeline Execution

> **Architectural Layer:** L5/L6 Pipeline  
> **Source Directory:** `src/pipeline`  
> **File Count:** 18 source files  

End-to-end task pipelines, staging, execution harnesses, and lifecycle transitions.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [capture.rs](#src-pipeline-capture-rs) | 118 | `OutputCaptureManager` | Budget-aware tool output capture and artifact externalization (TL-03, ... |
| [dedup.rs](#src-pipeline-dedup-rs) | 472 | `MutationDedupFence, DedupError, FenceVerdict` | Durable mutating-tool deduplication fence.  Crash-between-action-and-p... |
| [dispatcher.rs](#src-pipeline-dispatcher-rs) | 585 | `ProductionActionDispatcher` | Production action dispatcher wiring WorkerRunner to the 11-stage pipel... |
| [error.rs](#src-pipeline-error-rs) | 267 | `ToolError, ToolErrorCategory` | Strongly typed model-facing tool error taxonomy with bounded correctio... |
| [mod.rs](#src-pipeline-mod-rs) | 21 | `Functions/Traits` | Non-bypassable 11-stage tool execution pipeline, output budgeting, and... |
| [runner.rs](#src-pipeline-runner-rs) | 344 | `ToolPipelineRunner` | Non-bypassable 11-stage tool execution pipeline runner (TL-03, per D-0... |
| [approval_resolution.rs](#src-pipeline-stages-approval_resolution-rs) | 379 | `ApprovalResolutionStage, ExecutionAuthorizedState` | Subsystem component |
| [capability_check.rs](#src-pipeline-stages-capability_check-rs) | 138 | `CapabilityAuthorizedState, CapabilityCheckStage` | Stage 5: Capability Check Stage (TL-03, per D-09). |
| [capture_normalization.rs](#src-pipeline-stages-capture_normalization-rs) | 300 | `AuditDigest, CaptureNormalizationStage, DiagnosticOutput` | Stage 10: Capture &amp; Normalization Stage (TL-03, per D-09, D-11). |
| [decoding.rs](#src-pipeline-stages-decoding-rs) | 80 | `ArgDecodingStage, DecodedArgsState` | Stage 2: Argument Decoding Stage (TL-03, per D-09). |
| [execution.rs](#src-pipeline-stages-execution-rs) | 68 | `RawExecutionState, ToolExecutionStage` | Stage 9: Tool Execution Stage (TL-03, per D-09).  Non-negotiable secur... |
| [mod.rs](#src-pipeline-stages-mod-rs) | 42 | `Functions/Traits` | The 11 non-bypassable typed state-machine stages of the tool execution... |
| [policy_gate.rs](#src-pipeline-stages-policy_gate-rs) | 145 | `PolicyEvaluatedState, PolicyGateStage` | Stage 7: PolicyGate Evaluation Stage (TL-03, per D-09). |
| [resolution.rs](#src-pipeline-stages-resolution-rs) | 41 | `ResolvedToolState, ToolResolutionStage` | Stage 1: Tool Resolution Stage (TL-03, per D-09). |
| [resource_scope.rs](#src-pipeline-stages-resource_scope-rs) | 475 | `ResourceBinding, ResourceScopeStage, ResourceScopedState` | Stage 6: Resource Scope &amp; Lease Validation Stage (TL-03, per D-09)... |
| [schema_validation.rs](#src-pipeline-stages-schema_validation-rs) | 207 | `SchemaValidatedState, SchemaValidationStage` | Stage 3: Schema Validation Stage (TL-03, per D-09). |
| [semantic_validation.rs](#src-pipeline-stages-semantic_validation-rs) | 92 | `SemanticValidationStage, SemanticallyValidatedState` | Stage 4: Semantic Validation Stage (TL-03, per D-09). |
| [telemetry_record.rs](#src-pipeline-stages-telemetry_record-rs) | 60 | `TelemetryDurableRecordStage` | Stage 11: Telemetry &amp; Durable Record Stage (TL-03, per D-09, D-12)... |

---

### `src/pipeline/capture.rs` {#src-pipeline-capture-rs}

- **Source Link:** [`src/pipeline/capture.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/capture.rs)
- **Lines of Code:** 118 (4397 bytes)

#### Primary Responsibility
Budget-aware tool output capture and artifact externalization (TL-03, per D-11).

#### Types & Trait Declarations
- **Structs (1):** `OutputCaptureManager`

#### Key Functions & Signatures (5 shown)
```rust
// private
fn default() -> Self;
// pub
fn new(max_inline_bytes: usize, max_inline_lines: usize) -> Self;
// pub
fn max_inline_bytes(&self) -> usize;
// pub
fn max_inline_lines(&self) -> usize;
// pub
async fn process_output(&self,
        raw_output: &str,
        artifact_store: Option<&Arc<dyn ArtifactStore>>,) -> Re;
```

---

### `src/pipeline/dedup.rs` {#src-pipeline-dedup-rs}

- **Source Link:** [`src/pipeline/dedup.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/dedup.rs)
- **Lines of Code:** 472 (18024 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Durable mutating-tool deduplication fence.  Crash-between-action-and-persistence replays an already-committed mutation as a brand-new side effect (at-least-once). This module provides the durable identity that closes the gap where safe:  ```text same committed mutation (task + tool + canonical input hash) → recognized from the fence → no duplicate side effect ```  Identity is semantic, never timestamp-only. Outcomes distinguish committed success (suppress duplicates) from failed attempts (legitimate retry still proceeds). Recovery is never made impossible: only a recorded *success* suppresses re-execution.  Suppression applies exclusively to the idempotent file-mutation allowlist ([`is_fenced_mutating_tool`]). Non-idempotent tools (process execution, test runs, network) always execute; their outcomes are still recorded for audit. Suppressing a repeated `cargo test` would break legitimate verify-after-fix flows, so commands are fenced by record, not by skip.

#### Types & Trait Declarations
- **Structs (1):** `MutationDedupFence`
- **Enums (2):** `DedupError`, `FenceVerdict`

#### Key Functions & Signatures (11 shown)
```rust
// pub
fn is_fenced_mutating_tool(tool_name: &str) -> bool;
// pub
fn canonical_json(value: &serde_json::Value) -> String;
// pub
fn fingerprint_mutation(task_id: &TaskId,
    tool_name: &str,
    params: &serde_json::Value,) -> String;
// pub
fn fingerprint_parts(parts: &[&[u8]]) -> String;
// pub
fn sha_hex(data: &[u8]) -> String;
// pub
fn new(pool: SqlitePool) -> Self;
// pub
async fn check(&self,
        task_id: &TaskId,
        tool_name: &str,
        fingerprint: &str,) -> FenceVerdict;
// pub
async fn acquire_claim(&self,
        task_id: &TaskId,
        tool_name: &str,
        fingerprint: &str,
        stal;
// pub
async fn commit_outcome(&self,
        task_id: &TaskId,
        tool_name: &str,
        fingerprint: &str,
        suc;
// pub
async fn record(&self,
        task_id: &TaskId,
        tool_name: &str,
        fingerprint: &str,
        success: bo;
// pub
async fn recorded_outcome(&self,
        task_id: &TaskId,
        tool_name: &str,
        fingerprint: &str,) -> Optio;
```

---

### `src/pipeline/dispatcher.rs` {#src-pipeline-dispatcher-rs}

- **Source Link:** [`src/pipeline/dispatcher.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/dispatcher.rs)
- **Lines of Code:** 585 (26707 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Production action dispatcher wiring WorkerRunner to the 11-stage pipeline (TL-03, D-12).

#### Types & Trait Declarations
- **Structs (1):** `ProductionActionDispatcher`

#### Key Functions & Signatures (12 shown)
```rust
// pub
fn new(runner: Arc<ToolPipelineRunner>,
        context: ToolExecutionContext,
        policy_gate: Arc<dyn PolicyGate>,;
// pub
fn with_session_repo(mut self,
        repo: crate::interaction::session::SqliteSessionRepository,) -> Self;
// pub
fn with_session_id(mut self, id: crate::ids::SessionId) -> Self;
// pub
fn with_event_bus(mut self, bus: Arc<dyn crate::events::EventBus>) -> Self;
// pub
fn with_replan_authority(mut self,
        replan_authority: Arc<crate::recovery::ReplanAuthority>,) -> Self;
// pub
fn replan_authority(&self) -> Option<&Arc<crate::recovery::ReplanAuthority>>;
// pub
fn runner(&self) -> &Arc<ToolPipelineRunner>;
// pub
fn context(&self) -> &ToolExecutionContext;
// pub
fn policy_gate(&self) -> &Arc<dyn PolicyGate>;
// pub
fn autonomy_mode(&self) -> AutonomyMode;
// private
async fn dispatch(&self, action: &ActionRequest) -> Result<ActionResult, String>;
// private
async fn dispatch_action(&self,
        action: &crate::agent::action::AgentAction,) -> Result<crate::agent::action::Age;
```

---

### `src/pipeline/error.rs` {#src-pipeline-error-rs}

- **Source Link:** [`src/pipeline/error.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/error.rs)
- **Lines of Code:** 267 (8296 bytes)

#### Primary Responsibility
Strongly typed model-facing tool error taxonomy with bounded correction hints (TL-04, per D-10).

#### Types & Trait Declarations
- **Structs (1):** `ToolError`
- **Enums (1):** `ToolErrorCategory`

#### Key Functions & Signatures (14 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// pub
fn new(category: ToolErrorCategory,
        code: impl Into<String>,
        message: impl Into<String>,
        provena;
// pub
fn validation(code: impl Into<String>,
        message: impl Into<String>,
        hint: Option<String>,) -> Self;
// pub
fn not_found(code: impl Into<String>,
        message: impl Into<String>,
        hint: Option<String>,) -> Self;
// pub
fn precondition_failed(code: impl Into<String>,
        message: impl Into<String>,
        hint: Option<String>,) -> Se;
// pub
fn permission_denied(code: impl Into<String>,
        message: impl Into<String>,
        hint: Option<String>,) -> Self;
// pub
fn execution_failed(code: impl Into<String>,
        message: impl Into<String>,
        hint: Option<String>,) -> Self;
// pub
fn resource_exhausted(code: impl Into<String>,
        message: impl Into<String>,
        hint: Option<String>,) -> Sel;
// pub
fn with_provenance(mut self, provenance: impl Into<String>) -> Self;
// pub
fn with_retryable(mut self, retryable: bool) -> Self;
// pub
fn to_model_diagnostic(&self) -> String;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// pub
fn sanitize_hint(hint: &str) -> String;
// private
fn from(err: crate::tools::error::ToolError) -> Self;
```

---

### `src/pipeline/mod.rs` {#src-pipeline-mod-rs}

- **Source Link:** [`src/pipeline/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/mod.rs)
- **Lines of Code:** 21 (842 bytes)

#### Primary Responsibility
Non-bypassable 11-stage tool execution pipeline, output budgeting, and typed error taxonomy (TL-03, TL-04).  Enforces compile-time and runtime guarantees: - 11 linear state-machine stages (`stages`) - Physical side effects occur strictly in Stage 9 (`execution`) - Budget-aware output capture and artifact externalization (`capture`) - Strongly typed model-facing error taxonomy with bounded hints (`error`) - Production dispatcher connecting `WorkerRunner` to the pipeline (`dispatcher`)

---

### `src/pipeline/runner.rs` {#src-pipeline-runner-rs}

- **Source Link:** [`src/pipeline/runner.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/runner.rs)
- **Lines of Code:** 344 (13936 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
Non-bypassable 11-stage tool execution pipeline runner (TL-03, per D-09, D-12).

#### Types & Trait Declarations
- **Structs (1):** `ToolPipelineRunner`

#### Key Functions & Signatures (11 shown)
```rust
// pub
fn new(tool_registry: Arc<ToolRegistry>) -> Self;
// pub
fn with_db_pool(mut self, pool: SqlitePool) -> Self;
// pub
fn with_approval_coordinator(mut self, coordinator: Arc<ApprovalCoordinator>) -> Self;
// pub
fn with_artifact_store(mut self, store: Arc<dyn ArtifactStore>) -> Self;
// pub
fn with_capture_manager(mut self, capture_manager: Arc<OutputCaptureManager>) -> Self;
// pub
fn tool_registry(&self) -> &Arc<ToolRegistry>;
// pub
fn capture_manager(&self) -> &Arc<OutputCaptureManager>;
// pub
fn artifact_store(&self) -> Option<&Arc<dyn ArtifactStore>>;
// pub
fn approval_coordinator(&self) -> Option<&Arc<ApprovalCoordinator>>;
// pub
fn db_pool(&self) -> Option<&SqlitePool>;
// pub
async fn execute_action(&self,
        action: &ActionRequest,
        context: &ToolExecutionContext,
        policy_ga;
```

---

### `src/pipeline/stages/approval_resolution.rs` {#src-pipeline-stages-approval_resolution-rs}

- **Source Link:** [`src/pipeline/stages/approval_resolution.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/stages/approval_resolution.rs)
- **Lines of Code:** 379 (18956 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (2):** `ApprovalResolutionStage`, `ExecutionAuthorizedState`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn execute(state: PolicyEvaluatedState,
        autonomy_mode: AutonomyMode,) -> Result<ExecutionAuthorizedState, ToolEr;
// pub
fn execute_sync(state: PolicyEvaluatedState,
        autonomy_mode: AutonomyMode,) -> Result<ExecutionAuthorizedState, T;
// pub
async fn execute_async(state: PolicyEvaluatedState,
        context: &ToolExecutionContext,
        autonomy_mode: Auton;
```

---

### `src/pipeline/stages/capability_check.rs` {#src-pipeline-stages-capability_check-rs}

- **Source Link:** [`src/pipeline/stages/capability_check.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/stages/capability_check.rs)
- **Lines of Code:** 138 (6361 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Stage 5: Capability Check Stage (TL-03, per D-09).

#### Types & Trait Declarations
- **Structs (2):** `CapabilityAuthorizedState`, `CapabilityCheckStage`

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn execute(state: SemanticallyValidatedState,
        context: &ToolExecutionContext,) -> Result<CapabilityAuthorizedSta;
```

---

### `src/pipeline/stages/capture_normalization.rs` {#src-pipeline-stages-capture_normalization-rs}

- **Source Link:** [`src/pipeline/stages/capture_normalization.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/stages/capture_normalization.rs)
- **Lines of Code:** 300 (10521 bytes)

#### Primary Responsibility
Stage 10: Capture &amp; Normalization Stage (TL-03, per D-09, D-11).

#### Types & Trait Declarations
- **Structs (7):** `AuditDigest`, `CaptureNormalizationStage`, `DiagnosticOutput`, `ModelVisibleOutput`, `NormalizedResultState`, `PipelineOutputEvidence`, `RawExecutionEvidence`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(raw: impl Into<String>) -> Self;
// pub
fn classify(self,
        model_visible_hint: String,) -> (ModelVisibleOutput, DiagnosticOutput, AuditDigest);
// pub
fn expose_privileged(&self) -> &str;
// pub
fn as_str(&self) -> &str;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn as_str(&self) -> &str;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn as_str(&self) -> &str;
// pub
fn empty_digest() -> Self;
// private
fn hex_digest(raw: &str) -> String;
// pub
fn new(raw: String, model_visible: String) -> Self;
// pub
fn empty() -> Self;
// pub
fn raw_evidence(&self) -> RawExecutionEvidence;
// pub
fn model_visible(&self) -> ModelVisibleOutput;
// pub
fn diagnostic(&self) -> DiagnosticOutput;
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_pipeline_output_evidence_classifications`, `test_pipeline_output_evidence_empty`

---

### `src/pipeline/stages/decoding.rs` {#src-pipeline-stages-decoding-rs}

- **Source Link:** [`src/pipeline/stages/decoding.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/stages/decoding.rs)
- **Lines of Code:** 80 (2935 bytes)

#### Primary Responsibility
Stage 2: Argument Decoding Stage (TL-03, per D-09).

#### Types & Trait Declarations
- **Structs (2):** `ArgDecodingStage`, `DecodedArgsState`

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn execute(state: ResolvedToolState) -> Result<DecodedArgsState, ToolError>;
```

---

### `src/pipeline/stages/execution.rs` {#src-pipeline-stages-execution-rs}

- **Source Link:** [`src/pipeline/stages/execution.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/stages/execution.rs)
- **Lines of Code:** 68 (2295 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Stage 9: Tool Execution Stage (TL-03, per D-09).  Non-negotiable security invariant: Side-effects occur STRICTLY in this stage. Stages 1–8 enforce structural, semantic, capability, resource, and policy authorization without mutations.

#### Types & Trait Declarations
- **Structs (2):** `RawExecutionState`, `ToolExecutionStage`

#### Key Functions & Signatures (1 shown)
```rust
// pub
async fn execute(state: ExecutionAuthorizedState,
        context: &ToolExecutionContext,) -> RawExecutionState;
```

---

### `src/pipeline/stages/mod.rs` {#src-pipeline-stages-mod-rs}

- **Source Link:** [`src/pipeline/stages/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/stages/mod.rs)
- **Lines of Code:** 42 (2069 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
The 11 non-bypassable typed state-machine stages of the tool execution pipeline (TL-03, D-09).  State transitions: `ActionRequest` -&gt; Stage 1: `ToolResolutionStage` (`ResolvedToolState`) -&gt; Stage 2: `ArgDecodingStage` (`DecodedArgsState`) -&gt; Stage 3: `SchemaValidationStage` (`SchemaValidatedState`) -&gt; Stage 4: `SemanticValidationStage` (`SemanticallyValidatedState`) -&gt; Stage 5: `CapabilityCheckStage` (`CapabilityAuthorizedState`) -&gt; Stage 6: `ResourceScopeStage` (`ResourceScopedState`) -&gt; Stage 7: `PolicyGateStage` (`PolicyEvaluatedState`) -&gt; Stage 8: `ApprovalResolutionStage` (`ExecutionAuthorizedState`) -&gt; Stage 9: `ToolExecutionStage` (`RawExecutionState`) [MUTATING SIDE-EFFECTS HERE ONLY] -&gt; Stage 10: `CaptureNormalizationStage` (`NormalizedResultState`) -&gt; Stage 11: `TelemetryDurableRecordStage` (`ActionResult`)

---

### `src/pipeline/stages/policy_gate.rs` {#src-pipeline-stages-policy_gate-rs}

- **Source Link:** [`src/pipeline/stages/policy_gate.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/stages/policy_gate.rs)
- **Lines of Code:** 145 (5524 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
Stage 7: PolicyGate Evaluation Stage (TL-03, per D-09).

#### Types & Trait Declarations
- **Structs (2):** `PolicyEvaluatedState`, `PolicyGateStage`

#### Key Functions & Signatures (2 shown)
```rust
// pub
async fn execute(state: ResourceScopedState,
        context: &ToolExecutionContext,
        policy_gate: &dyn PolicyGat;
// pub
async fn execute_with_pool(state: ResourceScopedState,
        context: &ToolExecutionContext,
        policy_gate: &dyn;
```

---

### `src/pipeline/stages/resolution.rs` {#src-pipeline-stages-resolution-rs}

- **Source Link:** [`src/pipeline/stages/resolution.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/stages/resolution.rs)
- **Lines of Code:** 41 (1237 bytes)

#### Primary Responsibility
Stage 1: Tool Resolution Stage (TL-03, per D-09).

#### Types & Trait Declarations
- **Structs (2):** `ResolvedToolState`, `ToolResolutionStage`

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn execute(action: &ActionRequest,
        registry: &Arc<ToolRegistry>,) -> Result<ResolvedToolState, ToolError>;
```

---

### `src/pipeline/stages/resource_scope.rs` {#src-pipeline-stages-resource_scope-rs}

- **Source Link:** [`src/pipeline/stages/resource_scope.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/stages/resource_scope.rs)
- **Lines of Code:** 475 (21741 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Stage 6: Resource Scope &amp; Lease Validation Stage (TL-03, per D-09).

#### Types & Trait Declarations
- **Structs (3):** `ResourceBinding`, `ResourceScopeStage`, `ResourceScopedState`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn execute(state: CapabilityAuthorizedState,
        context: &ToolExecutionContext,) -> Result<ResourceScopedState, Too;
// pub
fn verify_bindings_live(bound_resources: &[ResourceBinding],
        workspace_root: &Path,) -> Result<(), ToolError>;
// private
fn normalize_path(path: &Path) -> PathBuf;
```

---

### `src/pipeline/stages/schema_validation.rs` {#src-pipeline-stages-schema_validation-rs}

- **Source Link:** [`src/pipeline/stages/schema_validation.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/stages/schema_validation.rs)
- **Lines of Code:** 207 (7907 bytes)

#### Primary Responsibility
Stage 3: Schema Validation Stage (TL-03, per D-09).

#### Types & Trait Declarations
- **Structs (2):** `SchemaValidatedState`, `SchemaValidationStage`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn execute(state: DecodedArgsState) -> Result<SchemaValidatedState, ToolError>;
// private
fn coerce_value_to_schema_type(val: &mut serde_json::Value, schema: &serde_json::Value);
// private
fn matches_schema_type(val: &serde_json::Value, schema: &serde_json::Value) -> bool;
// private
fn check_single_type(val: &serde_json::Value, expected: &str) -> bool;
```

---

### `src/pipeline/stages/semantic_validation.rs` {#src-pipeline-stages-semantic_validation-rs}

- **Source Link:** [`src/pipeline/stages/semantic_validation.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/stages/semantic_validation.rs)
- **Lines of Code:** 92 (3699 bytes)

#### Primary Responsibility
Stage 4: Semantic Validation Stage (TL-03, per D-09).

#### Types & Trait Declarations
- **Structs (2):** `SemanticValidationStage`, `SemanticallyValidatedState`

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn execute(state: SchemaValidatedState) -> Result<SemanticallyValidatedState, ToolError>;
```

---

### `src/pipeline/stages/telemetry_record.rs` {#src-pipeline-stages-telemetry_record-rs}

- **Source Link:** [`src/pipeline/stages/telemetry_record.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/pipeline/stages/telemetry_record.rs)
- **Lines of Code:** 60 (2273 bytes)

#### Primary Responsibility
Stage 11: Telemetry &amp; Durable Record Stage (TL-03, per D-09, D-12).

#### Types & Trait Declarations
- **Structs (1):** `TelemetryDurableRecordStage`

#### Key Functions & Signatures (2 shown)
```rust
// pub
fn execute(state: NormalizedResultState) -> ActionResult;
// pub
fn record_failure(action_id: String, tool_id: String, error: ToolError) -> ActionResult;
```

---
