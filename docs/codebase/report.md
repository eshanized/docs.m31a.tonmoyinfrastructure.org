# Execution Reports

> **Architectural Layer:** L8 Reporting  
> **Source Directory:** `src/report`  
> **File Count:** 6 source files  

Structured scorecard generation, telemetry summaries, and execution reports.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [evidence.rs](#src-report-evidence-rs) | 252 | `EvidenceLinker, EvidenceError, EvidenceUri` | Strongly typed durable evidence URI linking for completion reports (RP... |
| [generator.rs](#src-report-generator-rs) | 582 | `ReportGenerator, ReportError` | Two-phase deterministic completion report generator (RPT-01, RPT-02, D... |
| [json.rs](#src-report-json-rs) | 92 | `JsonReportProjector` | Machine-readable JSON report projector and JSON Schema generator (RPT-... |
| [markdown.rs](#src-report-markdown-rs) | 362 | `MarkdownReportProjector` | Human-readable executive Markdown report projector (RPT-02, D-13). |
| [mod.rs](#src-report-mod-rs) | 18 | `Functions/Traits` | Deterministic Mission Completion Reporting and Evidence Linking (RPT-0... |
| [model.rs](#src-report-model-rs) | 424 | `AgentReportItem, ArtifactReportItem, CompletionReport` | Canonical CompletionReport domain models and ReportCandidate (RPT-01, ... |

---

### `src/report/evidence.rs` {#src-report-evidence-rs}

- **Source Link:** [`src/report/evidence.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/report/evidence.rs)
- **Lines of Code:** 252 (8389 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Strongly typed durable evidence URI linking for completion reports (RPT-03, D-13).

#### Types & Trait Declarations
- **Structs (1):** `EvidenceLinker`
- **Enums (2):** `EvidenceError`, `EvidenceUri`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn parse(uri: &str) -> Result<Self, EvidenceError>;
// pub
fn scheme(&self) -> &'static str;
// pub
fn locator(&self) -> String;
// pub
fn as_uri(&self) -> String;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// pub
fn artifact(id: ArtifactId) -> String;
// pub
fn check(id: CheckId) -> String;
// pub
fn commit(hash: impl Into<String>) -> String;
// pub
fn checkpoint(id: CheckpointId) -> String;
// pub
fn policy_grant(grant_id: impl Into<String>) -> String;
// pub
fn event(id: EventId) -> String;
// pub
fn validate(uri: &str) -> Result<EvidenceUri, EvidenceError>;
// pub
fn is_valid(uri: &str) -> bool;
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_evidence_uri_roundtrip_all_schemes`, `test_invalid_evidence_uri_formats`

---

### `src/report/generator.rs` {#src-report-generator-rs}

- **Source Link:** [`src/report/generator.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/report/generator.rs)
- **Lines of Code:** 582 (22207 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
Two-phase deterministic completion report generator (RPT-01, RPT-02, D-13).

#### Types & Trait Declarations
- **Structs (1):** `ReportGenerator`
- **Enums (1):** `ReportError`

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn new(pool: SqlitePool,
        artifact_store: Arc<dyn ArtifactStore>,
        report_repo: Arc<SqliteReportRepository;
// pub
fn artifact_store(&self) -> &Arc<dyn ArtifactStore>;
// pub
fn report_repo(&self) -> &Arc<SqliteReportRepository>;
// pub
fn redactor(&self) -> &Arc<SecretRedactor>;
// pub
async fn build_candidate(&self,
        mission_id: &MissionId,) -> Result<ReportCandidate, ReportError>;
// pub
async fn build_candidate_from_candidate(&self,
        mut candidate: ReportCandidate,) -> Result<ReportCandidate, Repor;
// pub
async fn seal_report(&self,
        candidate: ReportCandidate,
        gate_result: &Result<();
// pub
async fn write_report_files(&self,
        report: &CompletionReport,
        target_dir: &std::path::Path,) -> Result<(;
// private
fn sanitize_candidate(&self, candidate: &mut ReportCandidate);
// private
fn sanitize_report(&self, report: &mut CompletionReport);
```

---

### `src/report/json.rs` {#src-report-json-rs}

- **Source Link:** [`src/report/json.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/report/json.rs)
- **Lines of Code:** 92 (3533 bytes)

#### Primary Responsibility
Machine-readable JSON report projector and JSON Schema generator (RPT-02, D-13).

#### Types & Trait Declarations
- **Structs (1):** `JsonReportProjector`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn render_report(report: &CompletionReport) -> Result<String, serde_json::Error>;
// pub
fn render_candidate(candidate: &ReportCandidate) -> Result<String, serde_json::Error>;
// pub
fn generate_schema() -> serde_json::Value;
// pub
fn generate_schema_json() -> Result<String, serde_json::Error>;
// pub
fn validate_json(json_str: &str) -> Result<CompletionReport, serde_json::Error>;
// private
fn test_json_projection_and_schema();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_json_projection_and_schema`

---

### `src/report/markdown.rs` {#src-report-markdown-rs}

- **Source Link:** [`src/report/markdown.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/report/markdown.rs)
- **Lines of Code:** 362 (14662 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Human-readable executive Markdown report projector (RPT-02, D-13).

#### Types & Trait Declarations
- **Structs (1):** `MarkdownReportProjector`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn render_report(report: &CompletionReport) -> String;
// pub
fn render_candidate(candidate: &ReportCandidate) -> String;
// private
fn test_markdown_projection_has_yaml_frontmatter_and_sections();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_markdown_projection_has_yaml_frontmatter_and_sections`

---

### `src/report/mod.rs` {#src-report-mod-rs}

- **Source Link:** [`src/report/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/report/mod.rs)
- **Lines of Code:** 18 (705 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Deterministic Mission Completion Reporting and Evidence Linking (RPT-01..03, D-13).

---

### `src/report/model.rs` {#src-report-model-rs}

- **Source Link:** [`src/report/model.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/report/model.rs)
- **Lines of Code:** 424 (14850 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Canonical CompletionReport domain models and ReportCandidate (RPT-01, D-13).

#### Types & Trait Declarations
- **Structs (15):** `AgentReportItem`, `ArtifactReportItem`, `CompletionReport`, `FailureReportItem`, `FileChangeReportItem`, `GitReportState`, `ModelReportItem`, `PlanReportSummary`, `PolicyReportItem`, `RecoveryReportItem`, `ReportCandidate`, `RequirementReportItem`, `ReviewReportItem`, `TaskReportItem`, `VerificationReportItem`
- **Enums (1):** `CompletionStatus`

#### Key Functions & Signatures (9 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn total_tokens_used(&self) -> u64;
// pub
fn total_cost_usd(&self) -> f64;
// pub
fn total_evidence_count(&self) -> usize;
// pub
fn into_sealed(self, final_status: CompletionStatus) -> CompletionReport;
// private
fn test_completion_report_16_fields_exist_and_roundtrip();
// private
fn test_candidate_into_sealed();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_completion_report_16_fields_exist_and_roundtrip`, `test_candidate_into_sealed`

---
