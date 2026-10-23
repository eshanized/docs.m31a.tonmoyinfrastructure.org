# Release Certification

> **Architectural Layer:** L9 Release  
> **Source Directory:** `src/release`  
> **File Count:** 8 source files  

Release manifests, 20-point production evidence matrix, and release certification.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [hygiene.rs](#src-release-hygiene-rs) | 127 | `HygieneFinding, HygieneKind` | Release-directory cleanliness assertions.  The release output director... |
| [integrity.rs](#src-release-integrity-rs) | 302 | `ChecksumRecord, IntegrityError` | Artifact integrity: SHA-256 checksums, sorted manifest files, and fail... |
| [manifest.rs](#src-release-manifest-rs) | 252 | `ArtifactEntry, ReleaseManifest, ManifestError` | Machine-readable release manifest: schema, canonical serialization, an... |
| [mod.rs](#src-release-mod-rs) | 37 | `Functions/Traits` | Release engineering: version authority, manifest, integrity, provenanc... |
| [provenance.rs](#src-release-provenance-rs) | 230 | `ArtifactDigest, Provenance, ProvenanceError` | Release provenance: factual, verifiable build metadata.  The repositor... |
| [sbom.rs](#src-release-sbom-rs) | 157 | `CargoLock, CargoLockPackage, Sbom` | Software Bill of Materials generated from the exact resolved dependenc... |
| [status.rs](#src-release-status-rs) | 412 | `BlockerEvaluator, Finding, ReleaseCandidate` | Release-candidate status machine, unified blocker taxonomy, and releas... |
| [version.rs](#src-release-version-rs) | 62 | `Functions/Traits` | Canonical version authority.  The ONLY version source is the `Cargo.to... |

---

### `src/release/hygiene.rs` {#src-release-hygiene-rs}

- **Source Link:** [`src/release/hygiene.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/release/hygiene.rs)
- **Lines of Code:** 127 (4260 bytes)

#### Primary Responsibility
Release-directory cleanliness assertions.  The release output directory must be deterministic and controlled: no temporary files, no secrets, no developer-local leakage. Findings are reported, never silently ignored.

#### Types & Trait Declarations
- **Structs (1):** `HygieneFinding`
- **Enums (1):** `HygieneKind`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn check_release_dir(dir: &std::path::Path) -> Vec<HygieneFinding>;
// private
fn detects_temp_and_secrets();
// private
fn clean_dir_passes();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`detects_temp_and_secrets`, `clean_dir_passes`

---

### `src/release/integrity.rs` {#src-release-integrity-rs}

- **Source Link:** [`src/release/integrity.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/release/integrity.rs)
- **Lines of Code:** 302 (10917 bytes)

#### Primary Responsibility
Artifact integrity: SHA-256 checksums, sorted manifest files, and fail-closed verification.  Rules: cryptographic checksums for every artifact; deterministic ordering; no ambiguous filenames; no path traversal in manifests; no silent omission; verification fails when an artifact is modified, missing, or unexpected.

#### Types & Trait Declarations
- **Structs (1):** `ChecksumRecord`
- **Enums (1):** `IntegrityError`

#### Key Functions & Signatures (9 shown)
```rust
// pub
fn sha256_bytes(data: &[u8]) -> String;
// pub
fn sha256_file(path: &Path) -> Result<String, IntegrityError>;
// pub
fn validate_artifact_name(name: &str) -> Result<(), IntegrityError>;
// pub
fn write_sha256sums(dir: &Path, names: &[String]) -> Result<String, IntegrityError>;
// pub
fn verify_sha256sums(dir: &Path,
    document: &str,
    reject_unexpected: bool,) -> Result<Vec<ChecksumRecord>, Integr;
// pub
fn contained_artifact_path(dir: &Path, name: &str) -> Result<PathBuf, IntegrityError>;
// private
fn name_validation_table();
// private
fn tamper_missing_unexpected_detected();
// private
fn empty_document_never_verifies();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`name_validation_table`, `tamper_missing_unexpected_detected`, `empty_document_never_verifies`

---

### `src/release/manifest.rs` {#src-release-manifest-rs}

- **Source Link:** [`src/release/manifest.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/release/manifest.rs)
- **Lines of Code:** 252 (9376 bytes)

#### Primary Responsibility
Machine-readable release manifest: schema, canonical serialization, and fail-closed validation.  A manifest is valid only when: all required fields are present and well-formed; artifact names are unique, safe, and sorted; every entry resolves inside the release directory; and no entry is ambiguous.

#### Types & Trait Declarations
- **Structs (2):** `ArtifactEntry`, `ReleaseManifest`
- **Enums (1):** `ManifestError`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn to_canonical_json(&self) -> Result<String, ManifestError>;
// pub
fn parse_json(doc: &str) -> Result<Self, ManifestError>;
// pub
fn validate_schema(&self) -> Result<(), ManifestError>;
// pub
fn validate_against_dir(&self, dir: &Path) -> Result<(), ManifestError>;
// private
fn sample() -> ReleaseManifest;
// private
fn canonical_json_is_deterministic();
// private
fn schema_rejects_duplicates_unsorted_unsafe();
// private
fn malformed_documents_fail_closed();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`canonical_json_is_deterministic`, `schema_rejects_duplicates_unsorted_unsafe`, `malformed_documents_fail_closed`

---

### `src/release/mod.rs` {#src-release-mod-rs}

- **Source Link:** [`src/release/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/release/mod.rs)
- **Lines of Code:** 37 (1539 bytes)

#### Primary Responsibility
Release engineering: version authority, manifest, integrity, provenance, SBOM, RC state machine, and blocker evaluation.  Authority laws (see crate root / AGENTS.md) apply in full. In particular: release metadata must never claim verification that did not occur, and release automation fails closed rather than producing a partial or unverifiable release.  The single version authority is the `Cargo.toml` package version, propagated at compile time via `CARGO_PKG_VERSION`. There is no second version source.  Cryptographic signing: the repository defines no signing infrastructure, so provenance is factual, verifiable metadata — never a fake signature. `SIGNING_MECHANISM` states this explicitly and validation rejects any manifest that claims otherwise.

---

### `src/release/provenance.rs` {#src-release-provenance-rs}

- **Source Link:** [`src/release/provenance.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/release/provenance.rs)
- **Lines of Code:** 230 (8667 bytes)

#### Primary Responsibility
Release provenance: factual, verifiable build metadata.  The repository defines NO signing infrastructure. Provenance is therefore an explicit factual record — source revision, version, target, toolchain, timestamp policy, artifact digests — never a fake signature, placeholder signature, or manufactured "verified" state. `SIGNING_MECHANISM` states this; validation rejects any manifest claiming otherwise.

#### Types & Trait Declarations
- **Structs (2):** `ArtifactDigest`, `Provenance`
- **Enums (1):** `ProvenanceError`

#### Key Functions & Signatures (6 shown)
```rust
// private
fn run_capture(program: &str, args: &[&str], dir: &Path) -> Result<String, ProvenanceError>;
// pub
fn collect_provenance(repo_dir: &Path,
    version: &str,
    build_target: &str,
    artifacts: Vec<ArtifactDigest>,) -;
// pub
fn verify_provenance(provenance: &Provenance, dir: &Path) -> Result<(), ProvenanceError>;
// private
fn signing_is_explicitly_absent();
// private
fn empty_identity_fails_closed();
// private
fn unexpected_signing_claim_rejected();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`signing_is_explicitly_absent`, `empty_identity_fails_closed`, `unexpected_signing_claim_rejected`

---

### `src/release/sbom.rs` {#src-release-sbom-rs}

- **Source Link:** [`src/release/sbom.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/release/sbom.rs)
- **Lines of Code:** 157 (5055 bytes)

#### Primary Responsibility
Software Bill of Materials generated from the exact resolved dependency graph (`Cargo.lock`) of the release build.  Honesty rules: every `[[package]]` in the lock file appears exactly once, sorted deterministically; fields come only from the lock (name, version, source, checksum). `Cargo.lock` carries no license texts, so no licenses are claimed — the SBOM states this instead of inventing license data.

#### Types & Trait Declarations
- **Structs (4):** `CargoLock`, `CargoLockPackage`, `Sbom`, `SbomComponent`
- **Enums (1):** `SbomError`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn generate_sbom(lock_doc: &str) -> Result<(Sbom, String), SbomError>;
// pub
fn validate_sbom(doc: &str) -> Result<Sbom, SbomError>;
// private
fn generation_is_deterministic_and_sorted();
// private
fn empty_and_malformed_fail_closed();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`generation_is_deterministic_and_sorted`, `empty_and_malformed_fail_closed`

---

### `src/release/status.rs` {#src-release-status-rs}

- **Source Link:** [`src/release/status.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/release/status.rs)
- **Lines of Code:** 412 (14724 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Release-candidate status machine, unified blocker taxonomy, and release-blocker evaluation.  Taxonomy resolution: recovery audits and blocker matrices both record `CREDENTIAL-BLOCKED` in evidence while earlier allowed sets omitted it. Repository evidence (live tests gated on provider credentials and cost policy) shows credential-gating is a first-class, non-blocking classification: live test suites are executed only when explicit credentials are provisioned, and reported honestly otherwise. This module provides the authoritative closed set — the taxonomy cannot drift without failing `taxonomy_is_closed_and_documented`.

#### Types & Trait Declarations
- **Structs (4):** `BlockerEvaluator`, `Finding`, `ReleaseCandidate`, `ReleaseEvidence`
- **Enums (4):** `Blocker`, `ReleaseClassification`, `ReleaseState`, `TransitionError`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn is_terminal(self) -> bool;
// pub
fn as_str(self) -> &'static str;
// pub
fn evaluate(finding: &Finding, mandatory_gate_failed: bool) -> Blocker;
// pub
fn promotion_allowed(findings: &[Finding], mandatory_failures: usize) -> bool;
// pub
fn new() -> Self;
// pub
fn state(&self) -> ReleaseState;
// pub
fn record_build(&mut self, succeeded: bool) -> Result<(), TransitionError>;
// pub
fn record_integrity(&mut self, ok: bool) -> Result<(), TransitionError>;
// pub
fn record_verification(&mut self,
        evidence: &ReleaseEvidence,) -> Result<(), TransitionError>;
// pub
fn promote_to_released(&mut self,
        approval_note: &str,
        blockers: &[Blocker],) -> Result<(), TransitionEr;
// pub
fn reject(&mut self, _reason: &str) -> Result<(), TransitionError>;
// private
fn guard_terminal(&self, op: &str) -> Result<(), TransitionError>;
// private
fn default() -> Self;
// private
fn taxonomy_is_closed_and_documented();
// private
fn blocker_rules();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`taxonomy_is_closed_and_documented`, `blocker_rules`, `state_machine_failure_never_advances`

---

### `src/release/version.rs` {#src-release-version-rs}

- **Source Link:** [`src/release/version.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/release/version.rs)
- **Lines of Code:** 62 (2212 bytes)

#### Primary Responsibility
Canonical version authority.  The ONLY version source is the `Cargo.toml` package version, captured at compile time. The CLI `--version` output (clap `version`), runtime banners, and release metadata all derive from this constant. Any second version authority is a defect.

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn runtime_version() -> &'static str;
// pub
fn cli_version_string() -> String;
// pub
fn parse_cargo_toml_version(doc: &str) -> Result<String, String>;
// private
fn package_and_runtime_versions_agree();
// private
fn cli_version_format_matches_release_contract();
// private
fn cargo_toml_version_parse_rejects_defaults();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`package_and_runtime_versions_agree`, `cli_version_format_matches_release_contract`, `cargo_toml_version_parse_rejects_defaults`

---
