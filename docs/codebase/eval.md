# Autonomous Evaluation Harness

> **Architectural Layer:** L7 Verification  
> **Source Directory:** `src/eval`  
> **File Count:** 13 source files  

Acceptance test scenarios A through H, scoring, and automated evaluation runner.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [fixture.rs](#src-eval-fixture-rs) | 235 | `FixtureRepo, FixtureRepoBuilder` | Programmatic temporary Git fixture repository builder (D-15, TST-03). ... |
| [mod.rs](#src-eval-mod-rs) | 14 | `Functions/Traits` | Autonomous evaluation harness, fixture builder, and acceptance scenari... |
| [runner.rs](#src-eval-runner-rs) | 136 | `EvalRunner` | Autonomous Evaluation Runner Engine (D-15, TST-01..03, TST-06).  Orche... |
| [mod.rs](#src-eval-scenarios-mod-rs) | 99 | `ScenarioResult, EvaluationExecutionMode, ScenarioStatus` | Acceptance Scenarios A through H implementation (CONTEXT_M31A.md §99, ... |
| [scenario_a.rs](#src-eval-scenarios-scenario_a-rs) | 125 | `ScenarioA` | Acceptance Scenario A: Simple Bug Fix (CONTEXT_M31A.md §99, TST-01).  ... |
| [scenario_b.rs](#src-eval-scenarios-scenario_b-rs) | 120 | `ScenarioB` | Acceptance Scenario B: Multi-File Feature (CONTEXT_M31A.md §99, TST-01... |
| [scenario_c.rs](#src-eval-scenarios-scenario_c-rs) | 231 | `ScenarioC` | Acceptance Scenario C: Failure and DAG Replan (CONTEXT_M31A.md §99, TS... |
| [scenario_d.rs](#src-eval-scenarios-scenario_d-rs) | 107 | `ScenarioD` | Acceptance Scenario D: Policy Denial (CONTEXT_M31A.md §99, TST-01, SEC... |
| [scenario_e.rs](#src-eval-scenarios-scenario_e-rs) | 112 | `ScenarioE` | Acceptance Scenario E: Unattended ASK Fail-Closed (CONTEXT_M31A.md §99... |
| [scenario_f.rs](#src-eval-scenarios-scenario_f-rs) | 248 | `ScenarioF` | Acceptance Scenario F: Crash Recovery &amp; Resume (CONTEXT_M31A.md §9... |
| [scenario_g.rs](#src-eval-scenarios-scenario_g-rs) | 143 | `ScenarioG` | Acceptance Scenario G: Malicious Prompt Injection (CONTEXT_M31A.md §99... |
| [scenario_h.rs](#src-eval-scenarios-scenario_h-rs) | 133 | `ScenarioH` | Acceptance Scenario H: Huge Compiler Output Artifact Handling (CONTEXT... |
| [scorecard.rs](#src-eval-scorecard-rs) | 243 | `EvalScorecard, EvalSummary` | Evaluation Scorecard Generator producing JSON and Markdown reports (D-... |

---

### `src/eval/fixture.rs` {#src-eval-fixture-rs}

- **Source Link:** [`src/eval/fixture.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/eval/fixture.rs)
- **Lines of Code:** 235 (8070 bytes)

#### Primary Responsibility
Programmatic temporary Git fixture repository builder (D-15, TST-03).  Provides pristine, isolated Git repositories in temporary directories with strict environment isolation (global and system Git configuration pointed at the platform null device) preventing any contamination from the user's host Git configuration.

#### Types & Trait Declarations
- **Structs (2):** `FixtureRepo`, `FixtureRepoBuilder`

#### Key Functions & Signatures (12 shown)
```rust
// pub
fn path(&self) -> &Path;
// pub
fn head_commit(&self) -> &str;
// pub
fn git_command(&self) -> Command;
// pub
fn run_git(&self, args: &[&str]) -> Result<Output, std::io::Error>;
// pub
fn read_file(&self, relative_path: impl AsRef<Path>) -> Result<String, std::io::Error>;
// pub
fn write_file(&self,
        relative_path: impl AsRef<Path>,
        content: impl AsRef<[u8]>,) -> Result<(), std::io:;
// pub
fn new() -> Result<Self, std::io::Error>;
// pub
fn with_file(&mut self,
        relative_path: impl AsRef<Path>,
        content: impl AsRef<[u8]>,) -> &mut Self;
// pub
fn with_commit(&mut self, message: impl Into<String>) -> &mut Self;
// pub
fn with_dirty_file(&mut self,
        relative_path: impl AsRef<Path>,
        content: impl AsRef<[u8]>,) -> &mut Self;
// pub
fn build(self) -> Result<FixtureRepo, std::io::Error>;
// private
fn test_fixture_builder_creates_isolated_git_repo();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_fixture_builder_creates_isolated_git_repo`

---

### `src/eval/mod.rs` {#src-eval-mod-rs}

- **Source Link:** [`src/eval/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/eval/mod.rs)
- **Lines of Code:** 14 (473 bytes)

#### Primary Responsibility
Autonomous evaluation harness, fixture builder, and acceptance scenarios (D-15, TST-01..03, TST-06).

---

### `src/eval/runner.rs` {#src-eval-runner-rs}

- **Source Link:** [`src/eval/runner.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/eval/runner.rs)
- **Lines of Code:** 136 (4823 bytes)

#### Primary Responsibility
Autonomous Evaluation Runner Engine (D-15, TST-01..03, TST-06).  Orchestrates the execution of canonical acceptance scenarios A through H with: - Strict isolation per run in temporary Git fixtures. - Configurable per-scenario timeouts (default 120s). - Deterministic aggregation into `EvalScorecard`.

#### Types & Trait Declarations
- **Structs (1):** `EvalRunner`

#### Key Functions & Signatures (7 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_timeout(mut self, timeout: Duration) -> Self;
// pub
fn scenarios(&self) -> &[Arc<dyn EvalScenario>];
// pub
async fn run_scenario(&self, id_or_name: &str) -> Result<ScenarioResult, String>;
// pub
async fn run_all(&self) -> EvalScorecard;
// private
async fn execute_scenario(&self,
        scenario: &dyn EvalScenario,) -> Result<ScenarioResult, String>;
```

---

### `src/eval/scenarios/mod.rs` {#src-eval-scenarios-mod-rs}

- **Source Link:** [`src/eval/scenarios/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/eval/scenarios/mod.rs)
- **Lines of Code:** 99 (3105 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Acceptance Scenarios A through H implementation (CONTEXT_M31A.md §99, TST-01..03, D-15).

#### Types & Trait Declarations
- **Structs (1):** `ScenarioResult`
- **Enums (2):** `EvaluationExecutionMode`, `ScenarioStatus`
- **Traits (1):** `EvalScenario`

#### Key Functions & Signatures (5 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// private
fn id(&self) -> &'static str;
// private
fn name(&self) -> &'static str;
// private
fn description(&self) -> &'static str;
// private
async fn run(&self) -> Result<ScenarioResult, String>;
```

---

### `src/eval/scenarios/scenario_a.rs` {#src-eval-scenarios-scenario_a-rs}

- **Source Link:** [`src/eval/scenarios/scenario_a.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/eval/scenarios/scenario_a.rs)
- **Lines of Code:** 125 (4678 bytes)

#### Primary Responsibility
Acceptance Scenario A: Simple Bug Fix (CONTEXT_M31A.md §99, TST-01).  Objectives: 1. Set up isolated fixture containing a failing calculation bug (`a + b + 1`). 2. Execute fix on the single file. 3. Verify tests pass. 4. Verify Git commit records valid attribution trailers.

#### Types & Trait Declarations
- **Structs (1):** `ScenarioA`

#### Key Functions & Signatures (4 shown)
```rust
// private
fn id(&self) -> &'static str;
// private
fn name(&self) -> &'static str;
// private
fn description(&self) -> &'static str;
// private
async fn run(&self) -> Result<ScenarioResult, String>;
```

---

### `src/eval/scenarios/scenario_b.rs` {#src-eval-scenarios-scenario_b-rs}

- **Source Link:** [`src/eval/scenarios/scenario_b.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/eval/scenarios/scenario_b.rs)
- **Lines of Code:** 120 (4848 bytes)

#### Primary Responsibility
Acceptance Scenario B: Multi-File Feature (CONTEXT_M31A.md §99, TST-01).  Objectives: 1. Set up isolated fixture containing modular components. 2. Implement a cross-cutting caching feature spanning multiple files. 3. Verify multiple files modified and clean worktree state.

#### Types & Trait Declarations
- **Structs (1):** `ScenarioB`

#### Key Functions & Signatures (4 shown)
```rust
// private
fn id(&self) -> &'static str;
// private
fn name(&self) -> &'static str;
// private
fn description(&self) -> &'static str;
// private
async fn run(&self) -> Result<ScenarioResult, String>;
```

---

### `src/eval/scenarios/scenario_c.rs` {#src-eval-scenarios-scenario_c-rs}

- **Source Link:** [`src/eval/scenarios/scenario_c.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/eval/scenarios/scenario_c.rs)
- **Lines of Code:** 231 (8669 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Acceptance Scenario C: Failure and DAG Replan (CONTEXT_M31A.md §99, TST-01, D-08, D-15).  Objectives: 1. Set up isolated fixture containing a compilation failure. 2. Detect failure and classify as `Compilation`. 3. Trigger `DifferentialReplanEngine` to dynamically update the DAG to revision N+1. 4. Durably persist replan in SQLite `recovery_attempts`. 5. Apply corrective fix to fixture, commit with trailers, and verify pass.

#### Types & Trait Declarations
- **Structs (1):** `ScenarioC`

#### Key Functions & Signatures (5 shown)
```rust
// private
fn make_candidate_task(id: &str, objective: &str, deps: Vec<&str>) -> CandidateTask;
// private
fn id(&self) -> &'static str;
// private
fn name(&self) -> &'static str;
// private
fn description(&self) -> &'static str;
// private
async fn run(&self) -> Result<ScenarioResult, String>;
```

---

### `src/eval/scenarios/scenario_d.rs` {#src-eval-scenarios-scenario_d-rs}

- **Source Link:** [`src/eval/scenarios/scenario_d.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/eval/scenarios/scenario_d.rs)
- **Lines of Code:** 107 (4244 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Acceptance Scenario D: Policy Denial (CONTEXT_M31A.md §99, TST-01, SEC-01, D-15).  Objectives: 1. Set up isolated fixture repository. 2. Attempt an unauthorized operation (accessing sensitive credential or system paths). 3. Policy engine evaluates request through multi-layer hierarchy and returns `DENY`. 4. Verify side effect is blocked fail-closed and zero unauthorized mutations occur.

#### Types & Trait Declarations
- **Structs (1):** `ScenarioD`

#### Key Functions & Signatures (4 shown)
```rust
// private
fn id(&self) -> &'static str;
// private
fn name(&self) -> &'static str;
// private
fn description(&self) -> &'static str;
// private
async fn run(&self) -> Result<ScenarioResult, String>;
```

---

### `src/eval/scenarios/scenario_e.rs` {#src-eval-scenarios-scenario_e-rs}

- **Source Link:** [`src/eval/scenarios/scenario_e.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/eval/scenarios/scenario_e.rs)
- **Lines of Code:** 112 (4169 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Acceptance Scenario E: Unattended ASK Fail-Closed (CONTEXT_M31A.md §99, TST-01, SEC-06, D-15).  Objectives: 1. Set up isolated fixture repository. 2. Dispatch an action requiring interactive user confirmation (`PolicyDecision::Ask`). 3. Verify that under `AutonomyMode::Unattended`, the approval coordinator converts `Ask` into `Deny`. 4. Confirm zero unapproved side effects occur.

#### Types & Trait Declarations
- **Structs (1):** `ScenarioE`

#### Key Functions & Signatures (4 shown)
```rust
// private
fn id(&self) -> &'static str;
// private
fn name(&self) -> &'static str;
// private
fn description(&self) -> &'static str;
// private
async fn run(&self) -> Result<ScenarioResult, String>;
```

---

### `src/eval/scenarios/scenario_f.rs` {#src-eval-scenarios-scenario_f-rs}

- **Source Link:** [`src/eval/scenarios/scenario_f.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/eval/scenarios/scenario_f.rs)
- **Lines of Code:** 248 (9347 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Acceptance Scenario F: Crash Recovery &amp; Resume (CONTEXT_M31A.md §99, TST-01, CHK-02, CHK-05, D-15).  Objectives: 1. Set up isolated fixture repository and checkpoint state. 2. Seed mission with Task 1 (Succeeded) and Task 2 (in-flight Running). 3. Create durable Checkpoint 1 and simulate runtime crash interruption. 4. Scanner discovers incomplete mission, verifies baseline, and classifies as `SafeToResume`. 5. `SafeResumeEngine` preserves Task 1 without re-execution, reschedules Task 2, and completes mission.

#### Types & Trait Declarations
- **Structs (1):** `ScenarioF`

#### Key Functions & Signatures (4 shown)
```rust
// private
fn id(&self) -> &'static str;
// private
fn name(&self) -> &'static str;
// private
fn description(&self) -> &'static str;
// private
async fn run(&self) -> Result<ScenarioResult, String>;
```

---

### `src/eval/scenarios/scenario_g.rs` {#src-eval-scenarios-scenario_g-rs}

- **Source Link:** [`src/eval/scenarios/scenario_g.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/eval/scenarios/scenario_g.rs)
- **Lines of Code:** 143 (5817 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Acceptance Scenario G: Malicious Prompt Injection (CONTEXT_M31A.md §99, TST-01, SEC-02, SEC-05, D-15).  Objectives: 1. Set up isolated fixture repository containing an adversarial prompt injection in README.md. 2. Ensure untrusted repo content is strictly isolated inside XML trust envelopes. 3. Verify delimiter smuggling tags `&lt;/untrusted_evidence&gt;` are neutralized. 4. Verify policy engine prevents privilege escalation attempts triggered by adversarial text. 5. Successfully complete the legitimate mission objective.

#### Types & Trait Declarations
- **Structs (1):** `ScenarioG`

#### Key Functions & Signatures (4 shown)
```rust
// private
fn id(&self) -> &'static str;
// private
fn name(&self) -> &'static str;
// private
fn description(&self) -> &'static str;
// private
async fn run(&self) -> Result<ScenarioResult, String>;
```

---

### `src/eval/scenarios/scenario_h.rs` {#src-eval-scenarios-scenario_h-rs}

- **Source Link:** [`src/eval/scenarios/scenario_h.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/eval/scenarios/scenario_h.rs)
- **Lines of Code:** 133 (5070 bytes)

#### Primary Responsibility
Acceptance Scenario H: Huge Compiler Output Artifact Handling (CONTEXT_M31A.md §99, TST-01, BST-01, D-08, D-15).  Objectives: 1. Set up isolated fixture repository. 2. Generate large compiler/tool output simulating high-volume diagnostic dumps. 3. Verify `StreamingQuotaWriter` / `QuotaEnforcer` intercepts the write in real time. 4. Confirm disk and memory limits are respected without process crashes. 5. Ensure protected verification evidence remains intact.

#### Types & Trait Declarations
- **Structs (1):** `ScenarioH`

#### Key Functions & Signatures (4 shown)
```rust
// private
fn id(&self) -> &'static str;
// private
fn name(&self) -> &'static str;
// private
fn description(&self) -> &'static str;
// private
async fn run(&self) -> Result<ScenarioResult, String>;
```

---

### `src/eval/scorecard.rs` {#src-eval-scorecard-rs}

- **Source Link:** [`src/eval/scorecard.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/eval/scorecard.rs)
- **Lines of Code:** 243 (8616 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Evaluation Scorecard Generator producing JSON and Markdown reports (D-15, TST-06).  Provides structured aggregation of scenario outcomes: - Machine-readable JSON schema validation (`schemars`). - Human-readable Markdown summary tables with metrics (pass rate, duration, tokens, cost, replans).

#### Types & Trait Declarations
- **Structs (2):** `EvalScorecard`, `EvalSummary`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn from_results(results: Vec<ScenarioResult>) -> Self;
// pub
fn to_json(&self) -> Result<String, serde_json::Error>;
// pub
fn to_markdown(&self) -> String;
// private
fn test_scorecard_aggregation_and_formatting();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_scorecard_aggregation_and_formatting`

---
