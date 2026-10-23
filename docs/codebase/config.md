# Configuration Engine

> **Architectural Layer:** L1 Configuration  
> **Source Directory:** `src/config`  
> **File Count:** 11 source files  

8-tier hierarchical configuration precedence, strict schema validation, canonical defaults, and provenance.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [canonical.rs](#src-config-canonical-rs) | 241 | `ModelCatalogCachePolicy, ResourcePolicy, TimeoutPolicy` | Single authoritative configuration defaults (CFG-01).  This module is ... |
| [env.rs](#src-config-env-rs) | 78 | `SafeEnvironmentStatus` | Secure environment configuration status (CFG-01, CFG-03).  Production ... |
| [hierarchy.rs](#src-config-hierarchy-rs) | 126 | `ConfigPrecedenceEngine, ConfigTier` | 7-Tier Hierarchical Configuration Engine (CFG-01, D-12). |
| [merge.rs](#src-config-merge-rs) | 245 | `MonotonicSecurityMerger, ConfigError` | TOML Merging &amp; Monotonic Security Accumulation (CFG-01, D-12, THRE... |
| [mod.rs](#src-config-mod-rs) | 37 | `Functions/Traits` | Hierarchical Configuration Engine &amp; Validation (CFG-01–CFG-04, D-1... |
| [paths.rs](#src-config-paths-rs) | 230 | `PlatformPaths` | Platform-Aware Configuration &amp; Data Directories (CFG-03, D-14).  C... |
| [profile.rs](#src-config-profile-rs) | 265 | `ProfileConfig, ProfileResolver` | Composable Configuration Profiles &amp; Single Inheritance (CFG-04). |
| [provenance.rs](#src-config-provenance-rs) | 292 | `ConfigurationService, LayerEntry, ResolvedValue` | 7-Layer Configuration Provenance &amp; Immutable Constraint Protection... |
| [provider_registry.rs](#src-config-provider_registry-rs) | 960 | `MaskedSecret, ProviderDescriptor, ProviderProbeReport` | NVIDIA-NIM-Only Provider Registry &amp; Masked Secret Boundaries (CFX-... |
| [resolved.rs](#src-config-resolved-rs) | 1345 | `ConfigExplain, ResolvedConfigBuilder, ResolvedConfiguration` | Unified Authoritative Configuration Control Plane (CFG-01..04).  Provi... |
| [schema.rs](#src-config-schema-rs) | 1085 | `AgentsConfig, AppConfig, CacheConfig` | Strict Configuration Schema &amp; Validation (CFG-02, D-13). |

---

### `src/config/canonical.rs` {#src-config-canonical-rs}

- **Source Link:** [`src/config/canonical.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/config/canonical.rs)
- **Lines of Code:** 241 (10636 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Single authoritative configuration defaults (CFG-01).  This module is the ONLY place where ordinary runtime defaults live. Every other subsystem consumes these values via the configuration resolver ([`crate::config::ResolvedConfiguration`]) — never by re-stating the literal.  Split of responsibilities: - Configurable defaults → here (consumed by `schema.rs` `default_*` fns). - Immutable security floors / protocol constants → remain in code at their owning security layer (e.g. endpoint trust, egress policy, sandbox ceilings, query ceilings). - Serialization compatibility defaults → near the schema.  Lower layers MUST NOT `unwrap_or("&lt;literal&gt;")` for any value listed here. They receive the resolved value from `ResolvedConfiguration` or fail closed.

#### Types & Trait Declarations
- **Structs (3):** `ModelCatalogCachePolicy`, `ResourcePolicy`, `TimeoutPolicy`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn normalize_objective(input: Option<&str>) -> Option<String>;
// private
fn default() -> Self;
// private
fn default() -> Self;
// private
fn default() -> Self;
```

---

### `src/config/env.rs` {#src-config-env-rs}

- **Source Link:** [`src/config/env.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/config/env.rs)
- **Lines of Code:** 78 (3267 bytes)

#### Primary Responsibility
Secure environment configuration status (CFG-01, CFG-03).  Production credential rule: production code under `src/` MUST NOT discover LLM API keys through the process environment and MUST NOT load `.env` files. The single production credential authority is [`crate::runtime_authorities::resolve_runtime_credentials`] (canonical channel-isolated credential store → legacy workspace migration file, and nothing else).  `.env` loading and LLM API-key environment reads for explicitly opted-in live-model testing live exclusively under `tests/support/` (see `tests/support/credentials.rs`). They are never part of the production library.  The only environment values consulted here are NON-SECRET, explicitly supported Tier-5 configuration overrides (model selection display only). Secrets (API keys, tokens) are NEVER logged or printed.

#### Types & Trait Declarations
- **Structs (1):** `SafeEnvironmentStatus`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn probe() -> Self;
// pub
fn probe_workspace(workspace_root: &Path) -> Self;
// pub
fn log_status(&self);
```

---

### `src/config/hierarchy.rs` {#src-config-hierarchy-rs}

- **Source Link:** [`src/config/hierarchy.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/config/hierarchy.rs)
- **Lines of Code:** 126 (4589 bytes)

#### Primary Responsibility
7-Tier Hierarchical Configuration Engine (CFG-01, D-12).

#### Types & Trait Declarations
- **Structs (1):** `ConfigPrecedenceEngine`
- **Enums (1):** `ConfigTier`

#### Key Functions & Signatures (9 shown)
```rust
// pub
fn name(&self) -> &'static str;
// pub
fn new() -> Self;
// pub
fn set_layer(&mut self, tier: ConfigTier, value: toml::Value);
// pub
fn set_layer_from_str(&mut self,
        tier: ConfigTier,
        toml_str: &str,) -> Result<(), ConfigError>;
// pub
fn remove_layer(&mut self, tier: ConfigTier) -> Option<toml::Value>;
// pub
fn has_layer(&self, tier: ConfigTier) -> bool;
// pub
fn get_layer(&self, tier: ConfigTier) -> Option<&toml::Value>;
// pub
fn resolve_raw(&self) -> Result<toml::Value, ConfigError>;
// pub
fn resolve(&self) -> Result<T, ConfigError>;
```

---

### `src/config/merge.rs` {#src-config-merge-rs}

- **Source Link:** [`src/config/merge.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/config/merge.rs)
- **Lines of Code:** 245 (10311 bytes)

#### Primary Responsibility
TOML Merging &amp; Monotonic Security Accumulation (CFG-01, D-12, THREAT-05).

#### Types & Trait Declarations
- **Structs (1):** `MonotonicSecurityMerger`
- **Enums (1):** `ConfigError`

#### Key Functions & Signatures (3 shown)
```rust
// private
fn from(err: crate::config::schema::ConfigValidationError) -> Self;
// pub
fn deep_merge_toml(base: &mut toml::Value, overlay: toml::Value);
// pub
fn check(base: &toml::Value, overlay: &toml::Value) -> Result<(), ConfigError>;
```

---

### `src/config/mod.rs` {#src-config-mod-rs}

- **Source Link:** [`src/config/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/config/mod.rs)
- **Lines of Code:** 37 (1439 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Hierarchical Configuration Engine &amp; Validation (CFG-01–CFG-04, D-12–D-14).

---

### `src/config/paths.rs` {#src-config-paths-rs}

- **Source Link:** [`src/config/paths.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/config/paths.rs)
- **Lines of Code:** 230 (8236 bytes)

#### Primary Responsibility
Platform-Aware Configuration &amp; Data Directories (CFG-03, D-14).  Compatibility layer over the canonical storage authority ([`crate::storage::StorageLayout`] / [`crate::deployment::DeploymentPaths`]). Global directory resolution delegates to `DeploymentPaths`; only legacy fallback file locations (`.m31`, `/etc/m31`) remain here as explicit migration boundaries.

#### Types & Trait Declarations
- **Structs (1):** `PlatformPaths`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn for_channel(channel: crate::deployment::DeploymentChannel) -> Self;
// pub
fn channel(&self) -> crate::deployment::DeploymentChannel;
// private
fn deployment_paths(&self) -> &crate::deployment::DeploymentPaths;
// pub
fn config_dir(&self) -> PathBuf;
// pub
fn data_dir(&self) -> PathBuf;
// pub
fn cache_dir(&self) -> PathBuf;
// pub
fn state_dir(&self) -> PathBuf;
// pub
fn system_config_dir(&self) -> PathBuf;
// pub
fn user_config_file(&self) -> PathBuf;
// pub
fn system_config_file(&self) -> PathBuf;
// pub
fn canonical_workspace_config_file(workspace_root: &Path) -> PathBuf;
// pub
fn workspace_config_candidates(workspace_root: &Path) -> Vec<PathBuf>;
// pub
fn workspace_config_file(workspace_root: &Path) -> PathBuf;
```

---

### `src/config/profile.rs` {#src-config-profile-rs}

- **Source Link:** [`src/config/profile.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/config/profile.rs)
- **Lines of Code:** 265 (9355 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Composable Configuration Profiles &amp; Single Inheritance (CFG-04).

#### Types & Trait Declarations
- **Structs (2):** `ProfileConfig`, `ProfileResolver`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_canonical_profiles() -> Self;
// pub
fn register_profile(&mut self, name: &str, profile_toml: toml::Value);
// private
fn register_canonical_profiles(&mut self);
// pub
fn resolve_profile(&self, profile_name: &str) -> Result<toml::Value, ConfigError>;
// private
fn resolve_profile_recursive(&self,
        profile_name: &str,
        visited: &mut HashSet<String>,) -> Result<toml::;
// pub
fn apply_to_app_config(&self,
        profile_name: &str,
        mut base_config_toml: toml::Value,) -> Result<AppConfi;
// pub
fn canonical_profile_names() -> &'static [&'static str];
// pub
fn canonical_autonomy_for_profile(profile_name: &str) -> Result<String, ConfigError>;
// pub
fn canonical_metadata_for_profile(profile_name: &str) -> Result<toml::Value, ConfigError>;
// pub
fn is_canonical_profile(profile_name: &str) -> bool;
// private
fn normalize_profile_name(name: &str) -> String;
// private
fn hyphenated_profile_aliases_resolve_to_canonical_profiles();
// private
fn profile_names_are_normalized_when_registered_and_resolved();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`hyphenated_profile_aliases_resolve_to_canonical_profiles`, `profile_names_are_normalized_when_registered_and_resolved`, `canonical_profile_inventory_excludes_aliases`

---

### `src/config/provenance.rs` {#src-config-provenance-rs}

- **Source Link:** [`src/config/provenance.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/config/provenance.rs)
- **Lines of Code:** 292 (10274 bytes)

#### Primary Responsibility
7-Layer Configuration Provenance &amp; Immutable Constraint Protection (CFX-04, D-07).  Enforces the 7-tier precedence hierarchy (CLI &gt; Session &gt; Mission &gt; Workspace &gt; User &gt; System &gt; BuiltIn) and prevents lower-precedence configuration layers from weakening immutable safety constraints.

#### Types & Trait Declarations
- **Structs (3):** `ConfigurationService`, `LayerEntry`, `ResolvedValue`
- **Enums (2):** `ConfigLayer`, `ProvenanceError`

#### Key Functions & Signatures (11 shown)
```rust
// pub
fn precedence(&self) -> u8;
// pub
fn display_name(&self) -> &'static str;
// pub
fn badge(&self) -> &'static str;
// private
fn from(layer: ConfigLayer) -> Self;
// private
fn from(tier: ConfigTier) -> Self;
// pub
fn new() -> Self;
// pub
fn set_value(&mut self,
        layer: ConfigLayer,
        key: &str,
        value: serde_json::Value,
        source_;
// pub
fn resolve(&self, key: &str) -> Option<ResolvedValue>;
// pub
fn all_resolved(&self) -> Vec<ResolvedValue>;
// pub
fn grouped_by_domain(&self) -> BTreeMap<String, Vec<ResolvedValue>>;
// pub
fn get_all_entries_for_key(&self,
        key: &str,) -> Vec<(ConfigLayer, serde_json::Value, Option<PathBuf>, bool)>;
```

---

### `src/config/provider_registry.rs` {#src-config-provider_registry-rs}

- **Source Link:** [`src/config/provider_registry.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/config/provider_registry.rs)
- **Lines of Code:** 960 (36959 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
NVIDIA-NIM-Only Provider Registry &amp; Masked Secret Boundaries (CFX-01, CFX-02, D-08).  NVIDIA NIM is the sole production model provider in the current release. The registry retains retired provider descriptors (OpenAI, Anthropic, Gemini, OpenAI-Compatible/Local) exclusively so that ordinary configuration, `/model` selection, and environment resolution can reject them deterministically with a precise NVIDIA-only error. Retired entries are never exposed through production surfaces (`production_descriptors`, setup wizard, `/model`, model selector). `Mock` remains strictly as test infrastructure and is unreachable from normal user interaction.

#### Types & Trait Declarations
- **Structs (4):** `MaskedSecret`, `ProviderDescriptor`, `ProviderProbeReport`, `ProviderRegistry`
- **Enums (2):** `ProviderError`, `ProviderType`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn normalize_provider_id(id: &str) -> String;
// pub
fn is_production_provider_id(id: &str) -> bool;
// private
fn canonical_id_owned(id: &str) -> String;
// pub
fn is_retired_provider(id: &str) -> bool;
// pub
fn display_name(&self) -> &'static str;
// pub
fn is_production(&self) -> bool;
// pub
fn new(secret: impl Into<String>) -> Self;
// pub
fn is_empty(&self) -> bool;
// pub
fn expose_secret(&self) -> &str;
// pub
fn masked(&self) -> String;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,;
// private
fn deserialize(deserializer: D) -> Result<Self, D::Error>
    where
        D: serde::Deserializer<'de>,;
// private
fn from(e: std::io::Error) -> Self;
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_provider_status_discrimination`, `test_provider_probe_semantics`, `test_production_registry_is_nvidia_only`, `test_nvidia_only_error_message`, `test_f16_multibyte_utf8_secret_masking`

---

### `src/config/resolved.rs` {#src-config-resolved-rs}

- **Source Link:** [`src/config/resolved.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/config/resolved.rs)
- **Lines of Code:** 1345 (56386 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Unified Authoritative Configuration Control Plane (CFG-01..04).  Provides the single authoritative `ResolvedConfiguration` used by the production runtime, enforcing the 8-tier hierarchy: Tier 0: Immutable Security Invariants Tier 1: System Configuration (/etc/m31a/config.toml) Tier 2: User Configuration (~/.config/m31a/config.toml) Tier 3: Workspace Configuration (&lt;workspace&gt;/.m31a/config.toml) Tier 4: Profile (e.g. autonomous, coding, safe) Tier 5: Environment (M31A_*, std::env) Tier 6: CLI (--config, --model, --profile, --autonomy, etc.) Tier 7: Session Override (/model, /profile, runtime dynamic overrides)

#### Types & Trait Declarations
- **Structs (4):** `ConfigExplain`, `ResolvedConfigBuilder`, `ResolvedConfiguration`, `TierOverrideRecord`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn builder(workspace_root: impl Into<PathBuf>) -> ResolvedConfigBuilder;
// pub
fn for_workspace(workspace_root: impl Into<PathBuf>) -> Result<Self, ConfigError>;
// pub
fn build_fallback(workspace_root: impl Into<PathBuf>) -> Self;
// pub
fn workspace_config_exists(workspace_root: impl Into<PathBuf>) -> bool;
// pub
fn load_strict(workspace_root: impl Into<PathBuf>) -> Result<Self, ConfigError>;
// pub
fn get_resolved(&self, key: &str) -> Option<ResolvedValue>;
// pub
fn explain(&self, key: &str) -> Option<ConfigExplain>;
// pub
fn sources(&self) -> Vec<String>;
// pub
fn with_session_model(&self, model: &str) -> Result<Self, ConfigError>;
// pub
fn with_session_provider(&self, provider: &str) -> Result<Self, ConfigError>;
// pub
fn active_provider_status(&self) -> crate::model::types::ProviderCapabilityStatus;
// pub
fn provider_endpoint_source(&self) -> crate::model::provider::EndpointTrustSource;
// pub
fn timeout_policy(&self) -> crate::config::canonical::TimeoutPolicy;
// pub
fn resource_policy(&self) -> crate::config::canonical::ResourcePolicy;
// pub
fn cache_policy(&self) -> crate::config::canonical::ModelCatalogCachePolicy;
```

---

### `src/config/schema.rs` {#src-config-schema-rs}

- **Source Link:** [`src/config/schema.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/config/schema.rs)
- **Lines of Code:** 1085 (38150 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Strict Configuration Schema &amp; Validation (CFG-02, D-13).

#### Types & Trait Declarations
- **Structs (14):** `AgentsConfig`, `AppConfig`, `CacheConfig`, `GitConfig`, `PolicyConfig`, `ProviderConfig`, `ProviderTableConfig`, `ResourcesConfig`, `RuntimeConfig`, `TimeoutsConfig`, `TuiConfig`, `WorkflowConfig`, `WorkspaceConfig`, `WorkspaceVerificationConfig`
- **Enums (3):** `ConfigValidationError`, `GitExecutionIsolation`, `GitPushPolicy`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default_concurrency_limit() -> usize;
// private
fn default_timeout_secs() -> u64;
// private
fn default_sandbox_mode() -> String;
// private
fn default_true() -> bool;
// private
fn default_default_action() -> String;
// private
fn default_model() -> String;
// private
fn default_max_tokens() -> u32;
// private
fn default_fps() -> u32;
// private
fn default_theme() -> String;
// private
fn default_retention_policy() -> String;
// private
fn default_branch_prefix() -> String;
// private
fn default_provider() -> String;
// private
fn default_ignored_paths() -> Vec<String>;
// private
fn default_research_concurrency() -> usize;
// private
fn default_max_discovery_turns() -> usize;
```

---
