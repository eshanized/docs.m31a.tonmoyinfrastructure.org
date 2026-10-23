# Testing Guidelines & CI Quality Gates

How M31A enforces rigorous verification across test suites.

## Test Commands

```bash
# Run unit tests only
make test-unit

# Run full deterministic suite (both channels)
make test-all-channels

# Run clippy with -D warnings
make clippy

# Run live model tests (requires NVIDIA_API_KEY)
make test-live
```
