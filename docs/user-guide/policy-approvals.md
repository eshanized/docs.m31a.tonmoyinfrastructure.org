# Policy Approvals & Risk Confirmation

M31A enforces strict human-in-the-loop governance for mutating or sensitive operations.

## The 4 Policy Decisions

Every tool execution request evaluated by `src/policy/` yields one of four outcomes:

| Decision | Meaning | Runtime Behavior |
|---|---|---|
| **`Allow`** | Action complies with policy | Execution proceeds immediately |
| **`Deny`** | Action violates security rule | Execution halted with typed error; agent must replan |
| **`Ask`** | Action requires operator approval | Cockpit pauses; interactive confirmation dialog displayed |
| **`Escalate`** | Action exceeds standard risk threshold | Escalated to elevated channel or denied in unattended mode |

## Autonomy Modes & Policy Mapping

The active `AutonomyMode` controls how `Ask` decisions are resolved (`src/kernel/seams/policy.rs`):

- **`Safe`**: All workspace mutations, process executions, and git operations prompt for approval (`Ask → PauseForApproval`).
- **`Plan`**: Mutating actions are strictly prohibited (`Ask → Deny`). Read-only exploration and DAG planning only.
- **`Assisted`**: Routine edits within the workspace are allowed; destructive actions (file deletion, git reset) prompt for approval.
- **`Autonomous`**: Permitted workspace actions proceed automatically; out-of-bounds or sensitive operations escalate.
- **`Unattended`**: Headless CI mode. Any unresolved `Ask` is automatically **Denied** (`Ask → Deny`), guaranteeing that unattended runs never hang or perform unapproved actions.
