# Change Management

> **Architectural Layer:** L6 Execution  
> **Source Directory:** `src/change`  
> **File Count:** 7 source files  

Workspace change application, review, provenance, authority, and reconciliation.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [applier.rs](#src-change-applier-rs) | 531 | `AppliedChangeSet, AtomicChangeApplier, RollbackReport` | Atomic multi-file change applier with full rollback guarantees.  Appli... |
| [authority.rs](#src-change-authority-rs) | 850 | `ChangeAuthority, ChangeExecutionOutcome, ChangeAuthorityError` | Canonical Change Authority coordinating software modification lifecycl... |
| [mod.rs](#src-change-mod-rs) | 25 | `Functions/Traits` | Autonomous Code Modification &amp; Change Authority Subsystem.  Core p... |
| [observer.rs](#src-change-observer-rs) | 299 | `FreshMutationEvidence, PostMutationObserver` | Post-mutation repository observation and fresh context compiler.  Mand... |
| [provenance.rs](#src-change-provenance-rs) | 259 | `ChangeProvenanceStore` | Change provenance and requirement traceability store.  Enforces: - Eve... |
| [reconciler.rs](#src-change-reconciler-rs) | 512 | `PreMutationReconciler` | Pre-mutation repository reconciler.  Validates that a proposed change ... |
| [review.rs](#src-change-review-rs) | 231 | `DiffReviewer` | Diff self-review and anti-fake verification engine.  Enforces: - AGENT... |

---

### `src/change/applier.rs` {#src-change-applier-rs}

- **Source Link:** [`src/change/applier.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/change/applier.rs)
- **Lines of Code:** 531 (21461 bytes)

#### Primary Responsibility
Atomic multi-file change applier with full rollback guarantees.  Applies all mutations in a ChangeProposal sequentially. If any mutation fails (diagnostic mismatch, out of bounds, I/O error), ALL changes in the proposal are immediately rolled back to their exact pre-proposal bytes. The workspace is never left in a partially mutated or corrupt state.

#### Types & Trait Declarations
- **Structs (3):** `AppliedChangeSet`, `AtomicChangeApplier`, `RollbackReport`
- **Enums (1):** `ChangeApplyError`

#### Key Functions & Signatures (5 shown)
```rust
// pub
async fn rollback(&self,
        fs: &Arc<dyn FileSystemService>,) -> Result<RollbackReport, std::io::Error>;
// pub
async fn apply(workspace_root: &Path,
        proposal: &ChangeProposal,
        fs: &Arc<dyn FileSystemService>,) -> Re;
// private
async fn apply_single_mutation(_full_path: &Path,
        rel_path: &Path,
        operation: &FileMutationOp,
        f;
// private
async fn test_atomic_apply_multi_file_happy_path();
// private
async fn test_atomic_apply_rolls_back_on_failure();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_atomic_apply_multi_file_happy_path`, `test_atomic_apply_rolls_back_on_failure`

---

### `src/change/authority.rs` {#src-change-authority-rs}

- **Source Link:** [`src/change/authority.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/change/authority.rs)
- **Lines of Code:** 850 (33986 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
Canonical Change Authority coordinating software modification lifecycles.  Enforces: The model proposes. The runtime decides.  Mutation-lane ownership (explicit architecture: two canonical lanes with type-visible boundaries, not duplicate authorities over the same semantic object):  ```text Lane A — governed single-file tool writes: model/tool action → ToolPipeline (11 stages: capability → policy → approval → sandbox) → workspace file → tool result + artifact Owner: ToolPipelineRunner. Scope: exactly one file per action.  Lane B — multi-file change proposals: model/tool action → ToolPipeline → ChangeAuthority:: execute_change_proposal (reconcile → reserve surface → atomic apply → observe → diff-review → provenance) → workspace mutation → change record Owner: ChangeAuthority. Scope: one proposal, N files, atomic with rollback. ```  Ownership boundaries: - Lane A never performs multi-file atomic proposals, reconciliation, diff self-review, or provenance recording. - Lane B never bypasses Lane A's invariants: proposal application goes through the same `FileSystemService` containment (workspace-root confinement, `../` escape rejection) and executes only after the pipeline's capability/policy/approval stages admitted the action. - Neither lane can bypass the other's safety invariants: Lane A actions cannot fabricate Lane B provenance records; Lane B proposals cannot

#### Types & Trait Declarations
- **Structs (2):** `ChangeAuthority`, `ChangeExecutionOutcome`
- **Enums (1):** `ChangeAuthorityError`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_pool(mut self, pool: SqlitePool) -> Self;
// pub
fn get_state(&self, proposal_id: ChangeProposalId) -> Option<ChangeSetState>;
// pub
fn reserve_surface(&self,
        task_id: TaskId,
        surface: &ChangeSurface,) -> Result<(), ReconciliationViolati;
// pub
fn release_surface(&self, task_id: TaskId);
// pub
fn reconcile(&self,
        workspace_root: &Path,
        proposal: &ChangeProposal,
        baseline: Option<&Reposito;
// pub
async fn execute_change_proposal(&self,
        workspace_root: &Path,
        proposal: &ChangeProposal,
        fs: &A;
// private
fn proposal_fingerprint(proposal: &ChangeProposal) -> String;
// private
async fn post_manifest(workspace_root: &Path, files: &[String]) -> Option<String>;
// private
async fn fence_record(&self,
        proposal: &ChangeProposal,
        fingerprint: &str,
        success: bool,
      ;
// private
fn set_state(&self, proposal_id: ChangeProposalId, state: ChangeSetState);
// private
fn compute_aggregate_hash(file_hashes: &[(String, Option<String>);
// private
async fn test_change_authority_end_to_end_accepted();
// private
async fn test_change_authority_rejects_fake_implementation_and_rolls_back();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_change_authority_end_to_end_accepted`, `test_change_authority_rejects_fake_implementation_and_rolls_back`, `test_provenance_cryptographic_hashes_accurate_and_verification_truthful`, `test_surface_reservation_released_on_rejected_diff`

---

### `src/change/mod.rs` {#src-change-mod-rs}

- **Source Link:** [`src/change/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/change/mod.rs)
- **Lines of Code:** 25 (1071 bytes)

#### Primary Responsibility
Autonomous Code Modification &amp; Change Authority Subsystem.  Core principle: The model proposes. The runtime decides.  Owns: - Pre-mutation reconciliation &amp; conflict detection (`PreMutationReconciler`) - Atomic multi-file mutation application with rollback (`AtomicChangeApplier`) - Post-mutation re-observation &amp; context refresh (`PostMutationObserver`) - Independent diff self-review rejecting fake success (`DiffReviewer`) - Change provenance and requirement traceability (`ChangeProvenanceStore`) - Change authority coordinator (`ChangeAuthority`)

---

### `src/change/observer.rs` {#src-change-observer-rs}

- **Source Link:** [`src/change/observer.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/change/observer.rs)
- **Lines of Code:** 299 (11379 bytes)

#### Primary Responsibility
Post-mutation repository observation and fresh context compiler.  Mandatory invariant: After modifying code, DO NOT continue reasoning from stale pre-edit context. Re-queries: - Fresh file content &amp; SHA-256 hashes - Affected symbols and definitions - Callers, callees, and impacted dependencies - Targeted tests discovered via BoundedQueryEngine - Fresh unified git diff of modifications

#### Types & Trait Declarations
- **Structs (2):** `FreshMutationEvidence`, `PostMutationObserver`

#### Key Functions & Signatures (5 shown)
```rust
// pub
async fn observe(workspace_root: &Path,
        files_modified: &[String],
        query_engine: Option<&BoundedQueryEng;
// pub
async fn observe_with_snapshots(workspace_root: &Path,
        files_modified: &[String],
        query_engine: Option<&;
// private
async fn generate_diff(workspace_root: &Path,
        files: &[String],
        snapshots: Option<&HashMap<PathBuf, Opti;
// pub
fn generate_file_unified_diff(file: &str,
        old_bytes: Option<&[u8]>,
        new_bytes: Option<&[u8]>,) -> String;
// private
async fn test_post_mutation_observe_captures_hashes();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_post_mutation_observe_captures_hashes`

---

### `src/change/provenance.rs` {#src-change-provenance-rs}

- **Source Link:** [`src/change/provenance.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/change/provenance.rs)
- **Lines of Code:** 259 (9318 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Change provenance and requirement traceability store.  Enforces: - Every mutation remains associated with: mission, requirement, task, change proposal. - Answers: "Which changes implement this requirement?" "Which requirement authorized this change?" "What changed in this file and was it verified?"

#### Types & Trait Declarations
- **Structs (1):** `ChangeProvenanceStore`

#### Key Functions & Signatures (7 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
async fn record(&self,
        record: &ChangeProvenanceRecord,
        pool: Option<&SqlitePool>,) -> Result<(), sqlx::;
// pub
async fn get_by_proposal(&self,
        proposal_id: ChangeProposalId,
        pool: Option<&SqlitePool>,) -> Result<Opt;
// pub
async fn list_for_requirement(&self,
        requirement_key: &str,
        pool: Option<&SqlitePool>,) -> Result<Vec<Ch;
// pub
async fn list_for_file(&self,
        file_path: &str,
        pool: Option<&SqlitePool>,) -> Result<Vec<ChangeProvenanc;
// private
fn decode_row(r: &sqlx::sqlite::SqliteRow) -> Result<ChangeProvenanceRecord, sqlx::Error>;
```

---

### `src/change/reconciler.rs` {#src-change-reconciler-rs}

- **Source Link:** [`src/change/reconciler.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/change/reconciler.rs)
- **Lines of Code:** 512 (19921 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Pre-mutation repository reconciler.  Validates that a proposed change still corresponds to current repository state: - File hashes match expected base states (stale patch detection) - Required files and expected symbols exist - Direct mutation of generated files is rejected - Protected runtime/repo paths (.git, .m31a) are blocked - Committed migrations/schemas cannot be altered - Competing concurrent task modifications on the same files are blocked - Pre-change impact and recommended tests are calculated via BoundedQueryEngine

#### Types & Trait Declarations
- **Structs (1):** `PreMutationReconciler`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn reconcile(workspace_root: &Path,
        proposal: &ChangeProposal,
        _baseline: Option<&RepositoryBaseline>,
 ;
// pub
fn detect_generated_file(content: &str, path: &str) -> Option<String>;
// private
fn test_reconcile_clean_success();
// private
fn test_reconcile_stale_hash_rejected();
// private
fn test_reconcile_generated_file_rejected();
// private
fn test_reconcile_concurrent_conflict_rejected();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_reconcile_clean_success`, `test_reconcile_stale_hash_rejected`, `test_reconcile_generated_file_rejected`, `test_reconcile_concurrent_conflict_rejected`

---

### `src/change/review.rs` {#src-change-review-rs}

- **Source Link:** [`src/change/review.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/change/review.rs)
- **Lines of Code:** 231 (8410 bytes)

#### Primary Responsibility
Diff self-review and anti-fake verification engine.  Enforces: - AGENTS.md Rule 5: Never fake success (rejects todo!(), unimplemented!(), empty stubs, mock returns). - AGENTS.md Rule 6: Completion requires evidence. - Section 21: Final diff corresponds strictly to assigned task (no accidental edits). - Section 23: Test assertions must not be weakened or deleted to mask failures.

#### Types & Trait Declarations
- **Structs (1):** `DiffReviewer`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn review(diff_text: &str,
        change_surface: &ChangeSurface,
        files_modified: &[String],) -> DiffReviewRepo;
// private
fn test_diff_review_clean_passes();
// pub
fn compute() -> u32;
// private
fn test_diff_review_detects_todo_macro();
// pub
fn compute() -> u32;
// private
fn test_diff_review_detects_commented_out_assertion();
// private
fn test_compute();
// private
fn test_diff_review_detects_scope_creep();
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_diff_review_clean_passes`, `test_diff_review_detects_todo_macro`, `test_diff_review_detects_commented_out_assertion`, `test_compute`, `test_diff_review_detects_scope_creep`

---
