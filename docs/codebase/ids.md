# Domain Identity Types

> **Architectural Layer:** L0 Domain Identities  
> **Source Directory:** `src/ids`  
> **File Count:** 18 source files  

Strongly typed domain IDs (ExecutionRunId, TaskId, AgentId, ArtifactId, CheckId, etc.).

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [agent.rs](#src-ids-agent-rs) | 124 | `AgentId` | AgentId - strongly typed UUIDv7 identifier for agents. |
| [approval.rs](#src-ids-approval-rs) | 78 | `ApprovalRequestId` | ApprovalRequestId - strongly typed UUIDv7 identifier for interactive a... |
| [artifact.rs](#src-ids-artifact-rs) | 124 | `ArtifactId` | ArtifactId - strongly typed UUIDv7 identifier for artifacts. |
| [check.rs](#src-ids-check-rs) | 110 | `CheckId` | CheckId - strongly typed UUIDv7 identifier for verification checks. |
| [checkpoint.rs](#src-ids-checkpoint-rs) | 124 | `CheckpointId` | CheckpointId - strongly typed UUIDv7 identifier for checkpoints. |
| [event.rs](#src-ids-event-rs) | 124 | `EventId` | EventId - strongly typed UUIDv7 identifier for events. |
| [execution.rs](#src-ids-execution-rs) | 123 | `ExecutionId` | ExecutionId - strongly typed UUIDv7 identifier for worker execution in... |
| [execution_run.rs](#src-ids-execution_run-rs) | 116 | `ExecutionRunId` | ExecutionRunId - strongly typed UUIDv7 identifier for execution runs. |
| [handoff.rs](#src-ids-handoff-rs) | 123 | `HandoffId` | HandoffId - strongly typed UUIDv7 identifier for AGT-06 agent handoffs... |
| [job.rs](#src-ids-job-rs) | 127 | `JobId` | JobId - strongly typed UUIDv7 identifier for jobs. |
| [mission.rs](#src-ids-mission-rs) | 6 | `Functions/Traits` | MissionId - legacy identifier type aliased to ExecutionRunId.  Canonic... |
| [mod.rs](#src-ids-mod-rs) | 39 | `Functions/Traits` | Strongly typed UUIDv7 domain identifiers.  Per D-13, this module owns ... |
| [policy.rs](#src-ids-policy-rs) | 78 | `PolicyEvaluationId` | PolicyEvaluationId - strongly typed UUIDv7 identifier for policy evalu... |
| [session.rs](#src-ids-session-rs) | 123 | `SessionId` | SessionId - strongly typed UUIDv7 identifier for sessions. |
| [task.rs](#src-ids-task-rs) | 248 | `RequirementId, TaskId` | TaskId and RequirementId - strongly typed UUIDv7 identifiers for tasks... |
| [task_graph.rs](#src-ids-task_graph-rs) | 135 | `TaskGraphId` | TaskGraphId - strongly typed UUIDv7 identifier for task graphs (D-02). |
| [tool.rs](#src-ids-tool-rs) | 123 | `ToolCallId` | ToolCallId - strongly typed UUIDv7 identifier for tool calls. |
| [workflow.rs](#src-ids-workflow-rs) | 207 | `WorkflowRunId, WorkflowStepRunId` | Workflow domain identifiers (D-13, D-15).  Provides strongly typed UUI... |

---

### `src/ids/agent.rs` {#src-ids-agent-rs}

- **Source Link:** [`src/ids/agent.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/agent.rs)
- **Lines of Code:** 124 (2910 bytes)

#### Primary Responsibility
AgentId - strongly typed UUIDv7 identifier for agents.

#### Types & Trait Declarations
- **Structs (1):** `AgentId`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: AgentId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
// private
fn test_agent_id_construction();
// private
fn test_agent_id_hex_roundtrip();
// private
fn test_agent_id_binary_roundtrip();
// private
fn test_agent_id_display();
// private
fn test_agent_id_from_uuid();
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_agent_id_construction`, `test_agent_id_hex_roundtrip`, `test_agent_id_binary_roundtrip`, `test_agent_id_display`, `test_agent_id_from_uuid`, `test_agent_id_into_uuid`

---

### `src/ids/approval.rs` {#src-ids-approval-rs}

- **Source Link:** [`src/ids/approval.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/approval.rs)
- **Lines of Code:** 78 (1886 bytes)

#### Primary Responsibility
ApprovalRequestId - strongly typed UUIDv7 identifier for interactive approval requests.

#### Types & Trait Declarations
- **Structs (1):** `ApprovalRequestId`

#### Key Functions & Signatures (11 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// pub
fn parse(s: &str) -> Result<Self, uuid::Error>;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: ApprovalRequestId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
```

---

### `src/ids/artifact.rs` {#src-ids-artifact-rs}

- **Source Link:** [`src/ids/artifact.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/artifact.rs)
- **Lines of Code:** 124 (3000 bytes)

#### Primary Responsibility
ArtifactId - strongly typed UUIDv7 identifier for artifacts.

#### Types & Trait Declarations
- **Structs (1):** `ArtifactId`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: ArtifactId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
// private
fn test_artifact_id_construction();
// private
fn test_artifact_id_hex_roundtrip();
// private
fn test_artifact_id_binary_roundtrip();
// private
fn test_artifact_id_display();
// private
fn test_artifact_id_from_uuid();
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_artifact_id_construction`, `test_artifact_id_hex_roundtrip`, `test_artifact_id_binary_roundtrip`, `test_artifact_id_display`, `test_artifact_id_from_uuid`, `test_artifact_id_into_uuid`

---

### `src/ids/check.rs` {#src-ids-check-rs}

- **Source Link:** [`src/ids/check.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/check.rs)
- **Lines of Code:** 110 (2629 bytes)

#### Primary Responsibility
CheckId - strongly typed UUIDv7 identifier for verification checks.

#### Types & Trait Declarations
- **Structs (1):** `CheckId`

#### Key Functions & Signatures (14 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: CheckId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
// private
fn test_check_id_construction();
// private
fn test_check_id_serde_roundtrip();
// private
fn test_check_id_binary_roundtrip();
// private
fn test_check_id_display();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_check_id_construction`, `test_check_id_serde_roundtrip`, `test_check_id_binary_roundtrip`, `test_check_id_display`

---

### `src/ids/checkpoint.rs` {#src-ids-checkpoint-rs}

- **Source Link:** [`src/ids/checkpoint.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/checkpoint.rs)
- **Lines of Code:** 124 (3076 bytes)

#### Primary Responsibility
CheckpointId - strongly typed UUIDv7 identifier for checkpoints.

#### Types & Trait Declarations
- **Structs (1):** `CheckpointId`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: CheckpointId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
// private
fn test_checkpoint_id_construction();
// private
fn test_checkpoint_id_hex_roundtrip();
// private
fn test_checkpoint_id_binary_roundtrip();
// private
fn test_checkpoint_id_display();
// private
fn test_checkpoint_id_from_uuid();
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_checkpoint_id_construction`, `test_checkpoint_id_hex_roundtrip`, `test_checkpoint_id_binary_roundtrip`, `test_checkpoint_id_display`, `test_checkpoint_id_from_uuid`, `test_checkpoint_id_into_uuid`

---

### `src/ids/event.rs` {#src-ids-event-rs}

- **Source Link:** [`src/ids/event.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/event.rs)
- **Lines of Code:** 124 (2910 bytes)

#### Primary Responsibility
EventId - strongly typed UUIDv7 identifier for events.

#### Types & Trait Declarations
- **Structs (1):** `EventId`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: EventId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
// private
fn test_event_id_construction();
// private
fn test_event_id_hex_roundtrip();
// private
fn test_event_id_binary_roundtrip();
// private
fn test_event_id_display();
// private
fn test_event_id_from_uuid();
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_event_id_construction`, `test_event_id_hex_roundtrip`, `test_event_id_binary_roundtrip`, `test_event_id_display`, `test_event_id_from_uuid`, `test_event_id_into_uuid`

---

### `src/ids/execution.rs` {#src-ids-execution-rs}

- **Source Link:** [`src/ids/execution.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/execution.rs)
- **Lines of Code:** 123 (3014 bytes)

#### Primary Responsibility
ExecutionId - strongly typed UUIDv7 identifier for worker execution instances.

#### Types & Trait Declarations
- **Structs (1):** `ExecutionId`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: ExecutionId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
// private
fn test_execution_id_construction();
// private
fn test_execution_id_hex_roundtrip();
// private
fn test_execution_id_binary_roundtrip();
// private
fn test_execution_id_display();
// private
fn test_execution_id_from_uuid();
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_execution_id_construction`, `test_execution_id_hex_roundtrip`, `test_execution_id_binary_roundtrip`, `test_execution_id_display`, `test_execution_id_from_uuid`, `test_execution_id_into_uuid`

---

### `src/ids/execution_run.rs` {#src-ids-execution_run-rs}

- **Source Link:** [`src/ids/execution_run.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/execution_run.rs)
- **Lines of Code:** 116 (3099 bytes)

#### Primary Responsibility
ExecutionRunId - strongly typed UUIDv7 identifier for execution runs.

#### Types & Trait Declarations
- **Structs (1):** `ExecutionRunId`

#### Key Functions & Signatures (14 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: ExecutionRunId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
// private
fn test_execution_run_id_construction();
// private
fn test_execution_run_id_hex_roundtrip();
// private
fn test_execution_run_id_bytes_roundtrip();
// private
fn test_execution_run_id_display_and_from_str();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_execution_run_id_construction`, `test_execution_run_id_hex_roundtrip`, `test_execution_run_id_bytes_roundtrip`, `test_execution_run_id_display_and_from_str`

---

### `src/ids/handoff.rs` {#src-ids-handoff-rs}

- **Source Link:** [`src/ids/handoff.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/handoff.rs)
- **Lines of Code:** 123 (2958 bytes)

#### Primary Responsibility
HandoffId - strongly typed UUIDv7 identifier for AGT-06 agent handoffs.

#### Types & Trait Declarations
- **Structs (1):** `HandoffId`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: HandoffId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
// private
fn test_handoff_id_construction();
// private
fn test_handoff_id_hex_roundtrip();
// private
fn test_handoff_id_binary_roundtrip();
// private
fn test_handoff_id_display();
// private
fn test_handoff_id_from_uuid();
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_handoff_id_construction`, `test_handoff_id_hex_roundtrip`, `test_handoff_id_binary_roundtrip`, `test_handoff_id_display`, `test_handoff_id_from_uuid`, `test_handoff_id_into_uuid`

---

### `src/ids/job.rs` {#src-ids-job-rs}

- **Source Link:** [`src/ids/job.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/job.rs)
- **Lines of Code:** 127 (2901 bytes)

#### Primary Responsibility
JobId - strongly typed UUIDv7 identifier for jobs.

#### Types & Trait Declarations
- **Structs (1):** `JobId`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// pub
fn parse(s: &str) -> Result<Self, uuid::Error>;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: JobId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
// private
fn test_job_id_construction();
// private
fn test_job_id_hex_roundtrip();
// private
fn test_job_id_binary_roundtrip();
// private
fn test_job_id_display();
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_job_id_construction`, `test_job_id_hex_roundtrip`, `test_job_id_binary_roundtrip`, `test_job_id_display`, `test_job_id_from_uuid`, `test_job_id_into_uuid`

---

### `src/ids/mission.rs` {#src-ids-mission-rs}

- **Source Link:** [`src/ids/mission.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/mission.rs)
- **Lines of Code:** 6 (265 bytes)

#### Primary Responsibility
MissionId - legacy identifier type aliased to ExecutionRunId.  Canonical execution identity is [`ExecutionRunId`]. This alias is preserved for backwards compatibility during migration.

---

### `src/ids/mod.rs` {#src-ids-mod-rs}

- **Source Link:** [`src/ids/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/mod.rs)
- **Lines of Code:** 39 (1031 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Strongly typed UUIDv7 domain identifiers.  Per D-13, this module owns all domain ID types. Each ID is a newtype wrapper over UUIDv7 providing compile-time type safety and dual serialization

---

### `src/ids/policy.rs` {#src-ids-policy-rs}

- **Source Link:** [`src/ids/policy.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/policy.rs)
- **Lines of Code:** 78 (1883 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
PolicyEvaluationId - strongly typed UUIDv7 identifier for policy evaluations.

#### Types & Trait Declarations
- **Structs (1):** `PolicyEvaluationId`

#### Key Functions & Signatures (11 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// pub
fn parse(s: &str) -> Result<Self, uuid::Error>;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: PolicyEvaluationId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
```

---

### `src/ids/session.rs` {#src-ids-session-rs}

- **Source Link:** [`src/ids/session.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/session.rs)
- **Lines of Code:** 123 (2922 bytes)

#### Primary Responsibility
SessionId - strongly typed UUIDv7 identifier for sessions.

#### Types & Trait Declarations
- **Structs (1):** `SessionId`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: SessionId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
// private
fn test_session_id_construction();
// private
fn test_session_id_hex_roundtrip();
// private
fn test_session_id_binary_roundtrip();
// private
fn test_session_id_display();
// private
fn test_session_id_from_uuid();
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_session_id_construction`, `test_session_id_hex_roundtrip`, `test_session_id_binary_roundtrip`, `test_session_id_display`, `test_session_id_from_uuid`, `test_session_id_into_uuid`

---

### `src/ids/task.rs` {#src-ids-task-rs}

- **Source Link:** [`src/ids/task.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/task.rs)
- **Lines of Code:** 248 (6269 bytes)

#### Primary Responsibility
TaskId and RequirementId - strongly typed UUIDv7 identifiers for tasks and requirements.

#### Types & Trait Declarations
- **Structs (2):** `RequirementId`, `TaskId`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: TaskId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
```

#### Unit Verification (13 inline tests)
Tests defined within module:
`test_task_id_construction`, `test_task_id_hex_roundtrip`, `test_task_id_binary_roundtrip`, `test_task_id_display`, `test_task_id_from_uuid`, `test_task_id_into_uuid`, `test_requirement_id_construction`, `test_requirement_id_hex_roundtrip`, `test_requirement_id_binary_roundtrip`, `test_requirement_id_display`...

---

### `src/ids/task_graph.rs` {#src-ids-task_graph-rs}

- **Source Link:** [`src/ids/task_graph.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/task_graph.rs)
- **Lines of Code:** 135 (3396 bytes)

#### Primary Responsibility
TaskGraphId - strongly typed UUIDv7 identifier for task graphs (D-02).

#### Types & Trait Declarations
- **Structs (1):** `TaskGraphId`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// pub
fn from_uuid(uuid: Uuid) -> Self;
// pub
fn into_uuid(self) -> Uuid;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: TaskGraphId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
// private
fn test_task_graph_id_construction();
// private
fn test_task_graph_id_hex_roundtrip();
// private
fn test_task_graph_id_binary_roundtrip();
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_task_graph_id_construction`, `test_task_graph_id_hex_roundtrip`, `test_task_graph_id_binary_roundtrip`, `test_task_graph_id_display_and_from_str`, `test_task_graph_id_from_and_into_uuid`, `test_task_graph_id_non_interchangeable`

---

### `src/ids/tool.rs` {#src-ids-tool-rs}

- **Source Link:** [`src/ids/tool.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/tool.rs)
- **Lines of Code:** 123 (2960 bytes)

#### Primary Responsibility
ToolCallId - strongly typed UUIDv7 identifier for tool calls.

#### Types & Trait Declarations
- **Structs (1):** `ToolCallId`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: ToolCallId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
// private
fn test_tool_call_id_construction();
// private
fn test_tool_call_id_hex_roundtrip();
// private
fn test_tool_call_id_binary_roundtrip();
// private
fn test_tool_call_id_display();
// private
fn test_tool_call_id_from_uuid();
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_tool_call_id_construction`, `test_tool_call_id_hex_roundtrip`, `test_tool_call_id_binary_roundtrip`, `test_tool_call_id_display`, `test_tool_call_id_from_uuid`, `test_tool_call_id_into_uuid`

---

### `src/ids/workflow.rs` {#src-ids-workflow-rs}

- **Source Link:** [`src/ids/workflow.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/ids/workflow.rs)
- **Lines of Code:** 207 (5598 bytes)

#### Primary Responsibility
Workflow domain identifiers (D-13, D-15).  Provides strongly typed UUIDv7 identifiers for workflow runs and workflow step runs.

#### Types & Trait Declarations
- **Structs (2):** `WorkflowRunId`, `WorkflowStepRunId`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
// private
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result;
// private
fn from(uuid: Uuid) -> Self;
// private
fn from(id: WorkflowRunId) -> Uuid;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn as_uuid(&self) -> &Uuid;
// pub
fn as_bytes(&self) -> &[u8;
// pub
fn from_bytes(bytes: [u8; 16]) -> Self;
// private
fn serialize(&self, serializer: S) -> Result<S::Ok, S::Error>;
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`test_workflow_run_id_construction`, `test_workflow_run_id_serde`, `test_workflow_run_id_bytes_roundtrip`, `test_workflow_step_run_id_construction`, `test_workflow_step_run_id_serde`, `test_workflow_step_run_id_bytes_roundtrip`

---
