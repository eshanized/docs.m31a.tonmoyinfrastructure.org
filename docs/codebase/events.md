# Event Bus & Envelopes

> **Architectural Layer:** L0/L8 Event Bus  
> **Source Directory:** `src/events`  
> **File Count:** 4 source files  

Broadcast channels, structured telemetry envelopes, and asynchronous event distribution.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [bus.rs](#src-events-bus-rs) | 326 | `BroadcastEventBus, EventFilter` | EventBus trait and BroadcastEventBus implementation (D-10, D-11, D-12,... |
| [envelope.rs](#src-events-envelope-rs) | 259 | `EventEnvelope, EventCategory` | Event envelope with metadata, causal tracking, and categorization (D-1... |
| [mod.rs](#src-events-mod-rs) | 11 | `Functions/Traits` | Events module - typed event contracts and sequencing (KRN-03)  Per D-1... |
| [types.rs](#src-events-types-rs) | 1501 | `TaskSummary, EventType` | Typed event vocabulary covering all domain concepts (KRN-03) |

---

### `src/events/bus.rs` {#src-events-bus-rs}

- **Source Link:** [`src/events/bus.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/events/bus.rs)
- **Lines of Code:** 326 (10080 bytes)

#### Primary Responsibility
EventBus trait and BroadcastEventBus implementation (D-10, D-11, D-12, EVT-01, EVT-03).

#### Types & Trait Declarations
- **Structs (2):** `BroadcastEventBus`, `EventFilter`
- **Traits (1):** `EventBus`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn all() -> Self;
// pub
fn with_mission(mut self, mission_id: MissionId) -> Self;
// pub
fn with_session(mut self, session_id: SessionId) -> Self;
// pub
fn with_type(mut self, event_type: impl Into<String>) -> Self;
// pub
fn with_category(mut self, category: EventCategory) -> Self;
// pub
fn from_seq(mut self, sequence: u64) -> Self;
// pub
fn to_seq(mut self, sequence: u64) -> Self;
// pub
fn matches(&self, envelope: &EventEnvelope) -> bool;
// private
async fn publish(&self, envelope: EventEnvelope) -> Result<(), M31AError>;
// private
async fn subscribe(&self, filter: EventFilter) -> EventReceiver;
// pub
fn new(capacity: usize) -> Self;
// pub
fn capacity(&self) -> usize;
// pub
fn subscriber_count(&self) -> usize;
// private
fn default() -> Self;
// private
async fn publish(&self, envelope: EventEnvelope) -> Result<(), M31AError>;
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_event_filter_builder_and_matching`, `test_broadcast_event_bus_publish_no_subscribers`, `test_broadcast_event_bus_delivery_and_filtering`, `test_broadcast_event_bus_lag_detection`

---

### `src/events/envelope.rs` {#src-events-envelope-rs}

- **Source Link:** [`src/events/envelope.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/events/envelope.rs)
- **Lines of Code:** 259 (8479 bytes)

#### Primary Responsibility
Event envelope with metadata, causal tracking, and categorization (D-13, EVT-01, EVT-02).

#### Types & Trait Declarations
- **Structs (1):** `EventEnvelope`
- **Enums (1):** `EventCategory`

#### Key Functions & Signatures (11 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn from_str(s: &str) -> Result<Self, Self::Err>;
// pub
fn new(sequence: u64,
        mission_id: Option<MissionId>,
        session_id: Option<SessionId>,
        actor: Strin;
// pub
fn new_for_run(sequence: u64,
        run_id: Option<ExecutionRunId>,
        session_id: Option<SessionId>,
        act;
// pub
fn with_schema_version(sequence: u64,
        mission_id: Option<MissionId>,
        session_id: Option<SessionId>,
    ;
// pub
fn with_causation(mut self,
        correlation_id: Option<String>,
        causation_id: Option<EventId>,) -> Self;
// pub
fn with_category(mut self, category: EventCategory) -> Self;
// private
fn test_event_envelope_new();
// private
fn test_event_envelope_causation_and_category();
// private
fn test_event_envelope_serde_roundtrip();
// private
fn test_event_envelope_generates_unique_ids();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_event_envelope_new`, `test_event_envelope_causation_and_category`, `test_event_envelope_serde_roundtrip`, `test_event_envelope_generates_unique_ids`

---

### `src/events/mod.rs` {#src-events-mod-rs}

- **Source Link:** [`src/events/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/events/mod.rs)
- **Lines of Code:** 11 (337 bytes)

#### Primary Responsibility
Events module - typed event contracts and sequencing (KRN-03)  Per D-16, events/ owns typed event contracts and event sequencing.

---

### `src/events/types.rs` {#src-events-types-rs}

- **Source Link:** [`src/events/types.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/events/types.rs)
- **Lines of Code:** 1501 (53182 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Typed event vocabulary covering all domain concepts (KRN-03)

#### Types & Trait Declarations
- **Structs (1):** `TaskSummary`
- **Enums (1):** `EventType`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn name(&self) -> &'static str;
// private
fn test_event_type_variants_count();
// private
fn test_event_type_serde_roundtrip();
// private
fn test_event_type_name();
// private
fn test_all_domains_covered();
// private
fn test_controller_lifecycle_events_serde_roundtrip();
// private
fn test_scheduler_events_serde_roundtrip();
// private
fn test_engineering_memory_events_serde_roundtrip();
```

#### Unit Verification (7 inline tests)
Tests defined within module:
`test_event_type_variants_count`, `test_event_type_serde_roundtrip`, `test_event_type_name`, `test_all_domains_covered`, `test_controller_lifecycle_events_serde_roundtrip`, `test_scheduler_events_serde_roundtrip`, `test_engineering_memory_events_serde_roundtrip`

---
