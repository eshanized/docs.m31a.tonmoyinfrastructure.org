# Context Compiler & Tokenizer

> **Architectural Layer:** L3 Intelligence  
> **Source Directory:** `src/context`  
> **File Count:** 8 source files  

Token budgeting, prompt envelope assembly, evidence ranking, and context window compaction.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [compiler.rs](#src-context-compiler-rs) | 1607 | `ProductionContextCompiler` | Production ContextCompiler delivering minimal fresh context, P0-P4 rev... |
| [envelope.rs](#src-context-envelope-rs) | 401 | `TrustEnvelope, TrustLevel` | XML trust envelopes with prompt-injection delimiter smuggling defense ... |
| [evidence.rs](#src-context-evidence-rs) | 709 | `EvidenceManifestRecord, OmittedEvidenceRecord, SelectedEvidenceItem` | Task-aware semantic context and evidence selection models.  Provides s... |
| [externalize.rs](#src-context-externalize-rs) | 405 | `AdmissionThreshold, ArtifactExternalizer, Engine` | Dynamic artifact externalization and structural preview generation (D-... |
| [manifest.rs](#src-context-manifest-rs) | 172 | `ContextCompilationManifest, ManifestSectionEntry` | Context compilation audit manifest model (D-16, CTX-04).  Emits audita... |
| [mod.rs](#src-context-mod-rs) | 25 | `Functions/Traits` | Context compilation and prompt-injection defense subsystem.  Submodule... |
| [priority.rs](#src-context-priority-rs) | 454 | `CompactionResult, ContextSection, ReverseCompactor` | 5-class deterministic priority pipeline and reverse compaction engine ... |
| [tokenizer.rs](#src-context-tokenizer-rs) | 146 | `TokenizerAdapter` | Model-aware token budgeting and token estimation through TokenizerAdap... |

---

### `src/context/compiler.rs` {#src-context-compiler-rs}

- **Source Link:** [`src/context/compiler.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/context/compiler.rs)
- **Lines of Code:** 1607 (64783 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Production ContextCompiler delivering minimal fresh context, P0-P4 reverse compaction, and prompt-injection defense (D-13, D-14, D-16, CTX-01, CTX-04, CTX-05).  Enforces zero conversational transcript leakage across tasks, strict fail-closed headroom protection, XML trust envelopes with closing-tag escaping, and auditable ContextCompilationManifest generation.

#### Types & Trait Declarations
- **Structs (1):** `ProductionContextCompiler`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn with_tokenizer(tokenizer: TokenizerAdapter) -> Self;
// pub
fn with_prompt_catalog(mut self, catalog: Arc<dyn PromptCatalog>) -> Self;
// pub
fn with_prompt_compiler(mut self, compiler: Arc<dyn PromptCompiler>) -> Self;
// pub
fn with_query_engine(mut self, query_engine: Arc<BoundedQueryEngine>) -> Self;
// pub
fn with_workspace_root(mut self, root: impl Into<PathBuf>) -> Self;
// pub
fn with_memory_store(mut self,
        store: Arc<dyn crate::memory::EngineeringMemoryStore>,) -> Self;
// pub
fn with_role_stage_fallback(mut self, fallback: RoleStageFallback) -> Self;
// pub
fn tokenizer(&self) -> &TokenizerAdapter;
// pub
fn prompt_catalog(&self) -> &Arc<dyn PromptCatalog>;
// pub
fn prompt_compiler(&self) -> &Arc<dyn PromptCompiler>;
// pub
fn workspace_root(&self) -> Option<&Path>;
// pub
fn memory_store(&self) -> Option<Arc<dyn crate::memory::EngineeringMemoryStore>>;
// pub
fn select_evidence(&self,
        req: &ContextCompilationRequest,
        max_evidence_tokens: usize,) -> crate::contex;
// pub
fn compile_sections(&self,
        sections: Vec<ContextSection>,
        total_budget: usize,
        reserved_headroom;
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_compile_context_emits_manifest_and_envelopes`, `test_compile_sections_protected_overflow_fails_closed`, `test_compile_sections_reverse_compaction_drops_p4`

---

### `src/context/envelope.rs` {#src-context-envelope-rs}

- **Source Link:** [`src/context/envelope.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/context/envelope.rs)
- **Lines of Code:** 401 (15818 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
XML trust envelopes with prompt-injection delimiter smuggling defense (D-13, CTX-04, SEC-02).  Structurally encapsulates untrusted repository evidence, tool outputs, and Git history in typed XML envelopes (`&lt;untrusted_evidence source="..." trust="..." hash="..."&gt;`) with closing tag escaping (`&lt;/untrusted_evidence&gt;` -&gt; `&amp;lt;/untrusted_evidence&amp;gt;`) to defeat prompt-injection delimiter hijacking.

#### Types & Trait Declarations
- **Structs (1):** `TrustEnvelope`
- **Enums (1):** `TrustLevel`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn escape_closing_tags(raw_content: &str) -> String;
// pub
fn escape_xml_attribute(val: &str) -> String;
// pub
fn wrap_untrusted(source: &str, trust: TrustLevel, raw_content: &str) -> String;
// pub
fn wrap_untrusted_evidence(source: &str, trust_level: &str, raw_content: &str) -> String;
// pub
fn wrap_untrusted_attributed(source: &str,
        trust: TrustLevel,
        origin: &str,
        reason: &str,
      ;
// pub
fn wrap_user_intent(raw_intent: &str) -> String;
// private
fn test_wrap_untrusted_basic();
// private
fn test_wrap_user_intent_basic_and_escaping();
// private
fn test_prompt_injection_delimiter_escaping();
// private
fn test_case_insensitive_delimiter_escaping();
// private
fn test_all_trust_levels();
// private
fn test_attribute_escaping_quotes_and_breakout();
// private
fn test_attribute_escaping_ampersands_and_entities();
```

#### Unit Verification (10 inline tests)
Tests defined within module:
`test_wrap_untrusted_basic`, `test_wrap_user_intent_basic_and_escaping`, `test_prompt_injection_delimiter_escaping`, `test_case_insensitive_delimiter_escaping`, `test_all_trust_levels`, `test_attribute_escaping_quotes_and_breakout`, `test_attribute_escaping_ampersands_and_entities`, `test_attribute_escaping_newlines_and_control_chars`, `test_wrap_untrusted_attributed_adversarial`, `test_hash_provenance_preserved_with_escaped_attributes`

---

### `src/context/evidence.rs` {#src-context-evidence-rs}

- **Source Link:** [`src/context/evidence.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/context/evidence.rs)
- **Lines of Code:** 709 (24720 bytes)

#### Primary Responsibility
Task-aware semantic context and evidence selection models.  Provides structured evidence typing, deterministic relevance scoring, progressive disclosure pipelines, and explicit vs derived context tracking.

#### Types & Trait Declarations
- **Structs (4):** `EvidenceManifestRecord`, `OmittedEvidenceRecord`, `SelectedEvidenceItem`, `TaskEvidenceSelectionResult`
- **Enums (4):** `ContextSelectionStatus`, `EvidenceOrigin`, `EvidenceSelectionReason`, `TaskContextMode`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn as_str(&self) -> &'static str;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn as_str(&self) -> &'static str;
// pub
fn is_usable(&self) -> bool;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn as_str(&self) -> &'static str;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// pub
fn to_manifest_record(&self) -> EvidenceManifestRecord;
// private
fn from(r: EvidenceManifestRecord) -> Self;
// private
fn from(r: &EvidenceManifestRecord) -> Self;
// private
fn from(r: OmittedEvidenceRecord) -> Self;
// private
fn from(r: &OmittedEvidenceRecord) -> Self;
// pub
fn select_task_aware_evidence(query_engine: Option<&BoundedQueryEngine>,
    req: &ContextCompilationRequest,
    max_ev;
```

---

### `src/context/externalize.rs` {#src-context-externalize-rs}

- **Source Link:** [`src/context/externalize.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/context/externalize.rs)
- **Lines of Code:** 405 (13711 bytes)

#### Primary Responsibility
Dynamic artifact externalization and structural preview generation (D-15, CTX-03).  Offloads oversized evidence to `FsArtifactStore` before exhausting context budget, compiling bounded structural previews (head/tail/error lines, code outlines, JSON projections) and stable `ArtifactId` locators into agent context.

#### Types & Trait Declarations
- **Structs (3):** `AdmissionThreshold`, `ArtifactExternalizer`, `Engine`
- **Enums (2):** `ExternalizeResult`, `State`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn context_representation(&self) -> &str;
// pub
fn new(store: Arc<S>) -> Self;
// pub
fn with_threshold(store: Arc<S>, threshold: AdmissionThreshold) -> Self;
// pub
fn threshold(&self) -> &AdmissionThreshold;
// pub
async fn externalize_if_needed(&self,
        payload: &str,
        file_hint: Option<&str>,) -> Result<ExternalizeResu;
// pub
fn generate_preview(content: &str, file_hint: Option<&str>) -> String;
// private
fn is_code_extension(path: &str) -> bool;
// private
fn extract_code_outline(content: &str) -> String;
// private
fn format_json_preview(val: &serde_json::Value) -> String;
// private
fn format_log_preview(content: &str) -> String;
// private
async fn test_inlined_under_threshold();
// private
async fn test_externalized_oversized_payload();
// private
fn test_generate_preview_log_with_errors();
// private
fn test_generate_preview_code_outline();
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_inlined_under_threshold`, `test_externalized_oversized_payload`, `test_generate_preview_log_with_errors`, `test_generate_preview_code_outline`, `test_generate_preview_json_projection`

---

### `src/context/manifest.rs` {#src-context-manifest-rs}

- **Source Link:** [`src/context/manifest.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/context/manifest.rs)
- **Lines of Code:** 172 (6660 bytes)

#### Primary Responsibility
Context compilation audit manifest model (D-16, CTX-04).  Emits auditable `ContextCompilationManifest` records tracking before/after token counts, section priorities, provenance, and reverse-compaction decisions.

#### Types & Trait Declarations
- **Structs (2):** `ContextCompilationManifest`, `ManifestSectionEntry`

#### Key Functions & Signatures (7 shown)
```rust
// pub
fn new(revision: u32,
        total_budget: usize,
        reserved_headroom: usize,
        compiled_tokens: usize,
   ;
// pub
fn with_evidence(mut self,
        selected_evidence: Vec<EvidenceManifestRecord>,
        omitted_evidence: Vec<Omitted;
// pub
fn to_contract(&self) -> crate::kernel::seams::context::ContextCompilationContract;
// private
fn from(entry: ManifestSectionEntry) -> Self;
// private
fn from(entry: &ManifestSectionEntry) -> Self;
// private
fn from(manifest: ContextCompilationManifest) -> Self;
// private
fn from(manifest: &ContextCompilationManifest) -> Self;
```

---

### `src/context/mod.rs` {#src-context-mod-rs}

- **Source Link:** [`src/context/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/context/mod.rs)
- **Lines of Code:** 25 (830 bytes)

#### Primary Responsibility
Context compilation and prompt-injection defense subsystem.  Submodules: - `envelope`: XML trust envelopes with prompt-injection smuggling defense. - `tokenizer`: TokenizerAdapter with exact BPE and conservative fallback. - `externalize`: Dynamic artifact externalization and preview generation. - `priority`: 5-class deterministic priority pipeline and reverse compaction engine. - `manifest`: Auditable ContextCompilationManifest model. - `compiler`: ProductionContextCompiler satisfying ContextCompiler seam.

---

### `src/context/priority.rs` {#src-context-priority-rs}

- **Source Link:** [`src/context/priority.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/context/priority.rs)
- **Lines of Code:** 454 (16545 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
5-class deterministic priority pipeline and reverse compaction engine (D-14, D-16, CTX-02, CTX-05).  Priorities: - P0 Runtime/Safety (unprunable) - P1 Task/Criteria (unprunable) - P2 Required Evidence (loss-preserving compaction) - P3 Active Working Context (recent turn window / summaries) - P4 Optional Background (discardable first)  Enforces protected budget gate: if P0+P1 exceeds admissible budget, fails closed with ContextBudgetExceeded.

#### Types & Trait Declarations
- **Structs (3):** `CompactionResult`, `ContextSection`, `ReverseCompactor`
- **Enums (1):** `ContextPriority`

#### Key Functions & Signatures (11 shown)
```rust
// pub
fn rank(&self) -> u8;
// pub
fn is_protected(&self) -> bool;
// pub
fn as_str(&self) -> &'static str;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(id: impl Into<String>,
        priority: ContextPriority,
        content: impl Into<String>,
        provenance:;
// pub
fn new(tokenizer: TokenizerAdapter) -> Self;
// pub
fn compact(&self,
        sections: Vec<ContextSection>,
        admissible_budget: usize,) -> Result<CompactionResult, ;
// private
fn make_section(id: &str,
        priority: ContextPriority,
        content: &str,
        compactable: bool,
        t;
// private
fn test_protected_budget_gate_fails_closed();
// private
fn test_reverse_compaction_drops_p4_before_p3();
// private
fn test_reverse_compaction_compacts_p3_and_p2_under_tight_budget();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_protected_budget_gate_fails_closed`, `test_reverse_compaction_drops_p4_before_p3`, `test_reverse_compaction_compacts_p3_and_p2_under_tight_budget`

---

### `src/context/tokenizer.rs` {#src-context-tokenizer-rs}

- **Source Link:** [`src/context/tokenizer.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/context/tokenizer.rs)
- **Lines of Code:** 146 (4688 bytes)

#### Primary Responsibility
Model-aware token budgeting and token estimation through TokenizerAdapter (D-14, CTX-01).  Provides exact BPE token counting via `tiktoken-rs` when available, conservative fallback estimation (~3.5 chars/token), and dynamic output/reasoning headroom calculation per ModelTier.

#### Types & Trait Declarations
- **Structs (1):** `TokenizerAdapter`

#### Key Functions & Signatures (13 shown)
```rust
// pub
fn estimate_tokens_conservative(text: &str) -> usize;
// pub
fn calculate_output_headroom(tier: ModelTier) -> usize;
// pub
fn new() -> Self;
// pub
fn for_model(model_name: &str) -> Self;
// pub
fn conservative() -> Self;
// pub
fn is_exact(&self) -> bool;
// pub
fn count_tokens(&self, text: &str) -> usize;
// pub
fn output_headroom(&self, tier: ModelTier) -> usize;
// pub
fn model_name(&self) -> Option<&str>;
// private
fn default() -> Self;
// private
fn test_estimate_tokens_conservative();
// private
fn test_bpe_exact_counting();
// private
fn test_calculate_output_headroom();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_estimate_tokens_conservative`, `test_bpe_exact_counting`, `test_calculate_output_headroom`

---
