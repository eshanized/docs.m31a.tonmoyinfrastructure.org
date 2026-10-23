# Release Model & Verification Evidence

M31A uses an automated, evidence-backed release engineering pipeline with strict quality gates enforced prior to artifact publishing.

## Compile-Time Deployment Channels

Unlike tools that rely on runtime environment variables, M31A enforces deployment identity at **compile time** using mutually exclusive Cargo features (`src/deployment/channel.rs`):

```
                        ┌──────────────────────────────────────────────┐
                        │              M31A Source Code                │
                        └──────────────────────┬───────────────────────┘
                                               │
                   ┌───────────────────────────┴───────────────────────────┐
                   ▼                                                       ▼
        [Default Features]                                      [--features development]
                   │                                                       │
                   ▼                                                       ▼
      ┌─────────────────────────┐                             ┌─────────────────────────┐
      │   Production Channel    │                             │   Development Channel   │
      │   Binary: `m31a`        │                             │   Binary: `m31a-dev`    │
      │   State: `~/.local/.../m31a` │                        │   State: `~/.local/.../m31a-dev` │
      │   Update Feed: `stable` │                             │   Update Feed: `development`│
      └─────────────────────────┘                             └─────────────────────────┘
```

> **Compilation Invariant:** Enabling both `production` and `development` features simultaneously triggers a compile-time error (`compile_error!`). They can never be combined.

## The 20-Point Release Evidence Matrix

Before an official release artifact is certified and promoted, the `release_certifier` agent and automated CI scripts (`scripts/rc-evidence.sh`, `scripts/release-check.sh`) verify 20 deterministic criteria:

1. **Clean Git State**: No uncommitted changes in release worktree.
2. **Channel Identity**: Target binary compiled with verified channel.
3. **Rust Toolchain Minimum**: Compiler meets `rust-version = 1.85`.
4. **Format Verification**: `cargo fmt --check` passes cleanly.
5. **Clippy Zero-Warning**: `cargo clippy --all-targets -- -D warnings` exits 0.
6. **Deterministic Unit Suite**: All unit tests pass in isolation.
7. **Integration Verification**: 220+ integration test suites execute successfully.
8. **Live Test Isolation**: Live model tests remain properly partitioned (`#[ignore]`).
9. **Single-Crate Integrity**: No Cargo workspace violations.
10. **Downward Dependency Check**: Layer dependencies strictly downward.
11. **Documentation Contract**: All 11 canonical documentation files match source reality.
12. **Migration Consistency**: All SQL migrations (001-032) apply forward and idempotently.
13. **Policy Gate Integrity**: Non-bypassable policy tests pass 100%.
14. **Process Tree Confinement**: PID tracking and signal escalation verified on host OS.
15. **Crash Recovery Seal**: Unfinished scans and spool sealing verified.
16. **NVIDIA Endpoint Validation**: Only canonical NVIDIA NIM endpoints accepted.
17. **Masked Secret Verification**: Multibyte UTF-8 secret masking passes.
18. **Artifact Manifest Integrity**: SHA-256 checksums match built release archives.
19. **Rollback Recovery**: Binary replacement rollback mechanism operational.
20. **TUI Render Invariant**: First-frame rendering precedes async runtime assembly.
