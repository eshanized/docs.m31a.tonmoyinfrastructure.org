# Model & Provider Layer

> **Architectural Layer:** L3 Intelligence  
> **Source Directory:** `src/model`  
> **File Count:** 16 source files  

NVIDIA NIM provider, SSE streaming, model catalog, dynamic discovery, and token usage.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [catalog.rs](#src-model-catalog-rs) | 657 | `ModelCatalog, CatalogRefreshState, CatalogSource` | Dynamic Model Catalog (PRD §01, MDL-01, D-05).  Provides the canonical... |
| [mod.rs](#src-model-mod-rs) | 22 | `Functions/Traits` | Model subsystem.  Owns model provider abstractions, wire protocol seri... |
| [invocation.rs](#src-model-persistence-invocation-rs) | 434 | `ModelInvocationRecord, SqliteModelInvocationRepository` | Durable SQLite repository for ModelInvocation records and token usage ... |
| [mod.rs](#src-model-persistence-mod-rs) | 5 | `Functions/Traits` | Persistence layer for model subsystem records and telemetry (MDL-05). |
| [pricing.rs](#src-model-pricing-rs) | 150 | `ModelPrice` | canonical pricing table and cost calculator for model invocations.  co... |
| [protocol.rs](#src-model-protocol-rs) | 384 | `ToolCallProtocol, ToolCallValidationOutcome` | Layered tool-call protocol, argument extraction, truncation detection,... |
| [endpoint.rs](#src-model-provider-endpoint-rs) | 399 | `ValidatedProviderEndpoint, EndpointTrustError, EndpointTrustSource` | Provider endpoint trust boundary (P0-01).  Invariant: NO CREDENTIAL → ... |
| [mod.rs](#src-model-provider-mod-rs) | 146 | `Functions/Traits` | Provider-neutral abstractions for LLM reasoning and streaming.  Core p... |
| [nvidia.rs](#src-model-provider-nvidia-rs) | 1778 | `NvidiaProvider` | Production NvidiaProvider targeting NVIDIA Build / NIM OpenAI-compatib... |
| [nvidia_metadata.rs](#src-model-provider-nvidia_metadata-rs) | 1215 | `FeaturedModelEntry, FeaturedModelsResponse, NvidiaModelMetadataResolver` | NVIDIA Model Metadata Enrichment Pipeline (Section 1–15).  Provides au... |
| [sse.rs](#src-model-provider-sse-rs) | 1012 | `AccumulatedToolCall, StreamAccumulator` | Asynchronous SSE stream accumulator, OpenAI-compatible JSON event pars... |
| [health.rs](#src-model-router-health-rs) | 554 | `CircuitBreakerRegistry, ModelCircuitBreaker, ModelHealthMetrics` | Runtime-local circuit breaker with semantic failure classification (D-... |
| [mod.rs](#src-model-router-mod-rs) | 11 | `Functions/Traits` | Model routing, circuit breaker health tracking, and recovery subsystem... |
| [recovery.rs](#src-model-router-recovery-rs) | 523 | `ModelRecoveryCoordinator, StepRecoveryDecision` | Two-level bounded model recovery coordinator (D-07, MDL-04).  Level 1:... |
| [resolver.rs](#src-model-router-resolver-rs) | 1088 | `ContextLimits, ModelCandidate, ModelResolutionDetails` | Two-stage deterministic model router with eligibility filtering and ti... |
| [types.rs](#src-model-types-rs) | 544 | `ModelInvocationOptions, ModelToolCall, TokenUsage` | Canonical domain types for model communication, proposals, streaming, ... |

---

### `src/model/catalog.rs` {#src-model-catalog-rs}

- **Source Link:** [`src/model/catalog.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/model/catalog.rs)
- **Lines of Code:** 657 (25642 bytes)

#### Primary Responsibility
Dynamic Model Catalog (PRD §01, MDL-01, D-05).  Provides the canonical in-memory and cached model catalog for the M31A runtime. Represents dynamically discovered provider model capabilities, context limits, availability states, and deterministic fallback selection without hardcoded model lists.

#### Types & Trait Declarations
- **Structs (1):** `ModelCatalog`
- **Enums (3):** `CatalogRefreshState`, `CatalogSource`, `ModelCacheStatus`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn default_catalog_schema_version() -> u32;
// pub
fn new(provider: impl Into<String>) -> Self;
// pub
fn from_discovered(provider: impl Into<String>,
        models: Vec<ModelCandidate>,
        timestamp: u64,) -> Self;
// pub
fn from_cache(provider: impl Into<String>,
        models: Vec<ModelCandidate>,
        timestamp: u64,
        is_stale;
// pub
fn failed_no_cache(provider: impl Into<String>) -> Self;
// pub
fn update_from_provider(&mut self,
        provider: impl Into<String>,
        models: Vec<ModelCandidate>,);
// pub
fn is_empty(&self) -> bool;
// pub
fn len(&self) -> usize;
// pub
fn models_for_tier(&self, tier: ModelTier) -> Vec<&ModelCandidate>;
// pub
fn find_model(&self, model_id: &str) -> Option<&ModelCandidate>;
// pub
fn contains_model(&self, model_id: &str) -> bool;
// pub
fn is_inventory_stale(&self, max_age_secs: u64) -> bool;
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_catalog_exact_context_capacity_roundtrip`, `test_catalog_legacy_unversioned_cache_is_stale`

---

### `src/model/mod.rs` {#src-model-mod-rs}

- **Source Link:** [`src/model/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/model/mod.rs)
- **Lines of Code:** 22 (517 bytes)

#### Primary Responsibility
Model subsystem.  Owns model provider abstractions, wire protocol serialization, SSE streaming, model routing, health management, and token telemetry (MDL-01 to MDL-05).  Core principle: The model proposes. The runtime decides.

---

### `src/model/persistence/invocation.rs` {#src-model-persistence-invocation-rs}

- **Source Link:** [`src/model/persistence/invocation.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/model/persistence/invocation.rs)
- **Lines of Code:** 434 (15693 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Durable SQLite repository for ModelInvocation records and token usage telemetry (D-08, MDL-05).  Maps to the `model_invocations` table created in Migration 005.

#### Types & Trait Declarations
- **Structs (2):** `ModelInvocationRecord`, `SqliteModelInvocationRepository`

#### Key Functions & Signatures (12 shown)
```rust
// pub
fn new(mission_id: MissionId,
        task_id: TaskId,
        agent_id: AgentId,
        step_number: u32,
        prov;
// pub
fn with_prompt_provenance(mut self, provenance: impl Into<String>) -> Self;
// pub
fn with_cost(mut self, cost_usd: Option<f64>, provenance: CostProvenance) -> Self;
// pub
fn new(pool: SqlitePool) -> Self;
// pub
async fn insert_invocation(&self,
        record: &ModelInvocationRecord,) -> Result<(), sqlx::Error>;
// pub
async fn get_invocations_for_task(&self,
        task_id: &TaskId,) -> Result<Vec<ModelInvocationRecord>, sqlx::Error>;
// pub
async fn get_invocations_for_mission(&self,
        mission_id: &MissionId,) -> Result<Vec<ModelInvocationRecord>, sqlx:;
// pub
async fn get_total_token_usage_for_mission(&self,
        mission_id: &MissionId,) -> Result<TokenUsage, sqlx::Error>;
// pub
async fn get_all_invocations(&self) -> Result<Vec<ModelInvocationRecord>, sqlx::Error>;
// private
fn map_row_to_invocation(row: SqliteRow) -> Result<ModelInvocationRecord, sqlx::Error>;
// private
async fn seed_test_parents(pool: &SqlitePool,
        mission_id: &MissionId,
        task_id: &TaskId,
        agent_id;
// private
async fn test_sqlite_model_invocation_crud();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_sqlite_model_invocation_crud`

---

### `src/model/persistence/mod.rs` {#src-model-persistence-mod-rs}

- **Source Link:** [`src/model/persistence/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/model/persistence/mod.rs)
- **Lines of Code:** 5 (119 bytes)

#### Primary Responsibility
Persistence layer for model subsystem records and telemetry (MDL-05).

---

### `src/model/pricing.rs` {#src-model-pricing-rs}

- **Source Link:** [`src/model/pricing.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/model/pricing.rs)
- **Lines of Code:** 150 (5398 bytes)

#### Primary Responsibility
canonical pricing table and cost calculator for model invocations.  computes estimated cost when the provider does not supply authoritative cost. never returns synthetic 0.00 for unknown commercial models; unknown models yield (None, CostProvenance::Unknown).

#### Types & Trait Declarations
- **Structs (1):** `ModelPrice`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn calculate_cost_usd(&self, prompt_tokens: usize, completion_tokens: usize) -> f64;
// pub
fn lookup_price(provider: &str, model: &str) -> Option<ModelPrice>;
// pub
fn calculate_cost(provider: &str,
    model: &str,
    prompt_tokens: usize,
    completion_tokens: usize,) -> (Option<f;
// pub
fn calculate_cost_from_usage(provider: &str,
    model: &str,
    usage: &crate::model::types::TokenUsage,) -> (Option<f;
// private
fn test_unknown_models_return_none_and_unknown_provenance();
// private
fn test_known_models_and_local_models_pricing();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_unknown_models_return_none_and_unknown_provenance`, `test_known_models_and_local_models_pricing`

---

### `src/model/protocol.rs` {#src-model-protocol-rs}

- **Source Link:** [`src/model/protocol.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/model/protocol.rs)
- **Lines of Code:** 384 (13144 bytes)

#### Primary Responsibility
Layered tool-call protocol, argument extraction, truncation detection, and constrained safe recovery (P3-B, MDL-01, MDL-03).

#### Types & Trait Declarations
- **Structs (1):** `ToolCallProtocol`
- **Enums (1):** `ToolCallValidationOutcome`

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn process_arguments(raw_args: &str,
        finish_reason: Option<&str>,) -> ToolCallValidationOutcome;
// pub
fn detect_unclosed_delimiters(text: &str) -> bool;
// pub
fn attempt_safe_recovery(raw: &str) -> Option<(Value, String)>;
// private
fn extract_from_markdown_or_quotes(text: &str) -> Option<String>;
// private
fn test_valid_json();
// private
fn test_empty_or_null_json();
// private
fn test_truncated_json_recoveries();
// private
fn test_markdown_codeblock_extraction();
// private
fn test_syntax_error_unrecoverable();
// private
fn test_token_limit_length_truncation();
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_valid_json`, `test_empty_or_null_json`, `test_truncated_json_recoveries`, `test_markdown_codeblock_extraction`, `test_syntax_error_unrecoverable`, `test_token_limit_length_truncation`

---

### `src/model/provider/endpoint.rs` {#src-model-provider-endpoint-rs}

- **Source Link:** [`src/model/provider/endpoint.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/model/provider/endpoint.rs)
- **Lines of Code:** 399 (15142 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Provider endpoint trust boundary (P0-01).  Invariant: NO CREDENTIAL → BEFORE ENDPOINT TRUST.  A repository-controlled workspace configuration must never be able to redirect a credential-bearing production provider request to an attacker-controlled URL. Endpoint authorization happens before any credential is loaded or attached, and every credential-bearing HTTP request site must go through a [`ValidatedProviderEndpoint`].  Trust tiers: - [`EndpointTrustSource::BuiltinDefault`] — immutable canonical default. - [`EndpointTrustSource::System`] — `/etc/m31a/config.toml` (trusted admin). - [`EndpointTrustSource::User`] — `~/.config/m31a/config.toml` (trusted user). - [`EndpointTrustSource::ExplicitCli`] — explicit `--config &lt;path&gt;` (trusted operator intent). - [`EndpointTrustSource::Workspace`] — `&lt;ws&gt;/.m31a/config.toml` (UNTRUSTED repository content). - [`EndpointTrustSource::SessionOverride`] — generic session overlay (untrusted by default).  Policy (production): - Canonical `https://integrate.api.nvidia.com/v1` is always trusted. - Any custom endpoint carrying a real credential MUST come from a trusted tier (System/User/ExplicitCli/BuiltinDefault). Workspace/Session custom endpoints are rejected when a real credential would be attached. - Custom endpoints must be `https://` (fail closed on `http://`), must parse, and must not target blocked destinations (loopback/RFC1918/ link-local/metadata/host aliases). Full DNS validation happens in [`ValidatedProviderEndpoint::authorize_for_credential`] before use.

#### Types & Trait Declarations
- **Structs (1):** `ValidatedProviderEndpoint`
- **Enums (2):** `EndpointTrustError`, `EndpointTrustSource`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn url(&self) -> &str;
// pub
fn source(&self) -> EndpointTrustSource;
// pub
fn is_canonical(&self) -> bool;
// pub
fn credential_permitted(&self) -> bool;
// pub
fn require_credential_permitted(&self) -> Result<&str, EndpointTrustError>;
// pub
fn is_test_credential(key: &str) -> bool;
// private
fn normalize(url: &str) -> String;
// pub
fn is_canonical_endpoint(url: &str) -> bool;
// pub
fn validate_nvidia_endpoint(base_url: Option<String>,
    source: EndpointTrustSource,) -> Result<ValidatedProviderEndpo;
// pub
async fn authorize_for_credential(mut self) -> Result<Self, EndpointTrustError>;
// private
fn canonical_endpoint_always_trusted_from_any_tier();
// private
fn workspace_custom_endpoint_rejected_for_credentials();
// private
fn trusted_tier_custom_https_endpoint_shape_accepted_pending_dns();
// private
fn http_custom_endpoint_rejected_even_from_trusted_tier();
// private
fn loopback_and_private_literals_rejected();
```

#### Unit Verification (7 inline tests)
Tests defined within module:
`canonical_endpoint_always_trusted_from_any_tier`, `workspace_custom_endpoint_rejected_for_credentials`, `trusted_tier_custom_https_endpoint_shape_accepted_pending_dns`, `http_custom_endpoint_rejected_even_from_trusted_tier`, `loopback_and_private_literals_rejected`, `destination_authorization_binds_dns_before_credential`, `blocked_destination_fails_closed_on_authorize`

---

### `src/model/provider/mod.rs` {#src-model-provider-mod-rs}

- **Source Link:** [`src/model/provider/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/model/provider/mod.rs)
- **Lines of Code:** 146 (5785 bytes)
- **Runtime Properties:** 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Provider-neutral abstractions for LLM reasoning and streaming.  Core principle: The model proposes. The runtime decides. (MDL-01, Law 1)

#### Types & Trait Declarations
- **Traits (1):** `ModelProvider`

#### Key Functions & Signatures (10 shown)
```rust
// private
async fn call_model(&self,
        model_name: &str,
        system_prompt: &str,
        tools: Vec<serde_json::Value>,;
// private
async fn call_model_with_messages(&self,
        _model_name: &str,
        _messages: &[crate::model::types::ChatMessag;
// private
async fn call_model_with_options(&self,
        model_name: &str,
        system_prompt: &str,
        tools: Vec<serde_;
// private
async fn call_model_with_messages_streaming(&self,
        _model_name: &str,
        _messages: &[crate::model::types::;
// private
async fn call_model_with_messages_streaming_options(&self,
        model_name: &str,
        messages: &[crate::model::t;
// private
async fn stream_model(&self,
        model_name: &str,
        system_prompt: &str,
        tools: Vec<serde_json::Value;
// private
async fn stream_model_with_messages(&self,
        _model_name: &str,
        _messages: &[crate::model::types::ChatMess;
// private
async fn discover_models(&self,) -> Result<Vec<crate::model::router::resolver::ModelCandidate>, ModelError>;
// private
fn is_test_double(&self) -> bool;
// private
fn provider_name(&self) -> &'static str;
```

---

### `src/model/provider/nvidia.rs` {#src-model-provider-nvidia-rs}

- **Source Link:** [`src/model/provider/nvidia.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/model/provider/nvidia.rs)
- **Lines of Code:** 1778 (66954 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Production NvidiaProvider targeting NVIDIA Build / NIM OpenAI-compatible API surface (D-01, MDL-01, MDL-03).  Connects to NVIDIA NIM endpoints via async SSE streaming. Enforces side-effect prohibition: returns validated ModelProposal for runtime decision.

#### Types & Trait Declarations
- **Structs (1):** `NvidiaProvider`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn record_live_provider_event(event: &str);
// private
fn record_live_provider_event(_event: &str);
// private
fn validate_chat_completion_body(body: &Value) -> Result<(), ModelError>;
// private
fn explicit_tier(item: &serde_json::Value,) -> Option<(crate::model::router::resolver::ModelTier, &'static str)>;
// pub
fn extract_context_capacity(item: &serde_json::Value) -> (usize, &'static str);
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn parse_model_candidate(item: &Value,
        now_secs: u64,) -> Option<crate::model::router::resolver::ModelCandidate>;
// pub
fn new(base_url: Option<String>, api_key: Option<String>) -> Result<Self, ModelError>;
// pub
fn new_governed(base_url: Option<String>,
        api_key: Option<String>,
        source: EndpointTrustSource,) -> Resu;
// pub
fn new_test_fixture(base_url: String, api_key: String) -> Result<Self, ModelError>;
// private
fn construct(base_url: Option<String>,
        api_key: Option<String>,
        source: EndpointTrustSource,) -> Result<;
// pub
fn with_request_tracer(mut self, tracer: RequestTraceHook) -> Self;
// pub
fn with_metadata_resolver(mut self,
        resolver: Arc<crate::model::provider::nvidia_metadata::NvidiaModelMetadataRe;
// pub
fn metadata_resolver(&self,) -> &Arc<crate::model::provider::nvidia_metadata::NvidiaModelMetadataResolver>;
// pub
fn with_client(client: Client,
        base_url: Option<String>,
        api_key: Option<String>,) -> Result<Self, Model;
```

#### Unit Verification (23 inline tests)
Tests defined within module:
`test_validate_chat_completion_accepts_nonempty_text`, `test_validate_chat_completion_accepts_tool_calls`, `test_validate_chat_completion_rejects_missing_or_empty_choices`, `test_validate_chat_completion_rejects_missing_message`, `test_validate_chat_completion_rejects_empty_content_without_tool_calls`, `test_provider_instantiation_with_defaults`, `test_provider_instantiation_trims_trailing_slash`, `test_provider_instantiation_fails_without_key`, `test_build_chat_request_payload_without_tools`, `test_build_chat_request_payload_with_tools`...

---

### `src/model/provider/nvidia_metadata.rs` {#src-model-provider-nvidia_metadata-rs}

- **Source Link:** [`src/model/provider/nvidia_metadata.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/model/provider/nvidia_metadata.rs)
- **Lines of Code:** 1215 (46979 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
NVIDIA Model Metadata Enrichment Pipeline (Section 1–15).  Provides authoritative per-model capability normalization, official NVIDIA model reference metadata enrichment, and capability provenance tracking.  Architecture: ```text /v1/models (Inventory) ↓ canonical model inventory ↓ metadata enrichment (NvidiaModelMetadataResolver) ↓ capability normalization ↓ ModelCandidate (with explicit ContextLimits &amp; CapabilitySupport) ↓ ModelCatalog ↓ Router / Wizard / TUI ```

#### Types & Trait Declarations
- **Structs (4):** `FeaturedModelEntry`, `FeaturedModelsResponse`, `NvidiaModelMetadataResolver`, `NvidiaModelReferenceRecord`
- **Traits (1):** `ProviderModelMetadataSource`

#### Key Functions & Signatures (15 shown)
```rust
// private
async fn enrich_candidate(&self, candidate: &mut ModelCandidate) -> Result<(), ModelError>;
// private
async fn enrich_candidates(&self, candidates: &mut [ModelCandidate]) -> Result<(), ModelError>;
// pub
fn new(model_id: impl Into<String>,
        context_length: usize,
        model_kind: ModelKind,
        tool_calling: ;
// pub
fn with_display_name(mut self, name: impl Into<String>) -> Self;
// pub
fn with_max_output(mut self, max_tokens: usize) -> Self;
// pub
fn with_modalities(mut self, modalities: Vec<String>) -> Self;
// pub
fn new() -> Self;
// pub
fn new_offline() -> Self;
// pub
fn with_featured_models_url(mut self, url: impl Into<String>) -> Self;
// pub
fn with_remote_enrichment(mut self, enabled: bool) -> Self;
// pub
fn register_reference(&mut self, record: NvidiaModelReferenceRecord);
// pub
fn reference_record(&self, model_id: &str) -> Option<&NvidiaModelReferenceRecord>;
// pub
fn lookup_reference(&self, model_id: &str) -> Option<ModelCandidate>;
// private
fn load_official_nvidia_references(&mut self);
// private
async fn get_remote_featured_models(&self) -> HashMap<String, FeaturedModelEntry>;
```

---

### `src/model/provider/sse.rs` {#src-model-provider-sse-rs}

- **Source Link:** [`src/model/provider/sse.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/model/provider/sse.rs)
- **Lines of Code:** 1012 (37581 bytes)

#### Primary Responsibility
Asynchronous SSE stream accumulator, OpenAI-compatible JSON event parser, and HTTP error normalizer (D-02, D-03, D-04).

#### Types & Trait Declarations
- **Structs (2):** `AccumulatedToolCall`, `StreamAccumulator`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn reasoning_text(&self) -> &str;
// pub
fn process_event(&mut self, event_data: &str) -> Result<Vec<StreamChunk>, ModelError>;
// pub
fn finalize(self) -> Result<(ModelProposal, TokenUsage), ModelError>;
// private
fn try_parse_action_envelope(val: &Value) -> Option<ModelProposal>;
// private
fn extract_json_codeblock(text: &str) -> Option<String>;
// private
fn extract_embedded_action(text: &str) -> Option<ModelProposal>;
// pub
fn normalize_http_error(status: u16, body: &str) -> ModelError;
// private
fn sanitize_credentials(text: &str) -> String;
// private
fn extract_cooldown_seconds(body: &str) -> Option<u64>;
// private
fn extract_context_window_numbers(lower_body: &str) -> (usize, usize);
// private
fn test_single_and_multi_chunk_text_streaming();
// private
fn test_multi_chunk_fragmented_tool_call_accumulation();
// private
fn test_malformed_tool_call_json_arguments();
// private
fn test_empty_stream_done_handling();
```

#### Unit Verification (10 inline tests)
Tests defined within module:
`test_single_and_multi_chunk_text_streaming`, `test_multi_chunk_fragmented_tool_call_accumulation`, `test_malformed_tool_call_json_arguments`, `test_empty_stream_done_handling`, `test_fallback_envelope_parsing`, `test_reasoning_content_tracked_without_polluting_answer`, `test_reasoning_only_stream_rejected_as_empty`, `test_whitespace_only_stream_rejected_as_empty`, `test_normalize_http_errors`, `test_normalize_http_error_credential_redaction`

---

### `src/model/router/health.rs` {#src-model-router-health-rs}

- **Source Link:** [`src/model/router/health.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/model/router/health.rs)
- **Lines of Code:** 554 (21710 bytes)

#### Primary Responsibility
Runtime-local circuit breaker with semantic failure classification (D-06, MDL-04).  Tracks model/endpoint health across Healthy, Degraded, Open, and HalfOpen states. Strictly enforces that client-side bugs (400 Bad Request, 401 Unauthorized, etc.) never degrade provider health or trip circuit breakers.

#### Types & Trait Declarations
- **Structs (3):** `CircuitBreakerRegistry`, `ModelCircuitBreaker`, `ModelHealthMetrics`
- **Enums (2):** `CircuitState`, `FailureKind`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn from_model_error(error: &ModelError) -> Self;
// pub
fn new(endpoint: impl Into<String>, model_name: impl Into<String>) -> Self;
// pub
fn with_failure_threshold(mut self, threshold: u32) -> Self;
// pub
fn check_admission(&mut self) -> Result<(), ModelError>;
// pub
fn check_admission_at(&mut self, now: DateTime<Utc>) -> Result<(), ModelError>;
// pub
fn record_success(&mut self);
// pub
fn record_failure(&mut self, error: &ModelError);
// pub
fn record_failure_at(&mut self, error: &ModelError, now: DateTime<Utc>);
// pub
fn state(&self) -> CircuitState;
// pub
fn consecutive_failures(&self) -> u32;
// pub
fn cooldown_until(&self) -> Option<DateTime<Utc>>;
// pub
fn last_failure_reason(&self) -> Option<&str>;
// private
fn default() -> Self;
// pub
fn new() -> Self;
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_bad_request_does_not_trip_circuit`, `test_consecutive_503_transitions_healthy_to_degraded_to_open`, `test_429_immediately_opens_circuit_with_cooldown`, `test_cooldown_expiry_enables_half_open_probe_and_recovery`, `test_circuit_breaker_registry_inspection_and_updates`

---

### `src/model/router/mod.rs` {#src-model-router-mod-rs}

- **Source Link:** [`src/model/router/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/model/router/mod.rs)
- **Lines of Code:** 11 (300 bytes)

#### Primary Responsibility
Model routing, circuit breaker health tracking, and recovery subsystem (MDL-02, MDL-04).  Enforces deterministic two-stage model resolution and runtime-local circuit health.

---

### `src/model/router/recovery.rs` {#src-model-router-recovery-rs}

- **Source Link:** [`src/model/router/recovery.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/model/router/recovery.rs)
- **Lines of Code:** 523 (17505 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Two-level bounded model recovery coordinator (D-07, MDL-04).  Level 1: In-step transient retry loop strictly bounded by configured budget (default 2 retries). Level 2: Persistent failure or retry exhaustion escalates to Model Fallback via ModelRouter. Fallback re-evaluates hard capability requirements and NEVER weakens task or role constraints (T-07-06).

#### Types & Trait Declarations
- **Structs (1):** `ModelRecoveryCoordinator`
- **Enums (1):** `StepRecoveryDecision`

#### Key Functions & Signatures (14 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_bounds(mut self, max_in_step_retries: u32, max_model_fallbacks: u32) -> Self;
// pub
fn max_in_step_retries(&self) -> u32;
// pub
fn max_model_fallbacks(&self) -> u32;
// pub
fn handle_step_failure(&self,
        current_attempt: u32,
        fallback_count: u32,
        error: &ModelError,
   ;
// pub
async fn record_telemetry_attempt(telemetry: &SqliteModelInvocationRepository,
        mission_id: MissionId,
        ta;
// private
fn test_candidates() -> Vec<ModelCandidate>;
// private
fn test_level_1_transient_failure_retries_in_step();
// private
fn test_level_1_retry_exhaustion_escalates_to_level_2_fallback();
// private
fn test_circuit_open_immediately_escalates_to_level_2_fallback();
// private
fn test_fallback_fails_closed_when_hard_constraints_not_met();
// private
async fn seed_test_parents(pool: &sqlx::SqlitePool,
        mission_id: &MissionId,
        task_id: &TaskId,
        ag;
// private
async fn test_telemetry_recording_helper();
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_level_1_transient_failure_retries_in_step`, `test_level_1_retry_exhaustion_escalates_to_level_2_fallback`, `test_circuit_open_immediately_escalates_to_level_2_fallback`, `test_fallback_fails_closed_when_hard_constraints_not_met`, `test_telemetry_recording_helper`

---

### `src/model/router/resolver.rs` {#src-model-router-resolver-rs}

- **Source Link:** [`src/model/router/resolver.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/model/router/resolver.rs)
- **Lines of Code:** 1088 (40658 bytes)

#### Primary Responsibility
Two-stage deterministic model router with eligibility filtering and tier ranking (D-05, MDL-02).  Stage 1: Derives model requirements from AgentProfile/RoutingRequest and applies hard capability filters (tool calling, context capacity, circuit health, budget bounds).  Stage 2: Deterministically ranks eligible candidates by tier suitability, operational health, cost preference, and stable model ID tie-breaking.

#### Types & Trait Declarations
- **Structs (6):** `ContextLimits`, `ModelCandidate`, `ModelResolutionDetails`, `ModelRouter`, `ResolvedModelSelection`, `RoutingRequest`
- **Enums (5):** `CapabilitySupport`, `ModelKind`, `ModelResolutionError`, `ModelRole`, `ModelTier`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default_candidate_availability() -> ProviderCapabilityStatus;
// private
fn default_candidate_source() -> String;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn is_supported(&self) -> bool;
// pub
fn is_unsupported(&self) -> bool;
// pub
fn is_unknown(&self) -> bool;
// private
fn from(b: bool) -> Self;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn is_embedding(&self) -> bool;
// pub
fn is_image_generation(&self) -> bool;
// pub
fn is_safety_guard(&self) -> bool;
// pub
fn is_text_or_code_generation(&self) -> bool;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(model_id: impl Into<String>,
        provider: impl Into<String>,
        tier: ModelTier,
        context_capaci;
// pub
fn with_display_name(mut self, name: impl Into<String>) -> Self;
```

#### Unit Verification (8 inline tests)
Tests defined within module:
`test_hard_filter_eliminates_insufficient_context`, `test_hard_filter_eliminates_missing_tool_support`, `test_circuit_breaker_open_rejected_in_stage_1`, `test_expired_cooldown_readmits_model_in_stage_1`, `test_role_temperature_follows_profile_registry`, `test_tier_matching_ranks_preferred_tier_first`, `test_tie_breaking_is_completely_deterministic`, `test_fails_closed_when_all_candidates_disqualified`

---

### `src/model/types.rs` {#src-model-types-rs}

- **Source Link:** [`src/model/types.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/model/types.rs)
- **Lines of Code:** 544 (19491 bytes)

#### Primary Responsibility
Canonical domain types for model communication, proposals, streaming, and error classification.  Core principle: The model proposes. The runtime decides. (MDL-01, MDL-03)

#### Types & Trait Declarations
- **Structs (4):** `ModelInvocationOptions`, `ModelToolCall`, `TokenUsage`, `UserOption`
- **Enums (7):** `ChatMessage`, `CostProvenance`, `ModelError`, `ModelProposal`, `ProviderCapabilityStatus`, `StreamChunk`, `UsageSource`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn is_completion(&self) -> bool;
// pub
fn tool_calls(&self) -> Vec<ModelToolCall>;
// pub
fn text_content(&self) -> Option<&str>;
// pub
fn kind_name(&self) -> &'static str;
// pub
fn tool_names(&self) -> Vec<String>;
// pub
fn tool_calls_count(&self) -> usize;
// pub
fn new(name: impl Into<String>, arguments: serde_json::Value) -> Self;
// pub
fn with_id(id: impl Into<String>,
        name: impl Into<String>,
        arguments: serde_json::Value,) -> Self;
// pub
fn new(prompt_tokens: usize,
        completion_tokens: usize,
        total_tokens: usize,
        reasoning_tokens: us;
// pub
fn accumulate(&mut self, other: &Self);
// pub
fn new() -> Self;
// pub
fn with_max_output_tokens(mut self, max_tokens: usize) -> Self;
// pub
fn with_temperature(mut self, temp: f32) -> Self;
// pub
fn with_top_p(mut self, top_p: f32) -> Self;
// pub
fn as_str(&self) -> &'static str;
```

#### Unit Verification (9 inline tests)
Tests defined within module:
`test_model_proposal_serialization_tool_calls_single`, `test_model_proposal_serialization_tool_calls_multiple`, `test_model_proposal_serialization_assistant_text`, `test_model_proposal_serialization_ask_user`, `test_model_proposal_serialization_handoff`, `test_model_proposal_serialization_complete`, `test_stream_chunk_serialization`, `test_token_usage_defaults_and_construction`, `test_model_error_formatting`

---
