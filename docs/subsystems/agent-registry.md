# Subsystem: Agent Pool & Registry

M31A defines 18 built-in agent roles managed by `RoleRegistry` (`src/agent/registry.rs`).

## Built-In Roles Catalog

### Core Roles
- **`planner`**: Decomposes objectives into DAG tasks.
- **`researcher`**: Explores codebase, documentation, and external patterns.
- **`implementer`**: Performs code mutations and edits.
- **`verifier`**: Runs test suites and evaluates evidence.
- **`reviewer`**: Audits diffs for security, style, and correctness.
- **`diagnostician`**: Analyzes compiler errors and test failures.
- **`discovery_analyst`**: Analyzes greenfield/brownfield workspace context.
- **`architect`**: Formulates architecture, ADRs, and system boundaries.
- **`integrator`**: Reconciles merge conflicts and cross-module boundaries.

### Specialized Research Roles
- `architecture_researcher`, `stack_researcher`, `features_researcher`, `pitfalls_researcher`, `security_researcher`, `deployment_researcher`.

### Governance Roles
- **`synthesizer`**: Merges multi-agent research into unified specifications.
- **`auditor`**: Enforces architectural invariants and dead-code prevention.
- **`release_certifier`**: Evaluates the 20-point release evidence matrix.
