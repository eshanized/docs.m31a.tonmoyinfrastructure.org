# Test Categories & Execution Contracts

Detailed breakdown of test categories and how to run them.

## 1. Deterministic CI Test Suite
Covers unit, integration, and state machine tests.

```bash
cargo test
```

## 2. Architectural Invariant Tests
Verified in `tests/architecture_*.rs`:
- `architecture_invariants.rs`: Enforces downward dependency discipline.
- `architecture_credential_boundary.rs`: Enforces secret masking.
- `architecture_live_test_partition.rs`: Proves all live tests are partitioned.

## 3. Live Model Tests
Partitioned live model tests require an active `NVIDIA_API_KEY`:

```bash
export NVIDIA_API_KEY="nvapi-..."
make test-live
```
