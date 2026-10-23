# Telemetry & Spans

> **Architectural Layer:** L8 Telemetry  
> **Source Directory:** `src/telemetry`  
> **File Count:** 7 source files  

Distributed tracing spans, metrics recording, and operational observability.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [collector.rs](#src-telemetry-collector-rs) | 361 | `TelemetryCollector` | Central Telemetry Collector Service (OBS-01, OBS-02, D-01, D-02).  Coo... |
| [context.rs](#src-telemetry-context-rs) | 136 | `CorrelationContext` | Distributed &amp; Hierarchical Correlation Context (OBS-01, D-03).  Pr... |
| [inspect.rs](#src-telemetry-inspect-rs) | 153 | `TelemetryInspectionReport` | Telemetry Inspection CLI Formatter (OBS-03, D-04).  Provides human-rea... |
| [mod.rs](#src-telemetry-mod-rs) | 15 | `Functions/Traits` | Local Observability, Telemetry &amp; Distributed Correlation (OBS-01, ... |
| [redactor.rs](#src-telemetry-redactor-rs) | 387 | `SecretRedactor` | Multi-tier Secret Redaction &amp; Sanitization Boundary (OBS-02, D-02)... |
| [stream.rs](#src-telemetry-stream-rs) | 162 | `NdjsonStreamWriter` | Append-only NDJSON Stream Writer for High-Volume Telemetry (OBS-01, D-... |
| [types.rs](#src-telemetry-types-rs) | 175 | `MetricSample, TelemetrySpan, TelemetrySummary` | Telemetry Domain Types &amp; Models (OBS-01, D-01, D-03). |

---

### `src/telemetry/collector.rs` {#src-telemetry-collector-rs}

- **Source Link:** [`src/telemetry/collector.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/telemetry/collector.rs)
- **Lines of Code:** 361 (12251 bytes)

#### Primary Responsibility
Central Telemetry Collector Service (OBS-01, OBS-02, D-01, D-02).  Coordinates secret redaction, SQLite index persistence, and high-volume NDJSON stream writing for spans and metrics.

#### Types & Trait Declarations
- **Structs (1):** `TelemetryCollector`

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn new(redactor: Arc<SecretRedactor>,
        repository: SqliteTelemetryRepository,
        stream_writer: NdjsonStream;
// pub
fn redactor(&self) -> &Arc<SecretRedactor>;
// pub
async fn start_span(&self,
        context: &CorrelationContext,
        name: &str,
        kind: SpanKind,) -> Result<;
// pub
async fn finish_span(&self,
        span_id: &str,
        status: SpanStatus,
        error_message: Option<String>,
  ;
// pub
async fn record_metric(&self,
        mission_id: MissionId,
        name: &str,
        value: f64,
        unit: &str,;
// private
async fn setup_test_collector() -> (
        TelemetryCollector,
        SqliteTelemetryRepository,
        NdjsonStream;
// private
async fn test_collector_initialization_and_accessor();
// private
async fn test_collector_start_and_finish_span_lifecycle();
// private
async fn test_collector_finish_untracked_span();
// private
async fn test_collector_record_metric_with_redaction();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_collector_initialization_and_accessor`, `test_collector_start_and_finish_span_lifecycle`, `test_collector_finish_untracked_span`, `test_collector_record_metric_with_redaction`

---

### `src/telemetry/context.rs` {#src-telemetry-context-rs}

- **Source Link:** [`src/telemetry/context.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/telemetry/context.rs)
- **Lines of Code:** 136 (4353 bytes)

#### Primary Responsibility
Distributed &amp; Hierarchical Correlation Context (OBS-01, D-03).  Provides W3C-compatible trace and span identifiers coupled with strongly typed M31A domain entity references (mission, task, agent, job, tool).

#### Types & Trait Declarations
- **Structs (1):** `CorrelationContext`

#### Key Functions & Signatures (10 shown)
```rust
// private
fn generate_trace_id() -> String;
// private
fn generate_span_id() -> String;
// pub
fn new_root(mission_id: MissionId) -> Self;
// pub
fn child_span(&self) -> Self;
// pub
fn with_task(&self, task_id: TaskId) -> Self;
// pub
fn with_agent(&self, agent_id: AgentId) -> Self;
// pub
fn with_tool_call(&self, call_id: impl Into<String>) -> Self;
// pub
fn with_job(&self, job_id: JobId) -> Self;
// pub
fn with_session(&self, session_id: SessionId) -> Self;
// private
fn test_root_and_child_span_correlation();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_root_and_child_span_correlation`

---

### `src/telemetry/inspect.rs` {#src-telemetry-inspect-rs}

- **Source Link:** [`src/telemetry/inspect.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/telemetry/inspect.rs)
- **Lines of Code:** 153 (5513 bytes)

#### Primary Responsibility
Telemetry Inspection CLI Formatter (OBS-03, D-04).  Provides human-readable console projections and machine-readable JSON/NDJSON exports of mission telemetry spans and metric observations.

#### Types & Trait Declarations
- **Structs (1):** `TelemetryInspectionReport`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn success(text: impl Into<String>, data: serde_json::Value) -> Self;
// pub
fn with_exit_code(mut self, code: i32) -> Self;
// pub
async fn inspect_telemetry(repo: &SqliteTelemetryRepository,
    stream_writer: &NdjsonStreamWriter,
    mission_id: &Mi;
```

---

### `src/telemetry/mod.rs` {#src-telemetry-mod-rs}

- **Source Link:** [`src/telemetry/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/telemetry/mod.rs)
- **Lines of Code:** 15 (488 bytes)

#### Primary Responsibility
Local Observability, Telemetry &amp; Distributed Correlation (OBS-01, OBS-02, OBS-03).

---

### `src/telemetry/redactor.rs` {#src-telemetry-redactor-rs}

- **Source Link:** [`src/telemetry/redactor.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/telemetry/redactor.rs)
- **Lines of Code:** 387 (14727 bytes)

#### Primary Responsibility
Multi-tier Secret Redaction &amp; Sanitization Boundary (OBS-02, D-02).  Enforces deterministic, unconditional scrubbing of API tokens, private keys, AWS credentials, registered secret tokens, ANSI escapes, and log injection controls before telemetry data is stored in SQLite or appended to NDJSON streams.

#### Types & Trait Declarations
- **Structs (1):** `SecretRedactor`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn global() -> &'static Self;
// pub
fn new() -> Self;
// pub
fn register_secret(&self, secret: &str);
// pub
fn redact_string(&self, input: &str) -> String;
// pub
fn redact(&self, input: &str) -> String;
// pub
fn redact_text(&self, input: &str) -> String;
// pub
fn sanitize_error(&self, err: &str) -> String;
// pub
fn redact_value(&self, value: &mut Value);
// private
fn test_exact_secret_redaction();
// private
fn test_regex_credential_scrubbing();
// private
fn test_ansi_and_carriage_return_sanitization();
// private
fn test_json_value_recursive_redaction();
// private
fn test_nvidia_api_key_redaction();
// private
fn test_github_and_gitlab_token_redaction();
```

#### Unit Verification (10 inline tests)
Tests defined within module:
`test_exact_secret_redaction`, `test_regex_credential_scrubbing`, `test_ansi_and_carriage_return_sanitization`, `test_json_value_recursive_redaction`, `test_nvidia_api_key_redaction`, `test_github_and_gitlab_token_redaction`, `test_jwt_and_private_key_redaction`, `test_database_url_credential_redaction`, `test_auth_header_and_env_kv_redaction`, `test_sanitize_error_helper`

---

### `src/telemetry/stream.rs` {#src-telemetry-stream-rs}

- **Source Link:** [`src/telemetry/stream.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/telemetry/stream.rs)
- **Lines of Code:** 162 (5483 bytes)

#### Primary Responsibility
Append-only NDJSON Stream Writer for High-Volume Telemetry (OBS-01, D-01).  Stores raw span events, debug traces, and telemetry payloads in `.m31a/telemetry/&lt;mission_id&gt;.ndjson` without polluting relational SQLite tables.

#### Types & Trait Declarations
- **Structs (1):** `NdjsonStreamWriter`

#### Key Functions & Signatures (9 shown)
```rust
// pub
fn new(base_dir: impl Into<PathBuf>) -> Self;
// pub
fn with_max_bytes(mut self, max_bytes: u64) -> Self;
// pub
fn stream_path(&self, mission_id: &MissionId) -> PathBuf;
// private
async fn ensure_dir(&self) -> std::io::Result<()>;
// private
async fn maybe_rotate(&self, path: &Path, mission_id: &MissionId) -> std::io::Result<()>;
// pub
async fn append_entry(&self,
        mission_id: &MissionId,
        entry: &serde_json::Value,) -> std::io::Result<()>;
// pub
async fn read_entries(&self,
        mission_id: &MissionId,) -> std::io::Result<Vec<serde_json::Value>>;
// private
async fn test_ndjson_append_and_read();
// private
async fn test_ndjson_stream_rotation();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_ndjson_append_and_read`, `test_ndjson_stream_rotation`

---

### `src/telemetry/types.rs` {#src-telemetry-types-rs}

- **Source Link:** [`src/telemetry/types.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/telemetry/types.rs)
- **Lines of Code:** 175 (5072 bytes)

#### Primary Responsibility
Telemetry Domain Types &amp; Models (OBS-01, D-01, D-03).

#### Types & Trait Declarations
- **Structs (3):** `MetricSample`, `TelemetrySpan`, `TelemetrySummary`
- **Enums (2):** `SpanKind`, `SpanStatus`

#### Key Functions & Signatures (6 shown)
```rust
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn new(span_id: String,
        trace_id: String,
        parent_span_id: Option<String>,
        mission_id: MissionId,;
// pub
fn finish(&mut self, end_time_us: i64, status: SpanStatus, error_message: Option<String>);
```

---
