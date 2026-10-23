# Repository Intelligence

> **Architectural Layer:** L2 Repository  
> **Source Directory:** `src/repo`  
> **File Count:** 13 source files  

Code search, symbol extraction, dependency graph, and workspace drift detection.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [cache.rs](#src-repo-cache-rs) | 494 | `SqliteRepoCache` | Subsystem component |
| [drift.rs](#src-repo-drift-rs) | 738 | `BaselineCaptureReport, DriftReport, RepositoryBaseline` | Subsystem component |
| [manifest.rs](#src-repo-extract-manifest-rs) | 428 | `CargoPackage, CargoTarget, CargoToml` | Subsystem component |
| [mod.rs](#src-repo-extract-mod-rs) | 9 | `Functions/Traits` | Subsystem component |
| [python.rs](#src-repo-extract-python-rs) | 390 | `PythonExtractor` | Subsystem component |
| [rust.rs](#src-repo-extract-rust-rs) | 541 | `MyStruct, RustAstExtractor, Color` | Subsystem component |
| [typescript.rs](#src-repo-extract-typescript-rs) | 477 | `TypeScriptExtractor` | Subsystem component |
| [graph.rs](#src-repo-graph-rs) | 738 | `RepositoryGraph, RepositoryEdgeKind, RepositoryNode` | Subsystem component |
| [lsp.rs](#src-repo-lsp-rs) | 1021 | `HoverInfo, LspQueryResult, LspService` | Language Server Protocol (LSP) and deep code intelligence subsystem (I... |
| [mod.rs](#src-repo-mod-rs) | 19 | `Functions/Traits` | Repository intelligence and code graph subsystem. |
| [query.rs](#src-repo-query-rs) | 1169 | `BoundedQueryEngine, BoundedQueryResult, ChangeImpactReport` | Subsystem component |
| [scanner.rs](#src-repo-scanner-rs) | 804 | `GitIgnoreFilter, RepositoryScanner, ScanSummary` | Subsystem component |
| [types.rs](#src-repo-types-rs) | 798 | `EntryPoint, EvidenceProvenance, RepositorySymbol` | Subsystem component |

---

### `src/repo/cache.rs` {#src-repo-cache-rs}

- **Source Link:** [`src/repo/cache.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/repo/cache.rs)
- **Lines of Code:** 494 (16116 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (1):** `SqliteRepoCache`

#### Key Functions & Signatures (11 shown)
```rust
// pub
fn new(pool: SqlitePool) -> Self;
// pub
async fn sync_file(&self,
        file_path: &str,
        content_hash: &str,
        language: &str,
        symbols: ;
// pub
async fn sync_edges(&self,
        edges: &[(&str, &str, RepositoryEdgeKind);
// pub
async fn load_cached_symbols(&self) -> Result<Vec<RepositorySymbol>, sqlx::Error>;
// pub
async fn rebuild_graph_from_cache(&self,
        generation_id: u64,) -> Result<RepositoryGraph, sqlx::Error>;
// pub
async fn remove_file(&self, file_path: &str) -> Result<(), sqlx::Error>;
// pub
async fn sync_scan(&self, summary: &ScanSummary) -> Result<usize, sqlx::Error>;
// private
async fn create_test_db() -> SqlitePool;
// private
async fn test_sqlite_repo_cache_incremental_sync();
// private
async fn test_sqlite_repo_cache_rebuild_graph();
// private
async fn test_sync_scan_and_remove_file();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_sqlite_repo_cache_incremental_sync`, `test_sqlite_repo_cache_rebuild_graph`, `test_sync_scan_and_remove_file`

---

### `src/repo/drift.rs` {#src-repo-drift-rs}

- **Source Link:** [`src/repo/drift.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/repo/drift.rs)
- **Lines of Code:** 738 (29624 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (3):** `BaselineCaptureReport`, `DriftReport`, `RepositoryBaseline`

#### Key Functions & Signatures (12 shown)
```rust
// private
fn record_excluded(&mut self, reason: &str, rel: &str);
// private
fn record_skipped(&mut self, detail: String);
// pub
fn new(mission_id: MissionId,
        task_id: Option<TaskId>,
        git_commit: Option<String>,
        file_hashes: ;
// pub
fn capture(workspace_root: &Path,
        mission_id: MissionId,
        task_id: Option<TaskId>,
        git_commit: Op;
// pub
fn capture_with_report(workspace_root: &Path,
        mission_id: MissionId,
        task_id: Option<TaskId>,
        gi;
// private
fn collect_hashes(base: &Path,
        canonical_base: &Path,
        dir: &Path,
        depth: usize,
        visited:;
// pub
async fn save_to_db(&self, pool: &SqlitePool) -> Result<(), sqlx::Error>;
// pub
async fn load_latest_for_mission(pool: &SqlitePool,
        mission_id: MissionId,) -> Result<Option<Self>, sqlx::Error>;
// pub
fn detect_drift(baseline: &RepositoryBaseline,
    current_hashes: &BTreeMap<String, String>,
    authorized_mutations: ;
// private
fn test_capture_and_drift_detection();
// private
async fn test_baseline_sqlite_persistence();
// private
fn test_baseline_capture_symlink_confinement_and_cycle_prevention();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_capture_and_drift_detection`, `test_baseline_sqlite_persistence`, `test_baseline_capture_symlink_confinement_and_cycle_prevention`

---

### `src/repo/extract/manifest.rs` {#src-repo-extract-manifest-rs}

- **Source Link:** [`src/repo/extract/manifest.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/repo/extract/manifest.rs)
- **Lines of Code:** 428 (13223 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (9):** `CargoPackage`, `CargoTarget`, `CargoToml`, `ManifestExtractor`, `PackageJson`, `PoetryDetails`, `PyProjectDetails`, `PyProjectToml`, `PyProjectTool`

#### Key Functions & Signatures (5 shown)
```rust
// pub
fn extract_cargo(file_path: &str, content: &str) -> Result<Vec<RepositorySymbol>, String>;
// pub
fn extract_package_json(file_path: &str,
        content: &str,) -> Result<Vec<RepositorySymbol>, String>;
// pub
fn extract_pyproject(file_path: &str,
        content: &str,) -> Result<Vec<RepositorySymbol>, String>;
// private
fn test_cargo_manifest_extraction();
// private
fn test_package_json_extraction();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_cargo_manifest_extraction`, `test_package_json_extraction`

---

### `src/repo/extract/mod.rs` {#src-repo-extract-mod-rs}

- **Source Link:** [`src/repo/extract/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/repo/extract/mod.rs)
- **Lines of Code:** 9 (212 bytes)

#### Primary Responsibility
Internal implementation file.

---

### `src/repo/extract/python.rs` {#src-repo-extract-python-rs}

- **Source Link:** [`src/repo/extract/python.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/repo/extract/python.rs)
- **Lines of Code:** 390 (13860 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (1):** `PythonExtractor`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn extract(file_path: &str, content: &str) -> Vec<RepositorySymbol>;
// pub
fn extract_with_edges(file_path: &str,
        content: &str,) -> (
        Vec<RepositorySymbol>,
        Vec<(String, ;
// private
fn extract_doc_and_extent(lines: &[&str],
        start_idx: usize,
        base_indent: usize,) -> (Option<String>, usi;
// private
fn test_python_extractor();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_python_extractor`

---

### `src/repo/extract/rust.rs` {#src-repo-extract-rust-rs}

- **Source Link:** [`src/repo/extract/rust.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/repo/extract/rust.rs)
- **Lines of Code:** 541 (18396 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (2):** `MyStruct`, `RustAstExtractor`
- **Enums (1):** `Color`
- **Traits (1):** `Greeter`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(file_path: impl Into<String>, content: &'a str) -> Self;
// pub
fn extract(file_path: &str, content: &'a str) -> Result<Vec<RepositorySymbol>, String>;
// pub
fn extract_with_edges(file_path: &str,
        content: &'a str,) -> Result<ExtractedSymbolsAndEdges, String>;
// private
fn byte_offset_to_line(&self, offset: usize) -> usize;
// private
fn locate_item(&self, keyword: &str, ident: &str) -> (usize, usize, String);
// private
fn extract_doc_comments(attrs: &[syn::Attribute]) -> Option<String>;
// private
fn qualified_prefix(&self) -> String;
// private
fn visit_item_fn(&mut self, node: &'ast ItemFn);
// private
fn visit_item_struct(&mut self, node: &'ast ItemStruct);
// private
fn visit_item_enum(&mut self, node: &'ast ItemEnum);
// private
fn visit_item_trait(&mut self, node: &'ast ItemTrait);
// private
fn visit_item_mod(&mut self, node: &'ast ItemMod);
// private
fn visit_item_use(&mut self, node: &'ast ItemUse);
// private
fn collect_use_paths(tree: &UseTree, prefix: &str, acc: &mut Vec<String>);
// private
fn visit_expr_call(&mut self, node: &'ast ExprCall);
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_rust_ast_extractor_functions_and_structs`

---

### `src/repo/extract/typescript.rs` {#src-repo-extract-typescript-rs}

- **Source Link:** [`src/repo/extract/typescript.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/repo/extract/typescript.rs)
- **Lines of Code:** 477 (16280 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (1):** `TypeScriptExtractor`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn extract(file_path: &str, content: &str) -> Vec<RepositorySymbol>;
// pub
fn extract_with_edges(file_path: &str,
        content: &str,) -> (
        Vec<RepositorySymbol>,
        Vec<(String, ;
// private
fn find_closing_brace(lines: &[&str], start_idx: usize) -> usize;
// private
fn test_typescript_extractor();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_typescript_extractor`

---

### `src/repo/graph.rs` {#src-repo-graph-rs}

- **Source Link:** [`src/repo/graph.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/repo/graph.rs)
- **Lines of Code:** 738 (25001 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (1):** `RepositoryGraph`
- **Enums (2):** `RepositoryEdgeKind`, `RepositoryNode`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn as_symbol(&self) -> Option<&RepositorySymbol>;
// pub
fn as_file_path(&self) -> Option<&str>;
// pub
fn as_str(&self) -> &'static str;
// pub
fn from_str_name(s: &str) -> Option<Self>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// pub
fn new(generation_id: u64) -> Self;
// pub
fn set_file_hash(&mut self, path: impl Into<String>, hash: impl Into<String>);
// pub
fn get_file_hash(&self, path: &str) -> Option<&str>;
// pub
fn from_scan_summary(summary: &crate::repo::scanner::ScanSummary,
        generation_id: u64,) -> Self;
// pub
fn add_file(&mut self, path: &str, language: &str) -> NodeIndex;
// pub
fn add_symbol(&mut self,
        symbol: RepositorySymbol,
        parent_file_idx: Option<NodeIndex>,) -> NodeIndex;
// pub
fn add_relationship(&mut self,
        source_id: &str,
        target_id: &str,
        kind: RepositoryEdgeKind,) -> b;
// pub
fn invalidate_file(&mut self, path: &str);
// pub
fn get_symbol(&self, symbol_id: &str) -> Option<&RepositorySymbol>;
// pub
fn get_file_symbols(&self, path: &str) -> Vec<&RepositorySymbol>;
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_repository_graph_add_and_invalidate`, `test_generation_isolation`, `test_tests_and_relationship_queries`, `test_entry_points_and_classifications`

---

### `src/repo/lsp.rs` {#src-repo-lsp-rs}

- **Source Link:** [`src/repo/lsp.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/repo/lsp.rs)
- **Lines of Code:** 1021 (38257 bytes)

#### Primary Responsibility
Language Server Protocol (LSP) and deep code intelligence subsystem (Issue 12).  Provides typed code navigation, hover documentation, definition lookups, and reference finding across Rust (`rust-analyzer`), TypeScript (`typescript-language-server`), Python (`pyright`/`pylsp`), and Go (`gopls`), with automatic fallbacks to syntactic and code-graph search when language servers are unavailable.

#### Types & Trait Declarations
- **Structs (5):** `HoverInfo`, `LspQueryResult`, `LspService`, `SourceLocation`, `SymbolInfo`
- **Enums (1):** `LspBackend`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(workspace_root: impl Into<PathBuf>) -> Self;
// pub
fn with_server_override(mut self, cmd: impl Into<String>) -> Self;
// pub
async fn active_backend(&self) -> LspBackend;
// pub
async fn detect_backend(&self) -> LspBackend;
// private
async fn query_stdio(&self,
        backend: LspBackend,
        method: &str,
        params: serde_json::Value,) -> Re;
// pub
async fn did_open(&self,
        file_path: &Path,
        content: &str,
        language_id: &str,) -> Result<(), Stri;
// pub
async fn did_change(&self, file_path: &Path, content: &str) -> Result<(), String>;
// pub
async fn did_close(&self, file_path: &Path) -> Result<(), String>;
// pub
async fn shutdown(&self) -> Result<(), String>;
// pub
async fn goto_definition(&self,
        file_path: &str,
        line: usize,
        col: usize,
        symbol_name: O;
// pub
async fn find_references(&self,
        file_path: &str,
        line: usize,
        col: usize,
        symbol_name: O;
// pub
async fn hover(&self,
        file_path: &str,
        line: usize,
        col: usize,
        symbol_name: Option<&str;
// pub
async fn workspace_symbols(&self,
        query: &str,) -> Result<LspQueryResult<Vec<SymbolInfo>>, String>;
// private
async fn extract_symbol_at(&self,
        file_path: &str,
        line: usize,
        col: usize,) -> Result<String, S;
// private
async fn fallback_find_definitions(&self, symbol: &str) -> Result<Vec<SourceLocation>, String>;
```

---

### `src/repo/mod.rs` {#src-repo-mod-rs}

- **Source Link:** [`src/repo/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/repo/mod.rs)
- **Lines of Code:** 19 (324 bytes)

#### Primary Responsibility
Repository intelligence and code graph subsystem.

---

### `src/repo/query.rs` {#src-repo-query-rs}

- **Source Link:** [`src/repo/query.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/repo/query.rs)
- **Lines of Code:** 1169 (39478 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (5):** `BoundedQueryEngine`, `BoundedQueryResult`, `ChangeImpactReport`, `QueryBounds`, `SymbolNeighborhood`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn new(max_results: usize, max_depth: usize, max_bytes: usize) -> Self;
// pub
fn from_configured(max_results: usize, max_depth: usize, max_bytes: usize) -> Self;
// pub
fn clamped(&self) -> Self;
// private
fn paginate_and_bound(items: Vec<T>,
    bounds: QueryBounds,) -> BoundedQueryResult<Vec<T>>;
// pub
fn new(graph: Arc<RepositoryGraph>) -> Self;
// pub
fn with_workspace_root(mut self, root: impl Into<PathBuf>) -> Self;
// pub
fn graph(&self) -> &Arc<RepositoryGraph>;
// pub
fn workspace_root(&self) -> Option<&Path>;
// pub
fn get_symbol(&self, symbol_id: &str) -> Option<RepositorySymbol>;
// pub
fn find_symbols(&self,
        query: &str,
        bounds: QueryBounds,) -> BoundedQueryResult<Vec<RepositorySymbol>>;
// pub
fn get_file_outline(&self,
        path: &str,
        bounds: QueryBounds,) -> BoundedQueryResult<Vec<RepositorySymbol>;
// pub
fn get_neighborhood(&self,
        symbol_id: &str,
        bounds: QueryBounds,) -> Option<BoundedQueryResult<SymbolNei;
// pub
fn find_tests_for_symbol(&self,
        symbol_id: &str,
        bounds: QueryBounds,) -> BoundedQueryResult<Vec<Reposit;
// pub
fn find_tests_for_file(&self,
        file_path: &str,
        bounds: QueryBounds,) -> BoundedQueryResult<Vec<String>>;
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_query_bounds_ceiling_enforcement`, `test_find_symbols_bounded`, `test_get_neighborhood_traversal`, `test_get_file_outline`, `test_repository_query_methods`

---

### `src/repo/scanner.rs` {#src-repo-scanner-rs}

- **Source Link:** [`src/repo/scanner.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/repo/scanner.rs)
- **Lines of Code:** 804 (27911 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (4):** `GitIgnoreFilter`, `RepositoryScanner`, `ScanSummary`, `ScannedFile`
- **Enums (1):** `SourceLanguage`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// pub
fn detect_from_path(path: &Path) -> Self;
// pub
fn is_binary_content(sample: &[u8]) -> bool;
// pub
fn classify_file(relative_path: &str,
    is_binary: bool,
    content_sample: &[u8],) -> FileClassification;
// pub
fn detect_subsystem(relative_path: &str) -> Option<SubsystemKind>;
// pub
fn new() -> Self;
// pub
fn load_from_dir(root: &Path) -> Self;
// pub
fn matches(&self, relative_path: &str, is_dir: bool) -> bool;
// private
fn glob_match(pattern: &str, text: &str) -> bool;
// pub
fn new(workspace_root: impl Into<PathBuf>) -> Self;
// pub
fn with_exclusions(mut self, exclusions: Vec<String>) -> Self;
// pub
fn scan(&self) -> Result<ScanSummary, std::io::Error>;
// private
fn walk_dir(&self, dir: &Path, callback: &mut F) -> Result<(), std::io::Error>
    where
        F: FnMut(&Path),;
// private
fn walk_dir_bounded(&self,
        dir: &Path,
        depth: usize,
        visited: &mut std::collections::HashSet<Pat;
// private
fn test_repository_scanner_walk_and_routing();
```

#### Unit Verification (3 inline tests)
Tests defined within module:
`test_repository_scanner_walk_and_routing`, `test_gitignore_and_classification_and_subsystems`, `test_binary_detection_and_size_guard`

---

### `src/repo/types.rs` {#src-repo-types-rs}

- **Source Link:** [`src/repo/types.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/repo/types.rs)
- **Lines of Code:** 798 (25301 bytes)

#### Primary Responsibility
Internal implementation file.

#### Types & Trait Declarations
- **Structs (4):** `EntryPoint`, `EvidenceProvenance`, `RepositorySymbol`, `SourceSlice`
- **Enums (9):** `AnalysisMethod`, `EntryPointKind`, `FactClass`, `FileClassification`, `FileStaleness`, `IndexStatus`, `SourceSliceKind`, `SubsystemKind`, `SymbolKind`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// pub
fn from_str_name(s: &str) -> Option<Self>;
// pub
fn is_verified(&self) -> bool;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// pub
fn as_str(&self) -> &'static str;
// pub
fn from_str_name(s: &str) -> Option<Self>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// pub
fn new(id: impl Into<String>,
        name: impl Into<String>,
        qualified_name: impl Into<String>,
        kind: ;
// pub
fn with_test(mut self, is_test: bool) -> Self;
// pub
fn with_provenance(mut self, provenance: EvidenceProvenance) -> Self;
// pub
fn as_str(&self) -> &'static str;
// pub
fn from_str_name(s: &str) -> Option<Self>;
// pub
fn is_source_or_test(&self) -> bool;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// pub
fn as_str(&self) -> &'static str;
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_fact_class_serde_and_display`, `test_symbol_kind_serde_and_display`, `test_repository_symbol_creation`, `test_file_classification_and_subsystems`, `test_provenance_and_entry_point`

---
