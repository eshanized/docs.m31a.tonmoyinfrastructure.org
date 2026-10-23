# Security Boundaries & Policy Enforcement

M31A enforces defense-in-depth across multiple boundary layers.

## The Layer 1 Policy Gate

Defined in `src/policy/` and `src/kernel/seams/policy.rs`:
Every tool execution creates a `PolicyEvaluationRequest` containing:
- Domain identifiers (`ExecutionRunId`, `TaskId`, `AgentId`)
- Agent role and active autonomy mode
- Canonical target file paths
- Normalized argument hashes

The policy engine evaluates rules in priority order:
1. **Immutable Kernel Security Floors** (never bypassable)
2. **System Machine Configuration** (`/etc/m31a`)
3. **User Global Configuration** (`~/.config/m31a`)
4. **Workspace Configuration** (`.m31a/config.toml`)
5. **Profile Rules** (`assets/profiles/*.toml`)

## Sensitive Path Protection

`src/kernel/sensitive_paths.rs` strictly blocks any tool from reading or mutating:
- Private SSH keys (`~/.ssh/id_*`)
- Cloud credentials (`~/.aws/credentials`, `~/.azure/`)
- Shell histories (`~/.bash_history`, `~/.zsh_history`)
- Environment files containing raw secrets (`.env`, `.env.production`)
- System password databases (`/etc/shadow`, `/etc/passwd`)

Any access attempt triggers immediate policy denial (`Deny`) and an audit security event.
