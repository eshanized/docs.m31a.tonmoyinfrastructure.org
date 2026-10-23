# System Requirements & Platform Support

M31A is engineered for cross-platform portability across modern 64-bit operating systems.

## Hardware Requirements

| Resource | Minimum | Recommended | Notes |
|---|---|---|---|
| **CPU** | 2 Cores (x86_64 or ARM64) | 4+ Cores | Required for parallel DAG task execution and local compiler checks |
| **RAM** | 2 GB Available | 4 GB+ Available | Memory footprint during SQLite indexing and AST analysis |
| **Storage** | 200 MB | 2 GB Available | Workspace databases, checkpoints, and artifact ledger staging |
| **Network** | Broadband Internet | Low-latency Broadband | Outbound HTTPS (TCP port 443) to NVIDIA NIM endpoint |

## Operating System Matrix

M31A implementation platform coverage (verified in `src/platform/` and `.github/workflows/`):

| Operating System | Architecture | Support Level | Sandbox Mechanism | Status |
|---|---|:---:|---|:---:|
| **Linux** (Ubuntu 22.04+, Debian 12+, RHEL 9+, Arch) | `x86_64`, `aarch64` | **Tier 1 (Primary)** | Landlock, seccomp, PID namespaces, `/proc` PID validation | Full Production Support |
| **macOS** (12.0 Monterey, 13+, 14 Sonoma, 15 Sequoia) | `aarch64` (Apple Silicon), `x86_64` | **Tier 1** | `sandbox-exec` profile restrictions, posix_spawn | Full Production Support |
| **Windows** (Windows 10, Windows 11, Server 2022) | `x86_64`, `arm64` | **Tier 2** | Windows Job Objects, restricted token privileges | Supported (CLI/TUI) |

## Toolchain & Runtime Prerequisites

When building from source:
- **Rust Toolchain**: Rust 1.85.0 or later (Stable). Verified via `rust-toolchain.toml`.
- **Git**: Version 2.30.0 or later. Required for worktree isolation, patch application, and trailer attribution.
- **SQLite**: Bundled via SQLx with modern JSON and UUID v7 extensions. No external database server required.
- **Network Egress**: Direct HTTPS connection to `https://integrate.api.nvidia.com/v1`. Proxies supported via `HTTPS_PROXY`.
