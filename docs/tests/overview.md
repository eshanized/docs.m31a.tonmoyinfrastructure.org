# Test Architecture Overview

M31A maintains an exhaustive 266-suite test architecture located under `tests/` and in inline module unit tests.

## Testing Strategy

Testing is structured into distinct assurance tiers:
1. **Deterministic CI Tests**: Run in continuous integration without network or credential dependencies, utilizing mock doubles and isolated temporary worktrees.
2. **Architectural Invariant Tests**: Programmatic verification of layer dependencies, single-crate rules, and authority boundaries.
3. **Security Regressions**: Targeted negative tests for policy enforcement, Landlock confinement, and sensitive paths.
4. **Partitioned Live Model Tests**: Real NVIDIA NIM API invocations, strictly marked `#[ignore]` to prevent false-green CI outcomes.
