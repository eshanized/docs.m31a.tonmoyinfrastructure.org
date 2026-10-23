# Deployment & Channels

> **Architectural Layer:** L9 Deployment  
> **Source Directory:** `src/deployment`  
> **File Count:** 11 source files  

Compile-time channel isolation (production vs development), update feeds, installer, and rollback.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [artifact.rs](#src-deployment-artifact-rs) | 215 | `ReleaseArtifact, ArtifactError, ArtifactFormat` | Canonical release artifact model.  An artifact's identity lives in str... |
| [channel.rs](#src-deployment-channel-rs) | 204 | `ChannelError, DeploymentChannel, UpdateChannel` | Deployment channel: compile-time artifact identity.  `DeploymentChanne... |
| [context.rs](#src-deployment-context-rs) | 257 | `DeploymentContext` | Authoritative deployment context: "What am I?"  `DeploymentContext` is... |
| [features.rs](#src-deployment-features-rs) | 121 | `FeatureAvailability, FeatureGate, DevelopmentFeature` | Centralized channel-aware feature gating.  Development-only capabiliti... |
| [installer.rs](#src-deployment-installer-rs) | 1054 | `Installer, InstallError` | Transactional installer: staged, verified, atomic replacement.  Update... |
| [manifest.rs](#src-deployment-manifest-rs) | 207 | `DeploymentManifest, ManifestArtifact, DeploymentManifestError` | Machine-readable deployment release manifest (schema v1).  Generated b... |
| [mod.rs](#src-deployment-mod-rs) | 44 | `Functions/Traits` | Deployment &amp; release channels: DEVELOPMENT vs PRODUCTION.  One cor... |
| [paths.rs](#src-deployment-paths-rs) | 332 | `DeploymentPaths` | Centralized deployment-aware path/profile abstraction.  All channel-co... |
| [promotion.rs](#src-deployment-promotion-rs) | 188 | `PromotionError` | Production promotion: development build → verified RC → production.  R... |
| [rollback.rs](#src-deployment-rollback-rs) | 62 | `RollbackError` | Rollback seam: restore the previous known-good binary.  The installer ... |
| [updater.rs](#src-deployment-updater-rs) | 211 | `UpdateCandidate, UpdateError` | Deterministic update discovery + channel-safe application.  Updates ar... |

---

### `src/deployment/artifact.rs` {#src-deployment-artifact-rs}

- **Source Link:** [`src/deployment/artifact.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/deployment/artifact.rs)
- **Lines of Code:** 215 (6956 bytes)

#### Primary Responsibility
Canonical release artifact model.  An artifact's identity lives in structured metadata, never in filenames alone. Every artifact records version, channel, target, format, sha256, size, build ID, and source commit so production provenance is traceable end-to-end (commit → CI run → build → checksum → manifest → release).

#### Types & Trait Declarations
- **Structs (1):** `ReleaseArtifact`
- **Enums (2):** `ArtifactError`, `ArtifactFormat`

#### Key Functions & Signatures (12 shown)
```rust
// pub
fn parse(s: &str) -> Option<Self>;
// pub
fn is_archive(&self) -> bool;
// pub
fn as_str(&self) -> &'static str;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn parsed_format(&self) -> Result<ArtifactFormat, ArtifactError>;
// pub
fn expected_executable_name(&self) -> String;
// pub
fn validate(&self) -> Result<(), ArtifactError>;
// pub
fn is_supported_target(target: &str) -> bool;
// private
fn sample() -> ReleaseArtifact;
// private
fn valid_artifact_passes();
// private
fn invalid_artifacts_rejected();
// private
fn target_matrix_complete();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`valid_artifact_passes`, `invalid_artifacts_rejected`, `target_matrix_complete`

---

### `src/deployment/channel.rs` {#src-deployment-channel-rs}

- **Source Link:** [`src/deployment/channel.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/deployment/channel.rs)
- **Lines of Code:** 204 (6660 bytes)

#### Primary Responsibility
Deployment channel: compile-time artifact identity.  `DeploymentChannel` is independent from Cargo build profiles (`dev` vs `release`). Valid combinations include development+debug, development+release, and production+release. The channel is stamped at compile time via the `development` cargo feature (production = default, no feature) and can NEVER be changed at runtime by environment variables.

#### Types & Trait Declarations
- **Enums (3):** `ChannelError`, `DeploymentChannel`, `UpdateChannel`

#### Key Functions & Signatures (9 shown)
```rust
// pub
fn parse(s: &str) -> Result<Self, ChannelError>;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn from(c: DeploymentChannel) -> Self;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn current_matches_feature_flag();
// private
fn parse_table();
// private
fn binary_names_distinct();
// private
fn update_channel_mapping();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`current_matches_feature_flag`, `parse_table`, `binary_names_distinct`, `update_channel_mapping`

---

### `src/deployment/context.rs` {#src-deployment-context-rs}

- **Source Link:** [`src/deployment/context.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/deployment/context.rs)
- **Lines of Code:** 257 (8832 bytes)

#### Primary Responsibility
Authoritative deployment context: "What am I?"  `DeploymentContext` is immutable runtime metadata stamped at compile time (channel + build facts) combined with the single canonical semantic version (`CARGO_PKG_VERSION`). It is cheap to clone, `Send + Sync`, and performs no filesystem or network I/O — channel resolution never blocks.

#### Types & Trait Declarations
- **Structs (1):** `DeploymentContext`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn current() -> Self;
// pub
fn from_parts(channel: DeploymentChannel,
        version: &str,
        commit: &str,
        branch: &str,
        bui;
// pub
fn is_development(&self) -> bool;
// pub
fn is_production(&self) -> bool;
// pub
fn cli_version_string(&self) -> String;
// pub
fn cockpit_label(&self) -> String;
// pub
fn verbose_report(&self) -> String;
// pub
fn to_json(&self) -> serde_json::Value;
// pub
fn build_channel_marker() -> &'static str;
// pub
fn derive_build_id(version: &str, channel: &str, commit: &str, target: &str) -> String;
// private
fn version_authority_preserved();
// private
fn build_channel_marker_agrees_with_current();
// private
fn build_id_deterministic_and_discriminating();
// private
fn cli_version_distinguishes_channel_without_forking_semver();
// private
fn verbose_report_has_no_secrets_shape();
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`version_authority_preserved`, `build_channel_marker_agrees_with_current`, `build_id_deterministic_and_discriminating`, `cli_version_distinguishes_channel_without_forking_semver`, `verbose_report_has_no_secrets_shape`

---

### `src/deployment/features.rs` {#src-deployment-features-rs}

- **Source Link:** [`src/deployment/features.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/deployment/features.rs)
- **Lines of Code:** 121 (3826 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Centralized channel-aware feature gating.  Development-only capabilities are gated in exactly one place. Callers ask `FeatureGate::check(feature)` and receive an explicit verdict — never a string comparison on `"development"` scattered across subsystems.  Invariant: gating controls *visibility/availability* of diagnostics and experimental affordances. It NEVER bypasses policy, sandbox, capability, approval, containment, or secret controls (§48).

#### Types & Trait Declarations
- **Structs (2):** `FeatureAvailability`, `FeatureGate`
- **Enums (1):** `DevelopmentFeature`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn new(channel: DeploymentChannel) -> Self;
// pub
fn current() -> Self;
// pub
fn check(&self, feature: DevelopmentFeature) -> FeatureAvailability;
// pub
fn is_enabled(&self, feature: DevelopmentFeature) -> bool;
// private
fn production_rejects_all_dev_features();
// private
fn development_enables_all_dev_features();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`production_rejects_all_dev_features`, `development_enables_all_dev_features`

---

### `src/deployment/installer.rs` {#src-deployment-installer-rs}

- **Source Link:** [`src/deployment/installer.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/deployment/installer.rs)
- **Lines of Code:** 1054 (39376 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Transactional installer: staged, verified, atomic replacement.  Update sequence (behavioral transaction): discover → download → verify checksum → stage → verify executable → atomically replace → verify runtime. On any failure the previous known-good binary is preserved and success is never reported.  User state (config/data/cache/state/database) is never wiped or migrated implicitly by installation.

#### Types & Trait Declarations
- **Structs (1):** `Installer`
- **Enums (1):** `InstallError`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn validate_archive_entry_path(path: &Path) -> Result<(), InstallError>;
// private
fn extract_executable_from_targz(bytes: &[u8],
    expected_binary_name: &str,
    target_path: &Path,) -> Result<(), In;
// private
fn extract_executable_from_zip(bytes: &[u8],
    expected_binary_name: &str,
    target_path: &Path,) -> Result<(), Inst;
// private
fn verify_executable(path: &Path,
    artifact: &ReleaseArtifact,
    expected_channel: DeploymentChannel,) -> Result<();
// private
fn safe_replace_file(src: &Path, dest: &Path, staging_dir: &Path) -> Result<(), std::io::Error>;
// pub
fn new(install_dir: impl Into<PathBuf>) -> Self;
// pub
fn install_dir(&self) -> &Path;
// pub
fn live_path(&self, binary_name: &str) -> PathBuf;
// pub
fn prev_path(&self, binary_name: &str) -> PathBuf;
// pub
fn staging_path(&self, filename: &str) -> PathBuf;
// pub
fn restore_backup(&self, binary_name: &str) -> Result<PathBuf, InstallError>;
// private
fn purge_staging_temp_files(&self, binary_name: &str);
// pub
fn install_bytes(&self,
        artifact: &ReleaseArtifact,
        bytes: &[u8],
        expected_channel: DeploymentCh;
// pub
fn previous_binary(&self, binary_name: &str) -> Option<PathBuf>;
// pub
fn make_tar_gz(entries: &[(&str, &[u8]);
```

#### Unit Verification (9 inline tests)
Tests defined within module:
`successful_tar_gz_install_and_update_preserves_previous`, `successful_zip_install_and_update`, `checksum_mismatch_keeps_previous`, `path_traversal_tar_rejected`, `symlink_tar_rejected`, `path_traversal_zip_rejected`, `missing_executable_in_archive_rejected`, `multiple_matching_executables_rejected`, `restoration_on_post_replacement_failure`

---

### `src/deployment/manifest.rs` {#src-deployment-manifest-rs}

- **Source Link:** [`src/deployment/manifest.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/deployment/manifest.rs)
- **Lines of Code:** 207 (7552 bytes)

#### Primary Responsibility
Machine-readable deployment release manifest (schema v1).  Generated by the release pipeline (`scripts/build-release.sh` / CI), never handwritten. One schema serves both channels (`channel` field differs); no incompatible dev-only format exists. Validation fails closed.

#### Types & Trait Declarations
- **Structs (2):** `DeploymentManifest`, `ManifestArtifact`
- **Enums (1):** `DeploymentManifestError`

#### Key Functions & Signatures (7 shown)
```rust
// pub
fn parse_json(doc: &str) -> Result<Self, DeploymentManifestError>;
// pub
fn to_canonical_json(&self) -> Result<String, DeploymentManifestError>;
// pub
fn validate(&self) -> Result<(), DeploymentManifestError>;
// private
fn sample() -> DeploymentManifest;
// private
fn valid_manifest_passes();
// private
fn dev_manifest_uses_same_schema();
// private
fn rejects_malformed();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`valid_manifest_passes`, `dev_manifest_uses_same_schema`, `rejects_malformed`

---

### `src/deployment/mod.rs` {#src-deployment-mod-rs}

- **Source Link:** [`src/deployment/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/deployment/mod.rs)
- **Lines of Code:** 44 (1869 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Deployment &amp; release channels: DEVELOPMENT vs PRODUCTION.  One core runtime, multiple deployment channels. The channel is compile-time artifact identity (`development` cargo feature; production is the default) and determines installation names (`m31a` vs `m31a-dev`), global state isolation, and update feeds — never security posture, workspace identity, or the canonical `Cargo.toml` version authority.  Module ownership: `release/` owns the release-candidate/evidence state machine; `deployment/` owns the installed-artifact/channel lifecycle. `config/` consumes deployment-aware paths; `runtime/` consumes the deployment context; `tui/` projects it. No reverse dependencies.

#### Key Functions & Signatures (2 shown)
```rust
// pub
fn cli_version_string() -> String;
// pub
fn binary_name() -> &'static str;
```

---

### `src/deployment/paths.rs` {#src-deployment-paths-rs}

- **Source Link:** [`src/deployment/paths.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/deployment/paths.rs)
- **Lines of Code:** 332 (12954 bytes)

#### Primary Responsibility
Centralized deployment-aware path/profile abstraction.  All channel-conditional path logic lives here. The rest of the runtime consumes canonical paths from `DeploymentPaths` — no scattered `if development &#123; ... &#125; else &#123; ... &#125;` at callsites.  Principles: - Global (user) state is fully isolated: `m31a` vs `m31a-dev` app names, so config/data/cache/state/runtime files never collide. - Project-local `.m31a/` is a shared workspace directory by default for source metadata (init, repo knowledge), with deployment-scoped runtime/session state isolated underneath it. Production keeps legacy filenames (backward compatible); development uses `-dev` suffixed siblings so it can never corrupt production state.

#### Types & Trait Declarations
- **Structs (1):** `DeploymentPaths`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(channel: DeploymentChannel) -> Self;
// pub
fn current() -> Self;
// pub
fn channel(&self) -> DeploymentChannel;
// private
fn env_override(dev_name: &str,
        shared_name: &str,
        channel: DeploymentChannel,) -> Option<PathBuf>;
// pub
fn config_dir(&self) -> PathBuf;
// pub
fn data_dir(&self) -> PathBuf;
// pub
fn cache_dir(&self) -> PathBuf;
// pub
fn state_dir(&self) -> PathBuf;
// pub
fn user_config_file(&self) -> PathBuf;
// pub
fn global_db_path(&self) -> PathBuf;
// pub
fn global_credentials_file(&self) -> PathBuf;
// pub
fn global_model_catalog_file(&self) -> PathBuf;
// pub
fn global_artifacts_dir(&self) -> PathBuf;
// pub
fn global_telemetry_dir(&self) -> PathBuf;
// pub
fn global_staging_dir(&self) -> PathBuf;
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`global_dirs_differ_by_channel`, `project_root_shared_but_state_isolated`

---

### `src/deployment/promotion.rs` {#src-deployment-promotion-rs}

- **Source Link:** [`src/deployment/promotion.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/deployment/promotion.rs)
- **Lines of Code:** 188 (5891 bytes)

#### Primary Responsibility
Production promotion: development build → verified RC → production.  Reuses the existing `src/release/*` state machine (`ReleaseCandidate`, `ReleaseEvidence`, `Blocker`, `BlockerEvaluator`). This module adds only the deployment-channel layer: a development artifact can never claim production status by itself; promotion requires a Candidate with full evidence, integrity, gates, and human approval.

#### Types & Trait Declarations
- **Enums (1):** `PromotionError`

#### Key Functions & Signatures (7 shown)
```rust
// pub
fn evaluate_promotion(target_channel: DeploymentChannel,
    source: &DeploymentContext,
    candidate: &ReleaseCandidat;
// private
fn candidate() -> ReleaseCandidate;
// private
fn ctx(channel: DeploymentChannel, dirty: bool) -> DeploymentContext;
// private
fn evidence() -> ReleaseEvidence;
// private
fn dev_build_cannot_self_promote_without_evidence();
// private
fn full_evidence_promotes();
// private
fn dirty_or_blocked_denied();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`dev_build_cannot_self_promote_without_evidence`, `full_evidence_promotes`, `dirty_or_blocked_denied`

---

### `src/deployment/rollback.rs` {#src-deployment-rollback-rs}

- **Source Link:** [`src/deployment/rollback.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/deployment/rollback.rs)
- **Lines of Code:** 62 (2334 bytes)

#### Primary Responsibility
Rollback seam: restore the previous known-good binary.  The installer preserves `&lt;binary&gt;.prev` on every replacement. Rollback is an explicit operation (command or automatic post-update recovery): it verifies the backup exists, restores it atomically over the live binary, and reports the restored identity. Rollback never invents a version and never deletes the only working executable.

#### Types & Trait Declarations
- **Enums (1):** `RollbackError`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn rollback(install_dir: &Path, binary_name: &str) -> Result<PathBuf, RollbackError>;
// pub
fn rollback_available(install_dir: &Path, binary_name: &str) -> bool;
// private
fn rollback_restores_previous();
// private
fn rollback_without_backup_fails_closed();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`rollback_restores_previous`, `rollback_without_backup_fails_closed`

---

### `src/deployment/updater.rs` {#src-deployment-updater-rs}

- **Source Link:** [`src/deployment/updater.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/deployment/updater.rs)
- **Lines of Code:** 211 (6978 bytes)

#### Primary Responsibility
Deterministic update discovery + channel-safe application.  Updates are infrastructure operations: no model/provider participation. Discovery resolves immutable release metadata (current version/channel/ target → candidate artifact URL + checksum); application delegates to the transactional `Installer`. Production never consumes development artifacts through the normal path; development never silently consumes stable.

#### Types & Trait Declarations
- **Structs (1):** `UpdateCandidate`
- **Enums (1):** `UpdateError`

#### Key Functions & Signatures (10 shown)
```rust
// private
fn from(e: InstallError) -> Self;
// pub
fn discover_update(manifest: &DeploymentManifest,
    channel: DeploymentChannel,
    target: &str,
    current_version:;
// pub
fn discover_for_current(manifest: &DeploymentManifest,
    target_override: Option<&str>,) -> Result<UpdateCandidate, Up;
// pub
fn feed_name(channel: DeploymentChannel) -> &'static str;
// pub
fn installer_for(channel: DeploymentChannel, install_dir: &std::path::Path) -> Installer;
// pub
fn current_package_version() -> &'static str;
// private
fn manifest(channel: DeploymentChannel, version: &str) -> DeploymentManifest;
// private
fn discovers_newer_same_channel_same_target();
// private
fn rejects_cross_channel_and_stale();
// private
fn manifest_artifact_import_used();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`discovers_newer_same_channel_same_target`, `rejects_cross_channel_and_stale`, `manifest_artifact_import_used`

---
