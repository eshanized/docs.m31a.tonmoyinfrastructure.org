# Storage Layout

> **Architectural Layer:** L0 Storage  
> **Source Directory:** `src/storage`  
> **File Count:** 2 source files  

Platform storage layout, global vs workspace state isolation, and legacy migrations.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [migration.rs](#src-storage-migration-rs) | 807 | `LegacyState, MigrationReport, PlanningMigrationReport` | Legacy project-local → platform-global migration.  Existing users may ... |
| [mod.rs](#src-storage-mod-rs) | 629 | `StorageLayout, ConfigScope, StorageClass` | Canonical M31A Storage Authority (L0-L1).  Single authoritative platfo... |

---

### `src/storage/migration.rs` {#src-storage-migration-rs}

- **Source Link:** [`src/storage/migration.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/storage/migration.rs)
- **Lines of Code:** 807 (32028 bytes)

#### Primary Responsibility
Legacy project-local → platform-global migration.  Existing users may have `&lt;ws&gt;/.m31a/m31a.db`, `&lt;ws&gt;/.m31a/credentials.json`, `&lt;ws&gt;/.m31a/artifacts`, `&lt;ws&gt;/.m31a/telemetry`, `&lt;ws&gt;/.m31a/state`, and `&lt;ws&gt;/.m31a/cache/model_catalog*.json`. Migration moves them once to the canonical [`super::StorageLayout`] locations with integrity verification, then stops using the old location. Never deletes user data silently: legacy files are renamed to `*.migrated` only after the destination verifies.

#### Types & Trait Declarations
- **Structs (3):** `LegacyState`, `MigrationReport`, `PlanningMigrationReport`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn is_empty(&self) -> bool;
// pub
fn detect_legacy_state(workspace_root: &Path, channel: DeploymentChannel) -> LegacyState;
// pub
fn is_legacy_present(workspace_root: &Path, channel: DeploymentChannel) -> bool;
// pub
fn has_errors(&self) -> bool;
// pub
fn errors(&self) -> Vec<&str>;
// private
fn sha256_bytes(data: &[u8]) -> String;
// private
fn is_valid_sqlite_bytes(data: &[u8]) -> bool;
// private
fn is_valid_credentials_bytes(data: &[u8]) -> bool;
// private
fn is_valid_catalog_bytes(data: &[u8]) -> bool;
// private
fn copy_file_verified_with_validator(src: &Path,
    dst: &Path,
    dst_valid: impl Fn(&[u8]) -> bool,
) -> Result<(), ;
// private
fn mark_migrated(src: &Path) -> Result<(), String>;
// pub
fn migrate_legacy_workspace_state(layout: &StorageLayout) -> MigrationReport;
// pub
fn migrate_legacy_planning_documents(workspace_root: &Path) -> PlanningMigrationReport;
// private
fn collect_files(dir: &Path,
        base: &Path,
        canon_base: &Path,
        list: &mut Vec<PathBuf>,
        vi;
// private
fn detects_legacy_db_and_credentials();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`detects_legacy_db_and_credentials`

---

### `src/storage/mod.rs` {#src-storage-mod-rs}

- **Source Link:** [`src/storage/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/storage/mod.rs)
- **Lines of Code:** 629 (24296 bytes)

#### Primary Responsibility
Canonical M31A Storage Authority (L0-L1).  Single authoritative platform-aware path system for every durable, cached, and ephemeral store. All other path helpers (`config::paths::PlatformPaths`, `persistence::paths`, `deployment::DeploymentPaths`) delegate to — or are consumed through — this layout so invalid placement is difficult.  ```text M31A_STORAGE ├── User Configuration  (platform config dir / `config.toml`) ├── User Data           (platform data dir / `m31a.db`, artifacts, telemetry) ├── Cache               (platform cache dir / model catalog) ├── Runtime State       (platform state dir / sockets, pid, logs) ├── Credentials         (platform config dir / `credentials.json`, 0600) └── Workspace           (project `.m31a/` — workspace-scoped metadata only) ```  Channel isolation: production uses the `m31a` app name, development uses `m31a-dev`. Platform directories already embed the app name, so the same filename in different channel directories is fully isolated.  Test isolation: when the workspace lives under the OS temp dir and no explicit `M31A_*_DIR` override is set, global paths are derived from a per-workspace isolated root under the temp dir (outside the workspace). This keeps `cargo test` hermetic without polluting the real user profile. Setting `M31A_CONFIG_DIR` / `M31A_DATA_DIR` / `M31A_CACHE_DIR` / `M31A_STATE_DIR` to a shared tempdir opts into shared global state across workspaces (used by multi-workspace contract tests).

#### Types & Trait Declarations
- **Structs (1):** `StorageLayout`
- **Enums (2):** `ConfigScope`, `StorageClass`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn as_str(self) -> &'static str;
// pub
fn parse(s: &str) -> Option<Self>;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(workspace_root: impl Into<PathBuf>, channel: DeploymentChannel) -> Self;
// pub
fn for_workspace(workspace_root: impl Into<PathBuf>) -> Self;
// pub
fn channel(&self) -> DeploymentChannel;
// pub
fn workspace_root(&self) -> &Path;
// pub
fn deployment(&self) -> &DeploymentPaths;
// private
fn has_override(dev_name: &str, shared_name: &str) -> bool;
// private
fn uses_isolated_global(&self) -> bool;
// private
fn isolated_global_root(&self) -> PathBuf;
// private
fn resolve_dir(&self, kind: &str, platform: PathBuf) -> PathBuf;
// pub
fn user_config_dir(&self) -> PathBuf;
// pub
fn user_config_file(&self) -> PathBuf;
// pub
fn user_data_dir(&self) -> PathBuf;
```

---
