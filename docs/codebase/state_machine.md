# Domain State Machines

> **Architectural Layer:** L8 State Machine  
> **Source Directory:** `src/state_machine`  
> **File Count:** 9 source files  

Strict state transition matrices for missions, tasks, agents, and autonomy modes.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [agent.rs](#src-state_machine-agent-rs) | 452 | `AgentRole, AgentEvent, AgentState` | Agent lifecycle state machine |
| [autonomy.rs](#src-state_machine-autonomy-rs) | 46 | `AutonomyMode` | Five canonical runtime autonomy modes (AUT-01, AUT-02, AUT-03, D-13, S... |
| [change_set.rs](#src-state_machine-change_set-rs) | 274 | `ChangeSetEvent, ChangeSetState` | Change set state machine and validated lifecycle transitions (KRN-02).... |
| [error.rs](#src-state_machine-error-rs) | 53 | `TransitionError` | Transition error types for state machines |
| [execution_run.rs](#src-state_machine-execution_run-rs) | 416 | `ExecutionRunEvent, ExecutionRunState` | ExecutionRun lifecycle state machine  Provides validated transitions f... |
| [lifecycle.rs](#src-state_machine-lifecycle-rs) | 451 | `LifecycleEvent, LifecycleStage` | Human-governed pre-execution lifecycle state machine.  Enforces: "The ... |
| [mission.rs](#src-state_machine-mission-rs) | 182 | `Functions/Traits` | Mission lifecycle transitions using the canonical execution lifecycle ... |
| [mod.rs](#src-state_machine-mod-rs) | 23 | `Functions/Traits` | State machine module - lifecycle enums and validated transitions (KRN-... |
| [task.rs](#src-state_machine-task-rs) | 287 | `TaskEvent, TaskState` | Task lifecycle state machine |

---

### `src/state_machine/agent.rs` {#src-state_machine-agent-rs}

- **Source Link:** [`src/state_machine/agent.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state_machine/agent.rs)
- **Lines of Code:** 452 (16018 bytes)

#### Primary Responsibility
Agent lifecycle state machine

#### Types & Trait Declarations
- **Structs (1):** `AgentRole`
- **Enums (2):** `AgentEvent`, `AgentState`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn new(id: impl Into<String>) -> Self;
// pub
fn as_str(&self) -> &str;
// pub
fn is_well_formed(&self) -> bool;
// pub
fn planner() -> Self;
// pub
fn researcher() -> Self;
// pub
fn architect() -> Self;
// pub
fn implementer() -> Self;
// pub
fn reviewer() -> Self;
// pub
fn verifier() -> Self;
// pub
fn diagnostician() -> Self;
// pub
fn integrator() -> Self;
// pub
fn discovery_analyst() -> Self;
// pub
fn stack_researcher() -> Self;
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_valid_transitions`, `test_terminal_states_reject_transitions`, `test_invalid_transitions_rejected`, `test_is_terminal`, `test_agent_role_serialization_and_display`

---

### `src/state_machine/autonomy.rs` {#src-state_machine-autonomy-rs}

- **Source Link:** [`src/state_machine/autonomy.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state_machine/autonomy.rs)
- **Lines of Code:** 46 (1468 bytes)

#### Primary Responsibility
Five canonical runtime autonomy modes (AUT-01, AUT-02, AUT-03, D-13, SEC-06).

#### Types & Trait Declarations
- **Enums (1):** `AutonomyMode`

#### Key Functions & Signatures (2 shown)
```rust
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
```

---

### `src/state_machine/change_set.rs` {#src-state_machine-change_set-rs}

- **Source Link:** [`src/state_machine/change_set.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state_machine/change_set.rs)
- **Lines of Code:** 274 (10651 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Change set state machine and validated lifecycle transitions (KRN-02).  Enforces: The model proposes. The runtime decides. State transitions govern the lifecycle of a code modification change proposal: Proposed -&gt; Validating -&gt; Authorized -&gt; Applying -&gt; Applied -&gt; Observing -&gt; Verifying -&gt; Accepted. Terminal states: Accepted, Rejected, Conflicted, RolledBack, Failed.

#### Types & Trait Declarations
- **Enums (2):** `ChangeSetEvent`, `ChangeSetState`

#### Key Functions & Signatures (12 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// pub
fn is_terminal(&self) -> bool;
// pub
fn is_active(&self) -> bool;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn transition_change_set(current: ChangeSetState,
    event: ChangeSetEvent,) -> Result<ChangeSetState, TransitionError>;
// private
fn test_happy_path_lifecycle();
// private
fn test_conflict_from_validating();
// private
fn test_rollback_from_applying();
// private
fn test_rollback_from_verifying();
// private
fn test_terminal_state_rejects_transitions();
// private
fn test_invalid_forward_transition_fails();
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_happy_path_lifecycle`, `test_conflict_from_validating`, `test_rollback_from_applying`, `test_rollback_from_verifying`, `test_terminal_state_rejects_transitions`, `test_invalid_forward_transition_fails`

---

### `src/state_machine/error.rs` {#src-state_machine-error-rs}

- **Source Link:** [`src/state_machine/error.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state_machine/error.rs)
- **Lines of Code:** 53 (1429 bytes)

#### Primary Responsibility
Transition error types for state machines

#### Types & Trait Declarations
- **Enums (1):** `TransitionError`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn invalid_transition(from: impl Into<String>, to: impl Into<String>) -> Self;
// pub
fn terminal_state(state: impl Into<String>) -> Self;
// private
fn test_invalid_transition_display();
// private
fn test_terminal_state_display();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_invalid_transition_display`, `test_terminal_state_display`

---

### `src/state_machine/execution_run.rs` {#src-state_machine-execution_run-rs}

- **Source Link:** [`src/state_machine/execution_run.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state_machine/execution_run.rs)
- **Lines of Code:** 416 (16101 bytes)

#### Primary Responsibility
ExecutionRun lifecycle state machine  Provides validated transitions for the canonical top-level execution lifecycle.

#### Types & Trait Declarations
- **Enums (2):** `ExecutionRunEvent`, `ExecutionRunState`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn is_terminal(&self) -> bool;
// pub
fn event_target_state(event: ExecutionRunEvent) -> Option<ExecutionRunState>;
// pub
fn target_state_to_event(current: Self,
        target: Self,) -> Result<ExecutionRunEvent, TransitionError>;
// pub
fn validate_transition(current: Self, target: Self) -> Result<Self, TransitionError>;
// pub
fn transition_execution_run(current: ExecutionRunState,
    event: ExecutionRunEvent,) -> Result<ExecutionRunState, Tran;
// pub(crate)
fn transition_execution_run_with_shortcuts(current: ExecutionRunState,
    event: ExecutionRunEvent,
    allow_direct_ex;
// private
fn test_valid_forward_transitions();
// private
fn test_direct_execution_transitions();
// private
fn test_pause_resume();
// private
fn test_block_unblock();
// private
fn test_fail_from_any_state();
// private
fn test_cancel_from_any_state();
// private
fn test_terminal_states_reject_transitions();
```

#### Unit Verification (8 inline tests)
Tests defined within module:
`test_valid_forward_transitions`, `test_direct_execution_transitions`, `test_pause_resume`, `test_block_unblock`, `test_fail_from_any_state`, `test_cancel_from_any_state`, `test_terminal_states_reject_transitions`, `test_from_str_and_display`

---

### `src/state_machine/lifecycle.rs` {#src-state_machine-lifecycle-rs}

- **Source Link:** [`src/state_machine/lifecycle.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state_machine/lifecycle.rs)
- **Lines of Code:** 451 (18561 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Human-governed pre-execution lifecycle state machine.  Enforces: "The model proposes. The runtime decides."  Ensures that between raw user intent and autonomous workspace execution, there are mandatory, typed human-governed gates: 1. Dynamic discovery &amp; question resolution 2. Plan review, editing, revision, and acceptance 3. Task review, editing, addition, removal, and acceptance 4. Explicit execution authorization  Terminal outcomes: Cancelled, Rejected, Blocked, Failed, Completed.

#### Types & Trait Declarations
- **Enums (2):** `LifecycleEvent`, `LifecycleStage`

#### Key Functions & Signatures (10 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn is_terminal(&self) -> bool;
// pub
fn is_governance_gate(&self) -> bool;
// pub
fn transition_lifecycle(current: LifecycleStage,
    event: LifecycleEvent,) -> Result<LifecycleStage, TransitionError>;
// private
fn test_happy_path_governance_progression();
// private
fn test_cannot_bypass_execution_authorization();
// private
fn test_upstream_invalidation_cascades();
// private
fn test_rejection_outcomes();
// private
fn test_terminal_states_reject_all();
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_happy_path_governance_progression`, `test_cannot_bypass_execution_authorization`, `test_upstream_invalidation_cascades`, `test_rejection_outcomes`, `test_terminal_states_reject_all`

---

### `src/state_machine/mission.rs` {#src-state_machine-mission-rs}

- **Source Link:** [`src/state_machine/mission.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state_machine/mission.rs)
- **Lines of Code:** 182 (6380 bytes)

#### Primary Responsibility
Mission lifecycle transitions using the canonical execution lifecycle state model.  Mission retains strict staged progression. Direct-execution shortcuts are enabled only for ExecutionRun, while the shared state/event definitions live in the canonical execution_run module.

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn transition_mission(current: MissionState,
    event: MissionEvent,) -> Result<MissionState, crate::state_machine::err;
// private
fn test_valid_forward_transitions();
// private
fn test_pause_resume();
// private
fn test_block_unblock();
// private
fn test_fail_from_non_terminal();
// private
fn test_cancel_from_non_terminal();
// private
fn test_terminal_states_reject_transitions();
// private
fn test_invalid_transitions_rejected();
// private
fn mission_rejects_execution_only_shortcuts();
// private
fn test_is_terminal();
```

#### Unit Verification (9 inline tests)
Tests defined within module:
`test_valid_forward_transitions`, `test_pause_resume`, `test_block_unblock`, `test_fail_from_non_terminal`, `test_cancel_from_non_terminal`, `test_terminal_states_reject_transitions`, `test_invalid_transitions_rejected`, `mission_rejects_execution_only_shortcuts`, `test_is_terminal`

---

### `src/state_machine/mod.rs` {#src-state_machine-mod-rs}

- **Source Link:** [`src/state_machine/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state_machine/mod.rs)
- **Lines of Code:** 23 (1007 bytes)

#### Primary Responsibility
State machine module - lifecycle enums and validated transitions (KRN-02)  Per D-15, state_machine/ owns lifecycle enums and validated transitions. Per D-08, enum-based state with transition functions returning Result&lt;NewState, TransitionError&gt;. Per D-10, invalid transitions return Result::Err(TransitionError) — caller handles.

---

### `src/state_machine/task.rs` {#src-state_machine-task-rs}

- **Source Link:** [`src/state_machine/task.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/state_machine/task.rs)
- **Lines of Code:** 287 (9629 bytes)

#### Primary Responsibility
Task lifecycle state machine

#### Types & Trait Declarations
- **Enums (2):** `TaskEvent`, `TaskState`

#### Key Functions & Signatures (9 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn is_terminal(&self) -> bool;
// pub
fn transition_task(current: TaskState, event: TaskEvent) -> Result<TaskState, TransitionError>;
// private
fn test_valid_transitions();
// private
fn test_universal_cancel_from_non_terminal_states();
// private
fn test_terminal_states_reject_transitions();
// private
fn test_invalid_transitions_rejected();
// private
fn test_is_terminal();
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_valid_transitions`, `test_universal_cancel_from_non_terminal_states`, `test_terminal_states_reject_transitions`, `test_invalid_transitions_rejected`, `test_is_terminal`

---
