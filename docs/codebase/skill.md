# Skill System

> **Architectural Layer:** L2 Skills  
> **Source Directory:** `src/skill`  
> **File Count:** 6 source files  

Modular skill discovery, invocation, and in-task execution guidance.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [compiler.rs](#src-skill-compiler-rs) | 285 | `CompiledSubDag, CompiledSubTask, SkillCompiler` | Dual-Mode Skill Execution Compiler (SKL-01, SKL-03, D-10).  Compiles d... |
| [discovery.rs](#src-skill-discovery-rs) | 151 | `SkillDiscovery, SkillPackage, SkillOriginTier` | Multi-Tier Skill Discovery (SKL-01, D-09).  Scans across Builtin -&gt;... |
| [manifest.rs](#src-skill-manifest-rs) | 376 | `PluginManifest, SkillExecutionConfig, SkillManifest` | Declarative SKILL.toml Manifest Schema (SKL-01, D-09).  Enforces stric... |
| [mod.rs](#src-skill-mod-rs) | 17 | `Functions/Traits` | Skills Architecture &amp; Reusable Capabilities Engine (SKL-01, SKL-02... |
| [registry.rs](#src-skill-registry-rs) | 253 | `SkillRegistry, SkillError` | Skill Registry with Collision Resolution &amp; Monotonic Safety Valida... |
| [verification.rs](#src-skill-verification-rs) | 90 | `SkillVerificationCompiler, SkillVerificationPlan` | Skill Verification Plan Compiler (SKL-01, SKL-03, D-12).  Transforms d... |

---

### `src/skill/compiler.rs` {#src-skill-compiler-rs}

- **Source Link:** [`src/skill/compiler.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/skill/compiler.rs)
- **Lines of Code:** 285 (10831 bytes)

#### Primary Responsibility
Dual-Mode Skill Execution Compiler (SKL-01, SKL-03, D-10).  Compiles declarative skills into either: 1. Sub-DAG task fragments admitted through scheduler dependency validation 2. In-task procedural prompt guidance within single-step agent contexts

#### Types & Trait Declarations
- **Structs (3):** `CompiledSubDag`, `CompiledSubTask`, `SkillCompiler`

#### Key Functions & Signatures (5 shown)
```rust
// pub
fn compile_sub_dag(manifest: &SkillManifest,
        parent_task_id: TaskId,) -> Result<CompiledSubDag, String>;
// pub
fn compile_in_task_guidance_with_catalog(manifest: &SkillManifest,
        catalog: &impl crate::prompt::catalog::Prompt;
// pub
fn compile_in_task_guidance(manifest: &SkillManifest) -> String;
// private
fn test_compile_sub_dag_generates_tasks_and_edges();
// private
fn test_compile_in_task_guidance();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_compile_sub_dag_generates_tasks_and_edges`

---

### `src/skill/discovery.rs` {#src-skill-discovery-rs}

- **Source Link:** [`src/skill/discovery.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/skill/discovery.rs)
- **Lines of Code:** 151 (5089 bytes)

#### Primary Responsibility
Multi-Tier Skill Discovery (SKL-01, D-09).  Scans across Builtin -&gt; System -&gt; User -&gt; Workspace precedence tiers, parses SKILL.toml files, and calculates cryptographic SHA-256 content hashes.

#### Types & Trait Declarations
- **Structs (2):** `SkillDiscovery`, `SkillPackage`
- **Enums (1):** `SkillOriginTier`

#### Key Functions & Signatures (5 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn compute_sha256(content: &str) -> String;
// pub
fn builtin_skills() -> Vec<SkillPackage>;
// pub
fn discover_directory(base_dir: &Path, tier: SkillOriginTier) -> Vec<SkillPackage>;
// pub
fn discover_all(workspace_root: Option<&Path>) -> Vec<SkillPackage>;
```

---

### `src/skill/manifest.rs` {#src-skill-manifest-rs}

- **Source Link:** [`src/skill/manifest.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/skill/manifest.rs)
- **Lines of Code:** 376 (11294 bytes)

#### Primary Responsibility
Declarative SKILL.toml Manifest Schema (SKL-01, D-09).  Enforces strict schema validation, capability declaration, execution mode, procedural steps, verification commands, and risk profile.

#### Types & Trait Declarations
- **Structs (7):** `PluginManifest`, `SkillExecutionConfig`, `SkillManifest`, `SkillProcedure`, `SkillRiskProfile`, `SkillStepDefinition`, `SkillVerificationSpec`
- **Enums (3):** `PluginValidationError`, `SkillExecutionMode`, `SkillRiskLevel`

#### Key Functions & Signatures (11 shown)
```rust
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn default_input_schema() -> serde_json::Value;
// pub
fn parse_toml(content: &str) -> Result<Self, String>;
// private
fn default_plugin_timeout() -> u64;
// pub
fn parse_toml(content: &str) -> Result<Self, String>;
// pub
fn validate_sandbox(&self, raw_bytes: Option<&[u8]>) -> Result<(), PluginValidationError>;
// private
fn test_parse_valid_skill_manifest();
// private
fn test_reject_unknown_fields();
// private
fn test_reject_unsupported_schema_version();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_parse_valid_skill_manifest`, `test_reject_unknown_fields`, `test_reject_unsupported_schema_version`

---

### `src/skill/mod.rs` {#src-skill-mod-rs}

- **Source Link:** [`src/skill/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/skill/mod.rs)
- **Lines of Code:** 17 (706 bytes)

#### Primary Responsibility
Skills Architecture &amp; Reusable Capabilities Engine (SKL-01, SKL-02, SKL-03).

---

### `src/skill/registry.rs` {#src-skill-registry-rs}

- **Source Link:** [`src/skill/registry.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/skill/registry.rs)
- **Lines of Code:** 253 (8708 bytes)

#### Primary Responsibility
Skill Registry with Collision Resolution &amp; Monotonic Safety Validation (SKL-01, SKL-03, D-09).

#### Types & Trait Declarations
- **Structs (1):** `SkillRegistry`
- **Enums (1):** `SkillError`

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn new() -> Self;
// pub
fn load_discovered(workspace_root: Option<&Path>) -> Result<Self, SkillError>;
// pub
fn register(&mut self, package: SkillPackage) -> Result<(), SkillError>;
// pub
fn get(&self, id: &str) -> Option<&SkillPackage>;
// pub
fn list(&self) -> Vec<&SkillPackage>;
// pub
fn validate_agent_authority(&self,
        skill: &SkillManifest,
        agent_envelope: &HashSet<String>,) -> Result<(;
// private
fn create_dummy_package(id: &str,
        tier: SkillOriginTier,
        v_tier: u8,
        risk: SkillRiskLevel,
     ;
// private
fn test_registry_monotonic_rejection_on_lowered_tier();
// private
fn test_registry_monotonic_rejection_on_removed_approval();
// private
fn test_agent_authority_validation();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_registry_monotonic_rejection_on_lowered_tier`, `test_registry_monotonic_rejection_on_removed_approval`, `test_agent_authority_validation`

---

### `src/skill/verification.rs` {#src-skill-verification-rs}

- **Source Link:** [`src/skill/verification.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/skill/verification.rs)
- **Lines of Code:** 90 (3137 bytes)

#### Primary Responsibility
Skill Verification Plan Compiler (SKL-01, SKL-03, D-12).  Transforms declarative SkillVerificationSpec into an executable VerificationPlan, enforcing runtime monotonicity: max(skill_tier, profile_tier, mission_tier).

#### Types & Trait Declarations
- **Structs (2):** `SkillVerificationCompiler`, `SkillVerificationPlan`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn compile(skill_id: &str,
        spec: &SkillVerificationSpec,
        minimum_tier: Option<CheckTier>,) -> Result<Ski;
// private
fn test_monotonic_verification_tier_strengthening();
// private
fn test_verification_plan_preserves_higher_skill_tier();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_monotonic_verification_tier_strengthening`, `test_verification_plan_preserves_higher_skill_tier`

---
