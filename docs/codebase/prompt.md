# Prompt System

> **Architectural Layer:** L3 Intelligence  
> **Source Directory:** `src/prompt`  
> **File Count:** 16 source files  

Prompt registry, template rendering, versioning, and prompt references.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [builtins.rs](#src-prompt-builtins-rs) | 351 | `Functions/Traits` | Embedded TOML builtin prompt contracts.  Provides compile-time embeddi... |
| [catalog.rs](#src-prompt-catalog-rs) | 1420 | `CatalogEntry, InMemoryPromptCatalog, PromptContractMetadata` | Immutable prompt catalog index, directory discovery, and built-in gene... |
| [compiler.rs](#src-prompt-compiler-rs) | 1130 | `CompilationOptions, DefaultPromptCompiler, EffectivePrompt` | PromptCompiler: Deterministic 7-layer composition and trust-aware prom... |
| [composer.rs](#src-prompt-composer-rs) | 508 | `ArtifactEvidenceSection, PromptComposition, PromptLayerEntry` | Typed 7-layer prompt composition model (Architecture Section 16).  Enf... |
| [context.rs](#src-prompt-context-rs) | 836 | `ArtifactEvidence, DurableStateContext, PromptBudget` | Typed runtime context abstraction for PromptOS (Architecture Section 8... |
| [contract.rs](#src-prompt-contract-rs) | 1233 | `BodyRaw, CompatibilityRaw, EvidenceRaw` | Versioned PromptContract models, hashing, and TOML deserialization. |
| [error.rs](#src-prompt-error-rs) | 79 | `PromptError` | Strongly typed errors for prompt contract validation, rendering, and c... |
| [mod.rs](#src-prompt-mod-rs) | 53 | `Functions/Traits` | PromptOS core module: versioned PromptContracts, MiniJinja rendering, ... |
| [model_profile.rs](#src-prompt-model_profile-rs) | 360 | `CapabilityRating, ModelProfile, StructuredOutputSupport` | Strongly typed model capability descriptor for PromptOS prompt adaptat... |
| [parameter.rs](#src-prompt-parameter-rs) | 20 | `PromptParameter` | Parameter models and limits for prompt template evaluation. |
| [provenance.rs](#src-prompt-provenance-rs) | 346 | `PromptCompactionMetadata, PromptCompilationTrace, PromptInvocationProvenance` | Prompt provenance, telemetry, and observability models (Architecture S... |
| [reachability.rs](#src-prompt-reachability-rs) | 222 | `PromptCiBucket, PromptReachability` | Authoritative prompt reachability classification (wiring remediation v... |
| [reference.rs](#src-prompt-reference-rs) | 246 | `PromptReference, PromptPurpose` | Typed reference to a versioned prompt contract. |
| [renderer.rs](#src-prompt-renderer-rs) | 117 | `RenderedPrompt` | Deterministic MiniJinja template rendering under strict byte and param... |
| [strategy.rs](#src-prompt-strategy-rs) | 163 | `PromptStrategy` | PromptStrategy enum and deterministic strategy resolution for PromptOS... |
| [v2.rs](#src-prompt-v2-rs) | 565 | `ClaimRecord, CompatibilityMetadata, EvidenceRequirements` | PromptOS V2 Canonical Domain Contracts, Layered Authority, and Epistem... |

---

### `src/prompt/builtins.rs` {#src-prompt-builtins-rs}

- **Source Link:** [`src/prompt/builtins.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/prompt/builtins.rs)
- **Lines of Code:** 351 (14294 bytes)

#### Primary Responsibility
Embedded TOML builtin prompt contracts.  Provides compile-time embedding of the canonical prompt contracts located under `prompts/`. All built-in prompts are parsed and validated upon catalog initialization.

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn load_builtin_contracts() -> Result<Vec<PromptContract>, PromptError>;
// pub
fn load_builtin_contracts_v2() -> Result<Vec<PromptContract>, PromptError>;
// pub
fn load_production_contracts() -> Result<Vec<PromptContract>, PromptError>;
// pub
fn load_compatibility_contracts() -> Result<Vec<PromptContract>, PromptError>;
// pub
fn load_production_and_compatibility_contracts() -> Result<Vec<PromptContract>, PromptError>;
// pub
fn load_test_fixture_contracts() -> Result<Vec<PromptContract>, PromptError>;
// pub
fn load_deprecated_metadata_contracts() -> Result<Vec<PromptContract>, PromptError>;
// pub
fn load_all_builtin_contracts() -> Result<Vec<PromptContract>, PromptError>;
```

---

### `src/prompt/catalog.rs` {#src-prompt-catalog-rs}

- **Source Link:** [`src/prompt/catalog.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/prompt/catalog.rs)
- **Lines of Code:** 1420 (55859 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Immutable prompt catalog index, directory discovery, and built-in genesis contracts.

#### Types & Trait Declarations
- **Structs (3):** `CatalogEntry`, `InMemoryPromptCatalog`, `PromptContractMetadata`
- **Traits (1):** `PromptCatalog`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn is_protected_contract_id(id: &str) -> bool;
// pub
fn is_layer0_contract_id(id: &str) -> bool;
// pub
fn is_behavioral_contract_id(id: &str) -> bool;
// private
fn get(&self, id: &str, version: u32) -> Result<&PromptContract, PromptError>;
// private
fn contains(&self, id: &str, version: u32) -> bool;
// private
fn list(&self) -> Vec<PromptContractMetadata>;
// private
fn source_kind(&self, id: &str, version: u32) -> Option<PromptSourceKind>;
// private
fn project_guidance_for(&self, _id: &str, _version: u32) -> Vec<CatalogEntry>;
// private
fn is_overrideable(&self, id: &str, _version: u32) -> bool;
// private
fn resolve_canonical(&self, id: &str, version: u32) -> Result<&PromptContract, PromptError>;
// private
fn audit_inventory(&self) -> crate::prompt::v2::PromptInventoryAudit;
// pub
fn new() -> Self;
// pub
fn with_production_builtins() -> Self;
// pub
fn with_production_builtins_and_workspace(workspace_root: &Path) -> Self;
// pub
fn with_builtins() -> Self;
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_catalog_builtins_and_source_kind`, `test_override_precedence_workspace_over_project_over_builtin`, `test_protected_contract_override_strictly_rejected`, `test_behavioral_override_becomes_guidance_not_replacement`, `test_duplicate_in_same_scope_rejected`, `test_path_safety_checks`

---

### `src/prompt/compiler.rs` {#src-prompt-compiler-rs}

- **Source Link:** [`src/prompt/compiler.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/prompt/compiler.rs)
- **Lines of Code:** 1130 (46308 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
PromptCompiler: Deterministic 7-layer composition and trust-aware prompt compilation pipeline.  # Responsibilities &amp; Architectural Ownership The `PromptCompiler` is the canonical engine that transforms an abstract [`PromptContract`] and structured runtime [`PromptContext`] into an [`EffectivePrompt`].  # The Seven Canonical Layers (L0 through L6) The compiler enforces a strictly ordered, non-reorderable 7-layer composition model: 1. **L0 — Runtime Safety Invariants:** Immutable P0 constraints (`RUNTIME_SAFETY_INVARIANTS`), unprunable, prepended unconditionally before any other content. 2. **L1 — Agent Role &amp; Profile:** Operating role identity and stage constraints (P1, unprunable). 3. **L2 — Workflow Step Objective &amp; Contract:** Current task purpose, acceptance criteria, expected output format, and user intent wrapped in `&lt;user_intent&gt;` (P1, unprunable). 4. **L3 — Project Charter &amp; Durable State:** `.m31a/project/` project memory extracts (P2, compactable). 5. **L4 — Upstream Artifact Evidence &amp; Tool Results:** Prior step outputs and tool execution logs wrapped in `&lt;untrusted_evidence&gt;` with closing tag escaping (P2/P3, compactable). 6. **L5 — Repository Topology &amp; Context:** Repository file extracts and AST summaries (P3/P4, disposable). 7. **L6 — Quality Gate &amp; Verification Checklist:** Acceptance assertions and checklist items (P1, unprunable).  # Trust Handling &amp; Delimiter Smuggling Defense External and untrusted data (user intent, tool outputs, repository files, git diffs) are encapsulated in typed XML trust envelopes (`&lt;user_intent&gt;` and `&lt;untrusted_evidence&gt;`). Any occurrences of closing tags within payload text are escaped to prevent prompt injection delimiter hijacking. External content never gains system-level instruction authority.  # Deterministic Compilation &amp; Hashing Compilation is strictly deterministic. On identical contracts, versions, parameters, and contexts, `PromptCompiler` produces byte-for-byte identical assembled prompts and cryptographic SHA-256 `content_hash` values. No random UUIDs, timestamps, or unordered collections are used in hashing.

#### Types & Trait Declarations
- **Structs (3):** `CompilationOptions`, `DefaultPromptCompiler`, `EffectivePrompt`
- **Traits (1):** `PromptCompiler`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn with_profile(mut self, profile: ModelProfile) -> Self;
// pub
fn with_strategy(mut self, strategy: PromptStrategy) -> Self;
// pub
fn with_budget(mut self, max_bytes: usize) -> Self;
// pub
fn with_strict_parameters(mut self, strict: bool) -> Self;
// pub
fn with_source_kind(mut self, source_kind: PromptSourceKind) -> Self;
// pub
fn invocation_provenance(&self) -> Option<PromptInvocationProvenance>;
// pub
fn source_kind(&self) -> PromptSourceKind;
// private
fn compile(&self,
        contract: &PromptContract,
        context: &PromptContext,
        options: &CompilationOptio;
// private
fn compile_with_guidance(&self,
        catalog: &dyn crate::prompt::catalog::PromptCatalog,
        contract: &PromptCo;
// pub
fn new() -> Self;
// pub
fn compile_from_catalog(&self,
        catalog: &dyn crate::prompt::catalog::PromptCatalog,
        id: &str,
        ve;
// pub
fn compile_from_catalog_with_guidance(&self,
        catalog: &dyn crate::prompt::catalog::PromptCatalog,
        id: &s;
// pub
fn calculate_effective_hash(contract: &PromptContract,
        parameters: &BTreeMap<String, String>,
        layers: &[;
// pub
fn calculate_legacy_hash(contract: &PromptContract,
        parameters: &BTreeMap<String, String>,
        layers: &[Pro;
```

---

### `src/prompt/composer.rs` {#src-prompt-composer-rs}

- **Source Link:** [`src/prompt/composer.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/prompt/composer.rs)
- **Lines of Code:** 508 (18383 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Typed 7-layer prompt composition model (Architecture Section 16).  Enforces the canonical layered prompt hierarchy: - Layer 0: Runtime Safety Invariants (P0, immutable, unprunable) - Layer 1: Agent Role &amp; Profile (P1, unprunable) - Layer 2: Workflow Step Objective &amp; Output Contract (P1, unprunable) - Layer 3: Project Charter &amp; Boundaries (P2, compactable) - Layer 4: Upstream Artifact Evidence &amp; Tool Results (P2/P3, compactable) - Layer 5: Repository Constraints &amp; Context (P3/P4, disposable) - Layer 6: Quality Gate Assertions (P1, unprunable)

#### Types & Trait Declarations
- **Structs (3):** `ArtifactEvidenceSection`, `PromptComposition`, `PromptLayerEntry`
- **Enums (1):** `PromptLayerKind`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// pub
fn priority(&self) -> u8;
// pub
fn is_prunable(&self) -> bool;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(kind: PromptLayerKind,
        name: impl Into<String>,
        content: impl Into<String>,
        trust_level: ;
// pub
fn new(role_profile: impl Into<String>,
        step_objective: impl Into<String>,
        quality_gate_assertions: Vec<;
// pub
fn from_context(context: &PromptContext,
        role_profile: impl Into<String>,
        rendered_objective: impl Into<;
// pub
fn with_charter(mut self, charter: impl Into<String>) -> Self;
// pub
fn with_upstream_artifact(mut self,
        source_step: impl Into<String>,
        artifact_name: impl Into<String>,
  ;
// pub
fn with_repo_context(mut self, repo_context: impl Into<String>) -> Self;
// pub
fn verify_safety_invariants(&self) -> bool;
// pub
fn validate(&self) -> Result<(), PromptError>;
// pub
fn ordered_layers(&self) -> Vec<PromptLayerEntry>;
// pub
fn to_full_prompt(&self) -> String;
// pub
fn to_context_sections(&self, tokenizer: &TokenizerAdapter) -> Vec<ContextSection>;
```

---

### `src/prompt/context.rs` {#src-prompt-context-rs}

- **Source Link:** [`src/prompt/context.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/prompt/context.rs)
- **Lines of Code:** 836 (30755 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Typed runtime context abstraction for PromptOS (Architecture Section 8 &amp; Section 46).  Enforces strong domain typing, explicit trust classification, and separation of ephemeral reasoning data from durable project memory.

#### Types & Trait Declarations
- **Structs (12):** `ArtifactEvidence`, `DurableStateContext`, `PromptBudget`, `PromptContext`, `QualityGateContext`, `RepoContext`, `RepoFileContext`, `TaskObjectiveContext`, `ToolOutputEvidence`, `TrustedPolicyContext`, `TrustedSystemContext`, `UserInputContext`
- **Enums (1):** `MissionStage`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn default() -> Self;
// pub
fn new(raw_intent: impl Into<String>) -> Self;
// pub
fn to_trust_envelope(&self) -> String;
// pub
fn new(task_objective: impl Into<String>) -> Self;
// pub
fn with_criteria(mut self, criteria: Vec<String>) -> Self;
// pub
fn with_output_format(mut self, format: impl Into<String>) -> Self;
// pub
fn load_from_workspace(workspace_root: &std::path::Path) -> Self;
// pub
fn new(source_step: impl Into<String>,
        artifact_name: impl Into<String>,
        excerpt: impl Into<String>,) ->;
// pub
fn to_trust_envelope(&self) -> String;
// pub
fn new(tool_name: impl Into<String>,
        call_id: impl Into<String>,
        output: impl Into<String>,
        is_e;
// pub
fn to_trust_envelope(&self) -> String;
// pub
fn new(path: impl Into<String>, content: impl Into<String>) -> Self;
// pub
fn to_trust_envelope(&self) -> String;
```

---

### `src/prompt/contract.rs` {#src-prompt-contract-rs}

- **Source Link:** [`src/prompt/contract.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/prompt/contract.rs)
- **Lines of Code:** 1233 (45643 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Versioned PromptContract models, hashing, and TOML deserialization.

#### Types & Trait Declarations
- **Structs (16):** `BodyRaw`, `CompatibilityRaw`, `EvidenceRaw`, `FailureBehaviorRaw`, `InputParamOptionalRaw`, `InputParamRequiredRaw`, `InputsRaw`, `OutputRaw`, `PromptContract`, `PromptFileRaw`, `PromptMetadataRaw`, `ReasoningRaw`, `RoleVisitor`, `SecurityRaw`, `TemplateRaw`, `VerificationRaw`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn deserialize_flexible_role(deserializer: D) -> Result<AgentRole, D::Error>
where
    D: serde::Deserializer<'de>,;
// private
fn expecting(&self, formatter: &mut std::fmt::Formatter) -> std::fmt::Result;
// private
fn visit_str(self, value: &str) -> Result<AgentRole, E>
        where
            E: serde::de::Error,;
// pub
fn deserialize_optional_flexible_role(deserializer: D,) -> Result<Option<AgentRole>, D::Error>
where
    D: serde::Deser;
// pub
fn parse_role_flexible(s: &str) -> Result<AgentRole, String>;
// pub
fn new(id: impl Into<String>,
        version: u32,
        role: AgentRole,
        description: impl Into<String>,
   ;
// pub
fn new_v2(id: impl Into<String>,
        version: u32,
        role: AgentRole,
        kind: PromptKind,
        stage:;
// pub
fn is_v2(&self) -> bool;
// pub
fn is_deprecated(&self) -> bool;
// pub
fn canonical_id(&self) -> &str;
// pub
fn requires_falsification(&self) -> bool;
// pub
fn requires_evidence(&self) -> bool;
// pub
fn calculate_hash(id: &str,
        version: u32,
        role: AgentRole,
        description: &str,
        input_para;
// pub
fn calculate_hash_v2(id: &str,
        version: u32,
        kind: PromptKind,
        role: AgentRole,
        descript;
// pub
fn from_toml_str(toml_str: &str) -> Result<Self, PromptError>;
```

---

### `src/prompt/error.rs` {#src-prompt-error-rs}

- **Source Link:** [`src/prompt/error.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/prompt/error.rs)
- **Lines of Code:** 79 (2727 bytes)

#### Primary Responsibility
Strongly typed errors for prompt contract validation, rendering, and catalog operations.

#### Types & Trait Declarations
- **Enums (1):** `PromptError`

---

### `src/prompt/mod.rs` {#src-prompt-mod-rs}

- **Source Link:** [`src/prompt/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/prompt/mod.rs)
- **Lines of Code:** 53 (2122 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
PromptOS core module: versioned PromptContracts, MiniJinja rendering, composition, and catalog.

---

### `src/prompt/model_profile.rs` {#src-prompt-model_profile-rs}

- **Source Link:** [`src/prompt/model_profile.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/prompt/model_profile.rs)
- **Lines of Code:** 360 (13662 bytes)

#### Primary Responsibility
Strongly typed model capability descriptor for PromptOS prompt adaptation (Section 11, Artifacts F &amp; G).  # Core Invariant: "The model proposes. The runtime decides."  `ModelProfile` represents trusted runtime facts about a model's operational characteristics, physical context boundaries, and tool-calling fidelity.  A `ModelProfile` is a capability descriptor, **never** an authority or privilege mechanism. Models cannot self-report, elevate, or negotiate their own profile attributes.

#### Types & Trait Declarations
- **Structs (2):** `CapabilityRating`, `ModelProfile`
- **Enums (1):** `StructuredOutputSupport`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(val: u8) -> Result<Self, PromptError>;
// pub
fn clamped(val: u8) -> Self;
// pub
fn as_u8(&self) -> u8;
// pub
fn score(&self) -> u8;
// private
fn try_from(value: u8) -> Result<Self, Self::Error>;
// private
fn from(rating: CapabilityRating) -> Self;
// private
fn eq(&self, other: &u8) -> bool;
// private
fn partial_cmp(&self, other: &u8) -> Option<std::cmp::Ordering>;
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
// pub
fn as_str(&self) -> &'static str;
// pub
fn requires_emulated_guidance(&self) -> bool;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn conservative_default() -> Self;
```

---

### `src/prompt/parameter.rs` {#src-prompt-parameter-rs}

- **Source Link:** [`src/prompt/parameter.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/prompt/parameter.rs)
- **Lines of Code:** 20 (844 bytes)

#### Primary Responsibility
Parameter models and limits for prompt template evaluation.

#### Types & Trait Declarations
- **Structs (1):** `PromptParameter`

---

### `src/prompt/provenance.rs` {#src-prompt-provenance-rs}

- **Source Link:** [`src/prompt/provenance.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/prompt/provenance.rs)
- **Lines of Code:** 346 (13207 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Prompt provenance, telemetry, and observability models (Architecture Section 24 &amp; Stage 7).  Enforces complete auditability and reproducibility for every model-facing prompt execution without introducing new runtime authority.  # Core Distinctions 1. **Contract Hash:** SHA-256 hash of the unrendered template in [`crate::prompt::PromptContract`]. 2. **Effective Prompt Hash:** Cryptographic composite SHA-256 hash of the fully compiled, strategy-adapted, parameter-bound, and trust-delimited prompt. 3. **Context Digest:** Deterministic cryptographic SHA-256 digest of the structured runtime context manifest.  # Privacy &amp; Security Guarantees - Zero raw secrets or credentials recorded in provenance metadata. - Raw prompt bodies are never stored in telemetry records. - Zero chain-of-thought or hidden reasoning prompts recorded.

#### Types & Trait Declarations
- **Structs (5):** `PromptCompactionMetadata`, `PromptCompilationTrace`, `PromptInvocationProvenance`, `PromptLayerMetadata`, `PromptProvenance`
- **Enums (1):** `PromptSourceKind`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(prompt_id: impl Into<String>,
        prompt_version: u32,
        prompt_content_hash: impl Into<String>,
      ;
// pub
fn with_source_kind(mut self, source_kind: PromptSourceKind) -> Self;
// pub
fn with_mission_id(mut self, mission_id: impl Into<String>) -> Self;
// pub
fn with_task_id(mut self, task_id: impl Into<String>) -> Self;
// pub
fn with_agent_id(mut self, agent_id: impl Into<String>) -> Self;
// pub
fn sanitized(&self, redactor: &SecretRedactor) -> Self;
// pub
fn new(kind: PromptLayerKind,
        name: impl Into<String>,
        byte_size: usize,
        trust_level: TrustLevel;
// pub
fn new(budget_max_bytes: usize,
        protected_bytes: usize,
        total_compiled_bytes: usize,
        layers_reta;
// pub
fn has_dropped_layers(&self) -> bool;
// pub
fn to_invocation_provenance(&self) -> PromptInvocationProvenance;
// pub
fn source_kind(&self) -> PromptSourceKind;
// pub
fn has_dropped_layers(&self) -> bool;
// pub
fn retained_layers(&self) -> &[PromptLayerKind];
// pub
fn dropped_layers(&self) -> &[PromptLayerKind];
```

---

### `src/prompt/reachability.rs` {#src-prompt-reachability-rs}

- **Source Link:** [`src/prompt/reachability.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/prompt/reachability.rs)
- **Lines of Code:** 222 (10268 bytes)

#### Primary Responsibility
Authoritative prompt reachability classification (wiring remediation v0.1.1).  Every shipped prompt asset has EXACTLY ONE classification describing how (or whether) the production runtime can reach it. Embedding a TOML via `include_str!` is NOT consumption: a prompt is production-reachable only when its identifier can flow into an actual model invocation through the production runtime spine (`PromptReference` → task/role binding → `PromptCatalog` → `PromptCompiler` → `EffectivePrompt` → `ModelCaller`).  The CI gate ([`ci_bucket`]) maps each classification into one of four release buckets. A shipped prompt with no classification fails CI.

#### Types & Trait Declarations
- **Enums (2):** `PromptCiBucket`, `PromptReachability`

#### Key Functions & Signatures (5 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// pub
fn as_str(&self) -> &'static str;
// pub
fn classify_builtin(id: &str, version: u32) -> Option<(PromptReachability, PromptCiBucket)>;
// pub
fn canonical_version(id: &str) -> Option<u32>;
// pub
fn builtin_reachability_matrix(catalog: &dyn crate::prompt::PromptCatalog,) -> (Vec<ReachabilityRow>, Vec<UnclassifiedRo;
```

---

### `src/prompt/reference.rs` {#src-prompt-reference-rs}

- **Source Link:** [`src/prompt/reference.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/prompt/reference.rs)
- **Lines of Code:** 246 (9846 bytes)

#### Primary Responsibility
Typed reference to a versioned prompt contract.

#### Types & Trait Declarations
- **Structs (1):** `PromptReference`
- **Enums (1):** `PromptPurpose`

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn infer_from_id(id: &str) -> Self;
// pub
fn as_str(&self) -> &'static str;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(id: impl Into<String>, version: u32) -> Self;
// pub
fn with_purpose(id: impl Into<String>, version: u32, purpose: PromptPurpose) -> Self;
// pub
fn with_explicit_purpose(mut self, purpose: PromptPurpose) -> Self;
// pub
fn for_role(role: crate::state_machine::agent::AgentRole) -> Self;
// pub
fn parse(s: &str) -> Result<Self, PromptError>;
// pub
fn parse_lenient(s: &str) -> Result<Self, PromptError>;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
```

---

### `src/prompt/renderer.rs` {#src-prompt-renderer-rs}

- **Source Link:** [`src/prompt/renderer.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/prompt/renderer.rs)
- **Lines of Code:** 117 (4354 bytes)

#### Primary Responsibility
Deterministic MiniJinja template rendering under strict byte and parameter bounds.

#### Types & Trait Declarations
- **Structs (1):** `RenderedPrompt`

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn render_prompt(contract: &PromptContract,
    parameters: &BTreeMap<String, String>,
    strict_parameters: bool,) -> ;
```

---

### `src/prompt/strategy.rs` {#src-prompt-strategy-rs}

- **Source Link:** [`src/prompt/strategy.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/prompt/strategy.rs)
- **Lines of Code:** 163 (7878 bytes)

#### Primary Responsibility
PromptStrategy enum and deterministic strategy resolution for PromptOS (Section 10 &amp; 11).  # Core Invariant: "The model proposes. The runtime decides."  A single logical prompt contract is executed across different models and operational contexts by applying a runtime-selected [`PromptStrategy`].  # DeepReasoning Invariant `DeepReasoning` injects explicit architectural directives (task decomposition, invariant validation, and pre-execution verification checklists). **DeepReasoning MUST NOT request or instruct the model to disclose private chain-of-thought or hidden reasoning.**

#### Types & Trait Declarations
- **Enums (1):** `PromptStrategy`

#### Key Functions & Signatures (7 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// pub
fn example_budget(&self) -> usize;
// pub
fn instruction_density(&self) -> &'static str;
// pub
fn structural_directives(&self) -> &'static str;
// pub
fn few_shot_examples(&self) -> Option<&'static str>;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn resolve_strategy(_role: AgentRole,
    stage: MissionStage,
    task_complexity_high: bool,
    in_recovery: bool,
  ;
```

---

### `src/prompt/v2.rs` {#src-prompt-v2-rs}

- **Source Link:** [`src/prompt/v2.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/prompt/v2.rs)
- **Lines of Code:** 565 (21143 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
PromptOS V2 Canonical Domain Contracts, Layered Authority, and Epistemic Governance.  Provides the foundational models and contract invariants for PromptOS V2: 1. **Canonical Taxonomy:** Deterministic, role- and stage-aware prompt categorization. 2. **Explicit Layered Authority:** Non-reorderable 7-layer hierarchy from Kernel (L0) to Dynamic Mission (L6). 3. **Structured Response Kinds:** Strongly typed model response expectations replacing raw string outputs. 4. **Evidence &amp; Verification Semantics:** Mandatory counterexample search, falsification, and empirical evidence validation. 5. **Epistemic Discipline:** Categorization into FACT, INFERENCE, ASSUMPTION, PROPOSAL, OBSERVATION, VERIFICATION, UNKNOWN. 6. **Production Reachability Awareness:** Tracking defined, instantiated, referenced, reachable, production-reachable, exercised, and verified code paths.

#### Types & Trait Declarations
- **Structs (8):** `ClaimRecord`, `CompatibilityMetadata`, `EvidenceRequirements`, `FailurePolicy`, `OutputContract`, `PromptInventoryAudit`, `ReasoningPolicy`, `VerificationRequirements`
- **Enums (9):** `AuthorityLevel`, `ClaimVerificationStatus`, `EpistemicStatus`, `FailureBehavior`, `ProductionReachability`, `PromptKind`, `PromptResponseKind`, `ReasoningDepth`, `ReasoningMode`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn parse_kind(s: &str) -> Result<Self, PromptError>;
// pub
fn as_str(&self) -> &'static str;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn rank(&self) -> u8;
// pub
fn can_override(&self, target: AuthorityLevel) -> bool;
// pub
fn from_type_str(s: &str) -> Self;
// pub
fn as_str(&self) -> &'static str;
// pub
fn new(response_kind: PromptResponseKind,
        format_type: impl Into<String>,
        schema_uri: Option<String>,
  ;
// pub
fn code_proposal() -> Self;
// pub
fn verification_verdict() -> Self;
// pub
fn failure_diagnosis() -> Self;
// private
fn default() -> Self;
// pub
fn for_implementer() -> Self;
// pub
fn for_verifier() -> Self;
// pub
fn strict_adversarial() -> Self;
```

---
