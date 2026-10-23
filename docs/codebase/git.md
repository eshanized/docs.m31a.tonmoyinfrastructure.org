# Git & Worktree Isolation

> **Architectural Layer:** L2 Git Operations  
> **Source Directory:** `src/git`  
> **File Count:** 10 source files  

Worktree management, branch naming, isolated attribution, trailers, stash, and hosting.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [attribution.rs](#src-git-attribution-rs) | 242 | `CommitAttributionRecord, GitAttributionStore` | SQLite-backed Git commit attribution persistence (GST-03, D-03). |
| [authorization.rs](#src-git-authorization-rs) | 465 | `AuthorizationAuthority, GitMutationAuthorization` | Non-forgeable runtime authorization for Git mutations (SEC-GIT-01).  `... |
| [drift.rs](#src-git-drift-rs) | 194 | `TreeHashDriftDetector, TreeSnapshot, DriftStatus` | Cryptographic Tree-Hash Drift Detection (GST-04, D-04). |
| [hosting.rs](#src-git-hosting-rs) | 309 | `CheckRun, GitHubCliHostingProvider, PullRequest` | Remote repository hosting integration (GitHub, GitLab) for PR/MR workf... |
| [integration.rs](#src-git-integration-rs) | 404 | `IntegrationReport, WorktreeIntegrationStateMachine, IntegrationState` | Two-stage Worktree Integration State Machine (GST-01, GST-04, D-05). |
| [mod.rs](#src-git-mod-rs) | 458 | `GitGate, GitError, GitOperation` | Git integration, worktree isolation, commit trailers, and drift detect... |
| [probe.rs](#src-git-probe-rs) | 62 | `GitWorkspaceInfo` | Git workspace status probe (GST-01, FRX-02). |
| [stash.rs](#src-git-stash-rs) | 193 | `PrivateStashManager` | Private Git stash manager (GST-01, D-06). |
| [trailers.rs](#src-git-trailers-rs) | 175 | `CommitTrailers` | RFC-compliant Git commit trailers for provenance and attribution (GST-... |
| [worktree.rs](#src-git-worktree-rs) | 491 | `IsolatedWorktree, WorktreeConfig, WorktreeManager` | Git Worktree Isolation Manager (GST-01, D-01). |

---

### `src/git/attribution.rs` {#src-git-attribution-rs}

- **Source Link:** [`src/git/attribution.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/git/attribution.rs)
- **Lines of Code:** 242 (7795 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
SQLite-backed Git commit attribution persistence (GST-03, D-03).

#### Types & Trait Declarations
- **Structs (2):** `CommitAttributionRecord`, `GitAttributionStore`

#### Key Functions & Signatures (7 shown)
```rust
// pub
fn new(pool: SqlitePool) -> Self;
// pub
fn pool(&self) -> &SqlitePool;
// pub
async fn record_commit(&self,
        commit_hash: &str,
        trailers: &CommitTrailers,
        created_at: Option<D;
// pub
async fn find_by_commit(&self,
        commit_hash: &str,) -> Result<Option<CommitAttributionRecord>, GitError>;
// pub
async fn find_by_task(&self,
        task_id: &TaskId,) -> Result<Vec<CommitAttributionRecord>, GitError>;
// pub
async fn find_by_mission(&self,
        mission_id: &MissionId,) -> Result<Vec<CommitAttributionRecord>, GitError>;
// pub
async fn find_by_model(&self,
        model_id: &str,) -> Result<Vec<CommitAttributionRecord>, GitError>;
```

---

### `src/git/authorization.rs` {#src-git-authorization-rs}

- **Source Link:** [`src/git/authorization.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/git/authorization.rs)
- **Lines of Code:** 465 (16239 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Non-forgeable runtime authorization for Git mutations (SEC-GIT-01).  `GitGate::authorized()` as a zero-argument boolean is removed as a security primitive. Git mutations require a [`GitMutationAuthorization`] minted by the [`AuthorizationAuthority`] held by the runtime composition root and bound to the exact execution being performed:  ```text authorization_id / mission_id / task_id / agent_id / request_id / policy_hash / workspace_root / operation / resource_scope / expiry / approval provenance ```  The binding tag is an HMAC-style SHA-256 over a per-instance secret and the canonical field encoding. A gate minted for one mission, workspace, operation, or policy generation does not verify for any other. Callers cannot fabricate authorization without the authority instance.

#### Types & Trait Declarations
- **Structs (2):** `AuthorizationAuthority`, `GitMutationAuthorization`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn mint_git_authorization(&self,
        mission_id: MissionId,
        task_id: Option<TaskId>,
        agent_id: Optio;
// pub
fn verify(&self, auth: &GitMutationAuthorization) -> bool;
// private
fn tag_for(&self, auth: &GitMutationAuthorization) -> String;
// private
fn constant_time_eq(a: &[u8], b: &[u8]) -> bool;
// pub
fn is_expired(&self) -> bool;
// pub
fn covers(&self, op: &GitOperation, workspace_root: &Path) -> bool;
// pub
fn verify_for(&self,
        authority: &AuthorizationAuthority,
        op: &GitOperation,
        workspace_root: &Pat;
// pub
fn authorization_commit_base(message: &str) -> String;
// private
fn normalize(p: &Path) -> PathBuf;
// private
fn operations_match(stored: &GitOperation, candidate: &GitOperation) -> bool;
// private
fn strip_commit_auth_trailer(message: &str) -> (String, Option<String>);
// private
fn commit_auth_trailer_id(message: &str) -> Option<String>;
// private
fn authority() -> AuthorizationAuthority;
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`minted_authorization_verifies`, `tampered_operation_fails_closed`, `wrong_workspace_fails_closed`, `foreign_authority_fails_closed`, `expired_authorization_fails_closed`

---

### `src/git/drift.rs` {#src-git-drift-rs}

- **Source Link:** [`src/git/drift.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/git/drift.rs)
- **Lines of Code:** 194 (6850 bytes)

#### Primary Responsibility
Cryptographic Tree-Hash Drift Detection (GST-04, D-04).

#### Types & Trait Declarations
- **Structs (2):** `TreeHashDriftDetector`, `TreeSnapshot`
- **Enums (1):** `DriftStatus`

#### Key Functions & Signatures (7 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_event_bus(mut self, event_bus: Arc<dyn EventBus>) -> Self;
// pub
async fn compute_tree_hash(&self, worktree_path: &Path) -> Result<String, GitError>;
// private
async fn run_with_temp_index(worktree_path: &Path,
        temp_index_path: &Path,
        args: &[&str],) -> Result<std;
// pub
async fn record_snapshot(&self, worktree_path: &Path) -> Result<TreeSnapshot, GitError>;
// pub
async fn check_drift(&self,
        mission_id: &MissionId,
        worktree_path: &Path,
        expected: &TreeSnapsho;
```

---

### `src/git/hosting.rs` {#src-git-hosting-rs}

- **Source Link:** [`src/git/hosting.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/git/hosting.rs)
- **Lines of Code:** 309 (9675 bytes)

#### Primary Responsibility
Remote repository hosting integration (GitHub, GitLab) for PR/MR workflows (Issue 16).  Provides a typed provider abstraction for creating PRs, checking status, posting review comments, and inspecting CI check runs, with fail-safe local/mock fallbacks and secret redaction.

#### Types & Trait Declarations
- **Structs (5):** `CheckRun`, `GitHubCliHostingProvider`, `PullRequest`, `PullRequestStatus`, `ReviewComment`
- **Traits (1):** `RepoHostingProvider`

#### Key Functions & Signatures (10 shown)
```rust
// private
async fn create_pull_request(&self,
        title: &str,
        body: &str,
        source_branch: &str,
        target;
// private
async fn get_pull_request_status(&self, pr_id: u64) -> Result<PullRequestStatus, GitError>;
// private
async fn post_review_comment(&self,
        pr_id: u64,
        body: &str,
        path: Option<&str>,
        line: Op;
// private
async fn list_check_runs(&self, ref_name: &str) -> Result<Vec<CheckRun>, GitError>;
// pub
fn new(workspace_root: impl Into<PathBuf>) -> Self;
// private
async fn is_gh_available(&self) -> bool;
// private
async fn create_pull_request(&self,
        title: &str,
        body: &str,
        source_branch: &str,
        target;
// private
async fn get_pull_request_status(&self, pr_id: u64) -> Result<PullRequestStatus, GitError>;
// private
async fn post_review_comment(&self,
        pr_id: u64,
        body: &str,
        path: Option<&str>,
        line: Op;
// private
async fn list_check_runs(&self, ref_name: &str) -> Result<Vec<CheckRun>, GitError>;
```

---

### `src/git/integration.rs` {#src-git-integration-rs}

- **Source Link:** [`src/git/integration.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/git/integration.rs)
- **Lines of Code:** 404 (16365 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Two-stage Worktree Integration State Machine (GST-01, GST-04, D-05).

#### Types & Trait Declarations
- **Structs (2):** `IntegrationReport`, `WorktreeIntegrationStateMachine`
- **Enums (2):** `IntegrationState`, `MergeStrategy`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn new(repo_root: impl Into<PathBuf>) -> Self;
// pub
fn state(&self) -> IntegrationState;
// pub
async fn integrate(&mut self,
        worktree: &IsolatedWorktree,
        target_branch: &str,
        strategy: MergeS;
// private
async fn cleanup_temp_worktree(&self,
        temp_path_str: &str,
        temp_path: &std::path::Path,) -> Result<(), G;
```

---

### `src/git/mod.rs` {#src-git-mod-rs}

- **Source Link:** [`src/git/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/git/mod.rs)
- **Lines of Code:** 458 (16681 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Git integration, worktree isolation, commit trailers, and drift detection (GST-01–GST-04, D-01–D-06).

#### Types & Trait Declarations
- **Structs (1):** `GitGate`
- **Enums (2):** `GitError`, `GitOperation`

#### Key Functions & Signatures (13 shown)
```rust
// pub
fn is_remote(&self) -> bool;
// pub
fn is_destructive(&self) -> bool;
// pub
fn requires_authorization(&self) -> bool;
// pub
fn default_policy_decision(&self) -> PolicyDecision;
// pub
fn enforce_policy(&self, approved: bool) -> Result<(), GitError>;
// pub
fn authorized_verified(authorization: GitMutationAuthorization,
        authority: &AuthorizationAuthority,) -> Result<S;
// pub
fn denied() -> Self;
// pub
fn authorization(&self) -> Option<&GitMutationAuthorization>;
// pub
fn enforce(&self,
        op: &GitOperation,
        workspace_root: &std::path::Path,) -> Result<(), GitError>;
// pub
fn validate_git_ref_arg(kind: &str, value: &str) -> Result<(), GitError>;
// pub
fn validate_git_sha(kind: &str, value: &str) -> Result<(), GitError>;
// pub
fn scoped_git_command() -> tokio::process::Command;
// pub
async fn run_scoped_git(current_dir: &std::path::Path,
    args: &[&str],
    timeout: std::time::Duration,) -> Result<s;
```

---

### `src/git/probe.rs` {#src-git-probe-rs}

- **Source Link:** [`src/git/probe.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/git/probe.rs)
- **Lines of Code:** 62 (1813 bytes)

#### Primary Responsibility
Git workspace status probe (GST-01, FRX-02).

#### Types & Trait Declarations
- **Structs (1):** `GitWorkspaceInfo`

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn probe(workspace_path: &Path) -> Self;
```

---

### `src/git/stash.rs` {#src-git-stash-rs}

- **Source Link:** [`src/git/stash.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/git/stash.rs)
- **Lines of Code:** 193 (7258 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Private Git stash manager (GST-01, D-06).

#### Types & Trait Declarations
- **Structs (1):** `PrivateStashManager`

#### Key Functions & Signatures (7 shown)
```rust
// pub
fn new(repo_root: impl Into<PathBuf>) -> Self;
// pub
fn stash_ref(mission_id: &MissionId) -> String;
// pub
async fn save(&self,
        mission_id: &MissionId,
        message: Option<&str>,
        gate: &GitGate,) -> Result<O;
// pub
async fn apply(&self, mission_id: &MissionId, gate: &GitGate) -> Result<(), GitError>;
// pub
async fn pop(&self, mission_id: &MissionId, gate: &GitGate) -> Result<(), GitError>;
// pub
async fn drop(&self, mission_id: &MissionId, gate: &GitGate) -> Result<(), GitError>;
// pub
async fn has_stash(&self, mission_id: &MissionId) -> Result<bool, GitError>;
```

---

### `src/git/trailers.rs` {#src-git-trailers-rs}

- **Source Link:** [`src/git/trailers.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/git/trailers.rs)
- **Lines of Code:** 175 (6861 bytes)

#### Primary Responsibility
RFC-compliant Git commit trailers for provenance and attribution (GST-03, D-02, D-03).

#### Types & Trait Declarations
- **Structs (1):** `CommitTrailers`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn new(mission_id: MissionId,
        task_id: TaskId,
        agent_role: AgentRole,
        model_id: impl Into<String;
// pub
fn for_governed_execution(mission_id: MissionId,
        task_id: TaskId,
        agent_id: Option<AgentId>,
        age;
// pub
fn with_agent_id(mut self, agent_id: AgentId) -> Self;
// pub
fn with_authorization(mut self, authorization_id: impl Into<String>) -> Self;
// pub
fn with_verification(mut self, run_id: impl Into<String>) -> Self;
// pub
fn format_trailers(&self) -> String;
// pub
fn embed_trailers(commit_msg: &str, trailers: &CommitTrailers) -> Result<String, GitError>;
// pub
fn parse_trailers(commit_msg: &str) -> Result<CommitTrailers, GitError>;
```

---

### `src/git/worktree.rs` {#src-git-worktree-rs}

- **Source Link:** [`src/git/worktree.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/git/worktree.rs)
- **Lines of Code:** 491 (17412 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Git Worktree Isolation Manager (GST-01, D-01).

#### Types & Trait Declarations
- **Structs (3):** `IsolatedWorktree`, `WorktreeConfig`, `WorktreeManager`
- **Enums (1):** `WorktreeRetentionPolicy`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(repo_root: impl Into<PathBuf>) -> Self;
// pub
fn with_retention(mut self, policy: WorktreeRetentionPolicy) -> Self;
// pub
fn with_worktrees_dir(mut self, dir: impl Into<PathBuf>) -> Self;
// pub
fn new(config: WorktreeConfig) -> Self;
// pub
fn config(&self) -> &WorktreeConfig;
// pub
fn worktree_path(&self, mission_id: &MissionId) -> PathBuf;
// pub
fn branch_name(mission_id: &MissionId) -> String;
// pub
async fn ensure_git_excludes(repo_root: &std::path::Path) -> Result<(), GitError>;
// pub
async fn create_worktree(&self,
        mission_id: &MissionId,
        base_commit: Option<&str>,
        gate: &GitGat;
// pub
async fn mission_branch_exists(&self, mission_id: &MissionId) -> Result<bool, GitError>;
// pub
async fn remove_worktree(&self,
        worktree: &IsolatedWorktree,
        force: bool,
        gate: &GitGate,) -> Re;
// pub
async fn prune_worktrees(&self) -> Result<usize, GitError>;
```

---
