# Event Bus & Structured Telemetry

Real-time communication and observability across the runtime.

## Broadcast Event Bus

`src/events/bus.rs` implements `BroadcastEventBus` using bounded `tokio::sync::broadcast` channels (default capacity: 2,048 items).
Events are wrapped in `EventEnvelope`:
- `event_id`: UUID v7
- `run_id`: Execution run correlation ID
- `timestamp`: UTC ISO-8601
- `payload`: Typed `EventType`

## Distributed Tracing & Spans

`src/telemetry/` records execution spans, token usage metrics, and latency. Telemetry is persisted in SQLite and can be exported as JSON or NDJSON via:

```bash
m31a telemetry inspect <EXECUTION_ID> --spans --metrics
```
