# Subsystem: Policy & Approval Coordination

Enforces security authorization before every tool call (`src/policy/`).

## Approval Coordination

`ApprovalCoordinator` coordinates interactive human confirmation:
- Creates `ApprovalRequest` with unique ID and risk level.
- Emits approval event to cockpit.
- Suspends tool execution until operator grants (`Approve`) or denies (`Deny`) the request.
