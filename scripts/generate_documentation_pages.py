#!/usr/bin/env python3
"""
Generates the authoritative, production-quality documentation pages for M31A.
Covers Intro, Getting Started, User Manual, Architecture, Subsystems, Tests,
Reference, Developer, Security, Deployment, and Troubleshooting.
"""

import os
from pathlib import Path

DOCS_DIR = Path("/home/snigdha/Desktop/docs.m31a.tonmoyinfrastructure.org/docs").resolve()

PAGES = {}

# ─────────────────────────────────────────────────────────────────────────────
# 1. Product Introduction
# ─────────────────────────────────────────────────────────────────────────────

PAGES["intro/overview.md"] = """# M31 Autonomous (M31A) Overview

**M31 Autonomous (M31A)** is a single-crate, Rust-native autonomous software engineering runtime engineered for deterministic execution, non-bypassable security policy gates, verifiable code mutation, and isolated Git attribution.

> **Foundational Axiom:** *"The model proposes. The runtime decides."*

Unlike conventional LLM wrappers or generative coding assistants that allow an AI model to directly execute shell commands, overwrite files, or mark tasks complete, M31A treats language models strictly as untrusted reasoning components. All model outputs are classified as *proposals*. The authoritative Rust runtime independently validates proposals, enforces security policies, schedules work via a DAG, supervises processes in sandboxes, and demands cryptographic evidence before verifying completion.

```mermaid
flowchart TD
    User([Developer / CI Engine]) -->|CLI / TUI Prompt| Runtime[M31A Core Runtime]
    Runtime -->|Context Envelope| Model[NVIDIA NIM Provider]
    Model -->|Structured Proposal| Runtime
    Runtime -->|Policy Evaluation Request| Gate{Policy Gate}
    Gate -->|Deny / Ask| Approval[Interactive Cockpit / Escalation]
    Gate -->|Allow| Capabilities[Sandbox / Tool Execution]
    Capabilities -->|File / Process Side Effects| Evidence[Durable Artifact Ledger]
    Evidence -->|7-Tier Verification| Verifier{Nyquist Gate}
    Verifier -->|Passed with Evidence| SQLite[(Authoritative SQLite Persistence)]
    Verifier -->|Failed / Drift| Recovery[Crash Recovery / Replanner]
```

## Core Distinctions

1. **Rust-Native Performance & Reliability**: Pure Rust core with zero Python, Node.js, or GPU runtime dependencies. Single static binary deployment.
2. **ExecutionRun Authority**: Replaced legacy mission entities with canonical `ExecutionRun` records (database migrations 030-032). All session, task, event, and artifact states derive from authoritative execution runs.
3. **NVIDIA NIM Production Exclusivity**: Production reasoning is powered exclusively via NVIDIA NIM (`integrate.api.nvidia.com/v1`), supporting advanced models such as `meta/llama-3.2-11b-vision-instruct`. Legacy providers (OpenAI, Anthropic, Gemini, Ollama) are deterministically rejected with clear diagnostics.
4. **Non-Bypassable Layer 1 Policy Gate**: Every tool execution passes through the security gate. Decisions are classified into 4 deterministic states: `Allow`, `Deny`, `Ask`, and `Escalate`.
5. **7-Tier Gated Verification Hierarchy**: Multi-stage fail-fast verification (Deterministic → Compiler → Tests → Static Analysis → Invariants → Reviewer → Diagnostician). No task can complete on model self-report.
6. **Compile-Time Channel Isolation**: Mutually exclusive `production` (default `m31a`) and `development` (`m31a-dev`) channels prevent cross-contamination of persistent state.

## Target Audiences

- **Developers**: Automate repository maintenance, large-scale refactoring, unit test generation, and pull request workflows.
- **Architects & Researchers**: Explore high-assurance agent architectures, topological DAG scheduling, and formal verification gating.
- **Security Engineers**: Inspect audit ledgers, process sandboxing, credential boundaries, and prompt-injection defense walls.
- **DevOps & Release Engineers**: Run headless deterministic execution runs in CI pipelines with exit codes 0 through 7.
"""

PAGES["intro/design-principles.md"] = """# Core Design Principles & Runtime Authority

M31A was constructed from the ground up under 10 non-negotiable architectural invariants detailed in `AGENTS.md` and enforced by automated tests in `tests/architecture_invariants.rs`.

## The 10 Architectural Invariants

### 1. Single Crate Architecture
M31A is intentionally built as a single Rust crate (`m31a`). It does not use a Cargo workspace. Domain boundaries are enforced using Rust module visibility (`pub(crate)`) and clear architectural layering (L0 through L9).

### 2. Pure Rust Core
The core runtime, CLI, TUI, scheduler, policy engine, and tests require only the Rust toolchain (Rust 1.85+, edition 2024) and platform C libraries (SQLite via SQLx). No external runtime interpreters (Python, Node.js) or local GPU drivers are required.

### 3. Policy Supremacy
Every external side effect—filesystem modifications, command executions, git worktrees, network egress—**must** pass through the Layer 1 Policy Gate. There are no bypasses for "internal" tools, test harnesses, or system agents.

### 4. TUI is a Pure Projection
The Ratatui terminal user interface (cockpit) is strictly a read-only projection over SQLite database state and asynchronous tokio broadcast event streams. The TUI never maintains authoritative execution state. If the terminal crashes or is resized, runtime execution is completely unaffected.

### 5. Never Fake Success
M31A rejects mock returns, TODO-only implementations, or silent fallbacks. Unimplemented or blocked execution paths return explicit, strongly typed errors. A present-but-invalid configuration is a fatal startup exit (Exit Code 2), never a silent fallback to defaults.

### 6. Completion Requires Evidence
No mission, task, or execution run can transition to `Succeeded` based on an LLM claiming "I have completed the task." Completion requires deterministic execution evidence: passing compiler checks, passing test suites, and cryptographic SHA-256 artifact verification against pre-execution repository baselines.

### 7. Bounded Retries & Execution
Every loop, retry counter, background process, and memory allocation is strictly bounded. The decommissioned token budget system has been replaced by concrete runtime limits:
- Maximum steps per agent role (default: 20-30 steps)
- Step stall timeouts (default: 60-90 seconds)
- Task wall-clock timeouts (default: 300-900 seconds)
- Action failure thresholds (default: 3 consecutive failures trigger diagnostic recovery)
- Global and per-mission job concurrency caps

### 8. Real, Non-Blocking Cancellation
All asynchronous operations and supervised processes support instantaneous cancellation via Tokio `CancellationToken` and POSIX signal escalation (SIGINT → SIGTERM → SIGKILL).

### 9. External Data is Untrusted
All data entering the runtime from the outside world—prompt inputs, repository contents, model responses, web search results—is treated as untrusted. Payloads pass through strict sanitization, UTF-8 normalization, and trust boundaries before context compilation.

### 10. Downward Dependency Discipline
Architectural layers (L0 Kernel through L9 CLI/TUI) depend downward only:
- Lower layers (e.g. L1 Security) may **never** import or depend on higher layers (e.g. L8 Autonomy, L9 CLI).
- Upward communication occurs exclusively via asynchronous event publishing or typed trait interfaces.
"""

PAGES["intro/system-requirements.md"] = """# System Requirements & Platform Support

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
"""

PAGES["intro/release-model.md"] = """# Release Model & Verification Evidence

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
"""

PAGES["intro/glossary.md"] = """# Glossary & Core Concepts

Authoritative definitions of core terminology used across the M31A platform.

### Agent Role
A specialized LLM prompt and policy profile with constrained capabilities. Examples: `planner`, `implementer`, `verifier`, `reviewer`, `diagnostician`, `architect`.

### Autonomy Mode
The operational posture of the runtime controlling approval requirements. M31A implements 5 modes: `Safe`, `Plan`, `Assisted`, `Autonomous`, and `Unattended`.

### Capability
A typed system interface (e.g. `fs.read`, `process.exec`, `git.commit`) that tools must acquire to perform work.

### Checkpoint
A durable, content-addressed snapshot of execution state, workspace files, and artifact ledger entries committed atomically to SQLite.

### ExecutionRun
The canonical root orchestrator entity representing an autonomous task execution from intake to completion (consolidated in database migrations 030-032).

### FsArtifactStore
Content-addressed filesystem storage located in platform directories (`~/.local/share/m31a/artifacts`) storing generated diffs, test logs, and review summaries.

### Nyquist Gate
The evidence-backed completion gate enforcing that no task or execution run may transition to `Succeeded` without deterministic verification evidence.

### Policy Gate
The Layer 1 security evaluator intercepting all tool calls and classifying them into `Allow`, `Deny`, `Ask`, or `Escalate`.

### Ratatui Cockpit
The high-performance interactive terminal user interface projecting live execution state.

### Worktree Isolation
A dedicated Git worktree branch (`m31a/run/...`) created for an execution run to ensure experiments never corrupt the operator's working branch.
"""

# ─────────────────────────────────────────────────────────────────────────────
# 2. Installation & Quickstart
# ─────────────────────────────────────────────────────────────────────────────

PAGES["getting-started/quickstart.md"] = """# 5-Minute Quickstart

Get up and running with M31 Autonomous in less than 5 minutes.

## Prerequisites

1. An **NVIDIA NIM API Key** (obtainable from [build.nvidia.com](https://build.nvidia.com)).
2. An initialized Git repository with code to inspect or modify.

## Step 1: Install M31A

Download and install the standalone binary using our official installation script:

```bash
# On Linux & macOS
curl -fsSL https://docs.m31a.tonmoyinfrastructure.org/install.sh | bash

# On Windows (PowerShell)
irm https://docs.m31a.tonmoyinfrastructure.org/install.ps1 | iex
```

Verify your installation:

```bash
m31a --version
```

Expected output:
```text
m31a 0.1.12 (production, x86_64-unknown-linux-gnu, git:3eddbfd)
```

## Step 2: Configure Your NVIDIA NIM Key

Set your API key in your shell environment:

```bash
export NVIDIA_API_KEY="nvapi-..."
```

Or configure it persistently in M31A's user configuration:

```bash
m31a config set provider.nvidia_nim.api_key "nvapi-..."
```

## Step 3: Run Environmental Doctor

Ensure your environment meets all requirements:

```bash
m31a doctor
```

The doctor probe will verify Git availability, directory permissions, sandbox support, and NVIDIA NIM endpoint connectivity.

## Step 4: Launch Your First Autonomous Run

Navigate to any Git repository and execute an autonomous prompt:

```bash
cd /path/to/your/project

m31a run "Inspect src/main.rs, add comprehensive error logging, and run tests"
```

## Step 5: Explore the Interactive Cockpit

To launch the full interactive Ratatui cockpit:

```bash
m31a
```

Use the interactive cockpit to chat with the planner, approve policy actions, view real-time DAG progression, and inspect diffs.
"""

PAGES["getting-started/installation.md"] = """# Installation Methods

M31A can be installed via precompiled standalone binaries, package managers, or built from source.

## Method 1: Official Shell Installer (Recommended)

Our verified installer detects your OS architecture, downloads the release binary, verifies SHA-256 checksums, and places `m31a` in your PATH (`~/.local/bin` on Linux/macOS):

```bash
# Linux / macOS
curl -fsSL https://docs.m31a.tonmoyinfrastructure.org/install.sh | bash
```

To install the **development channel** binary (`m31a-dev`):

```bash
curl -fsSL https://docs.m31a.tonmoyinfrastructure.org/install.sh | bash -s -- --channel development
```

### Windows (PowerShell)

```powershell
irm https://docs.m31a.tonmoyinfrastructure.org/install.ps1 | iex
```

## Method 2: Precompiled Binary Releases

Download archive bundles directly from the GitHub Releases page:
[https://github.com/eshanized/M31A/releases](https://github.com/eshanized/M31A/releases)

Available target triples:
- `x86_64-unknown-linux-gnu`
- `aarch64-unknown-linux-gnu`
- `aarch64-apple-darwin` (Apple Silicon M-series)
- `x86_64-apple-darwin` (Intel Mac)
- `x86_64-pc-windows-msvc`

### Checksum Verification

Always verify the SHA-256 hash against `SHA256SUMS.txt`:

```bash
sha256sum -c SHA256SUMS.txt --ignore-missing
```

## Method 3: Building from Source (Cargo)

Prerequisites: Rust 1.85.0+ installed via `rustup`.

```bash
# Clone the repository
git clone https://github.com/eshanized/M31A.git
cd M31A

# Build production binary (release mode)
cargo build --release

# The compiled binary is located at target/release/m31a
cp target/release/m31a ~/.local/bin/
```

To build the development channel binary:

```bash
cargo build --release --features development
# Produces target/release/m31a-dev
```

> **Warning:** Do not run `cargo build --all-features`. The `production` and `development` channels are mutually exclusive; enabling both is a compile-time error.
"""

PAGES["getting-started/onboarding.md"] = """# First-Run Onboarding & Workspace Initialization

When M31A is launched in a workspace for the first time, it ensures the repository is properly configured before executing autonomous work.

## Automatic Onboarding Wizard

If you run `m31a` in a new workspace without prior configuration, the interactive **Workspace Setup Wizard** appears automatically in the cockpit:

```text
┌─────────────────────────── Workspace Setup Wizard ───────────────────────────┐
│                                                                               │
│  Welcome to M31 Autonomous (M31A).                                            │
│  Let's configure this repository for safe, verifiable engineering.            │
│                                                                               │
│  [1] Primary Model: meta/llama-3.2-11b-vision-instruct (NVIDIA NIM)           │
│  [2] Autonomy Mode: Safe (Interactive human confirmation on mutations)        │
│  [3] Git Isolation: Isolated Worktrees (m31a/run/*)                           │
│  [4] Sandbox Policy: Standard (Confinement enabled)                           │
│                                                                               │
│  [ Enter ] Save & Initialize Workspace        [ Esc ] Exit                    │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

## Non-Interactive Workspace Initialization

In headless or CI environments, initialize a workspace non-interactively via:

```bash
m31a init
```

To overwrite existing configuration with defaults:

```bash
m31a init --force
```

## Created Files & Storage Structure

Initialization creates the following files within your repository:

```text
<workspace>/
└── .m31a/
    ├── config.toml           # Workspace configuration overrides
    ├── project/              # Projected planning documents & charters
    └── skills/               # Custom workspace skills (optional)
```

All heavy persistent data (SQLite database, checkpoints, event logs, artifact blobs) is stored in **platform user directories**, keeping your git repository completely clean:
- **Linux**: `~/.local/share/m31a/`
- **macOS**: `~/Library/Application Support/m31a/`
- **Windows**: `%LOCALAPPDATA%\m31a\`
"""

PAGES["getting-started/model-setup.md"] = """# Model Setup & NVIDIA Credentials

M31A uses NVIDIA NIM as its exclusive production model provider.

## Obtaining Credentials

1. Visit the NVIDIA API Catalog at [build.nvidia.com](https://build.nvidia.com).
2. Sign in and generate an API key with NIM model access.
3. Your key will have the format: `nvapi-...`.

## Configuring Credentials

M31A supports three ways to configure your key, evaluated in precedence order:

### 1. Environment Variable (Recommended for CI)

```bash
export NVIDIA_API_KEY="nvapi-your-key-here"
```

### 2. User Configuration (~/.config/m31a/config.toml)

```bash
m31a config set provider.nvidia_nim.api_key "nvapi-your-key-here"
```

### 3. TUI Settings Editor

In the interactive cockpit, press `Ctrl+,` to open the Settings surface, navigate to **Provider Credentials**, enter your key, and press `Enter`. The key is masked immediately (`nvap...[MASKED]`).

## Canonical Default Model

The default model is defined in `src/config/canonical.rs`:
```toml
model = "meta/llama-3.2-11b-vision-instruct"
```

Supported NVIDIA NIM models include:
- `meta/llama-3.2-11b-vision-instruct` (Default reasoning & vision)
- `meta/llama-3.1-70b-instruct` (Heavy synthesis & architecture)
- `meta/llama-3.1-405b-instruct` (Large-scale decomposition)
- `nvidia/llama-3.1-nemotron-70b-instruct` (High-precision alignment)

To select a different model for a run:

```bash
m31a run --model "meta/llama-3.1-70b-instruct" "Refactor the authentication module"
```

In the TUI, switch models dynamically using the `/model` slash command.
"""

PAGES["getting-started/installation-troubleshooting.md"] = """# Troubleshooting Installation

Solutions to common installation, permission, and environment issues.

## Diagnostic Command: `m31a doctor`

Whenever encountering startup or installation issues, run:

```bash
m31a doctor --verbose
```

To emit machine-readable JSON for automated verification:

```bash
m31a doctor --json
```

## Common Issues & Remediation

### 1. `m31a: command not found`
- **Cause**: `~/.local/bin` is not in your shell's `PATH`.
- **Fix**: Add `export PATH="$HOME/.local/bin:$PATH"` to `~/.bashrc` or `~/.zshrc`, then restart your terminal.

### 2. `Only NVIDIA NIM models are supported in this release`
- **Cause**: An outdated configuration or environment variable references `openai`, `anthropic`, or `ollama`.
- **Fix**: Clear `OPENAI_API_KEY` and set `NVIDIA_API_KEY`. Update `.m31a/config.toml` to remove non-NVIDIA provider blocks.

### 3. `workspace configuration is invalid: ... (startup on fallback defaults was refused)`
- **Cause**: A `.m31a/config.toml` file exists but contains syntax errors or unrecognized fields.
- **Fix**: M31A fails closed on invalid configs to prevent accidental data loss. Run `m31a config validate` to see the exact syntax error, or delete `.m31a/config.toml` to regenerate safe defaults with `m31a init`.

### 4. `sqlite pool initialization failed: database is locked`
- **Cause**: Another M31A process is holding an exclusive transaction on `~/.local/share/m31a/m31a.db`.
- **Fix**: Check running processes via `ps aux | grep m31a` and terminate stalled instances. SQLite WAL mode handles concurrent readers, but schema migrations require brief exclusive locks.
"""

# ─────────────────────────────────────────────────────────────────────────────
# 3. User Manual
# ─────────────────────────────────────────────────────────────────────────────

PAGES["user-guide/cli-usage.md"] = """# CLI Command Hierarchy & Global Options

M31A provides a comprehensive command-line interface structured with Clap 4.

## Global Options

The following flags are available across all commands:

```text
  -c, --config <PATH>       Path to custom TOML configuration file
  -p, --profile <NAME>      Named configuration profile (safe, coding, autonomous, ci, release)
      --model <NAME>        Override active NVIDIA NIM model name
      --autonomy <LEVEL>    Override autonomy level (safe, plan, assisted, autonomous, unattended)
  -o, --output <FORMAT>     Output format: text, json, stream-json [default: text]
  -q, --quiet               Suppress informational console banners
  -v, --verbose             Enable verbose debug and tracing spans
  -w, --workspace <PATH>    Path to target repository workspace directory [default: .]
  -h, --help                Print help documentation
  -V, --version             Print deployment-aware version string
```

## Primary Commands

### `m31a run <PROMPT>`
Directly executes an autonomous prompt against the workspace.

```bash
m31a run "Add unit tests for error handling in src/lib.rs"
m31a run --profile coding "Fix clippy warnings across the codebase"
```

### `m31a execution` (Alias: `exec`)
Full execution run lifecycle management:

```bash
# List all execution runs in the workspace
m31a exec list

# Show detailed status, DAG, and verification of a specific run
m31a exec show 01924b12-9c48-7fa0-a110-38491823901a

# Pause an active run
m31a exec pause 01924b12-9c48-7fa0-a110-38491823901a

# Resume a paused run
m31a exec resume 01924b12-9c48-7fa0-a110-38491823901a

# Cancel a run with explicit reason
m31a exec cancel 01924b12-9c48-7fa0-a110-38491823901a --reason "Operator override"

# Fork an existing run from its last checkpoint
m31a exec fork 01924b12-9c48-7fa0-a110-38491823901a
```

### `m31a task`
Inspect decomposed DAG tasks:

```bash
m31a task list --execution-id <ID>
m31a task show <TASK_ID>
```

### `m31a policy`
Evaluate security rules:

```bash
m31a policy check "fs:write"
m31a policy check "cli:bash"
```

### `m31a checkpoint`
Inspect and restore durable checkpoints:

```bash
m31a checkpoint list
m31a checkpoint restore <CHECKPOINT_ID>
```

### `m31a artifact`
Inspect generated artifacts, patches, and scorecards:

```bash
m31a artifact list
m31a artifact show <ARTIFACT_ID>
```

### `m31a doctor`
Run environmental diagnostics:

```bash
m31a doctor
m31a doctor --category sandbox
```

### `m31a config`
Configuration management:

```bash
m31a config sources           # Show 8-tier precedence order
m31a config explain <KEY>     # Explain provenance of a setting
m31a config validate          # Validate schema
m31a config get <KEY>
m31a config set <KEY> <VALUE>
```
"""

PAGES["user-guide/tui-cockpit.md"] = """# Interactive Ratatui TUI Cockpit

Launch the cockpit by executing `m31a` with no subcommand in an interactive terminal.

## Cockpit Architecture

The TUI cockpit is powered by Ratatui and Crossterm, running at 30 FPS with bounded channel backpressure. It is strictly a **read-only projection** of the underlying SQLite persistence layer.

```text
┌─ M31 Autonomous Cockpit ──────────────────────────────────── [Mode: Safe] [Profile: Coding] ─┐
│                                                                                               │
│  [Planner] Analyzing repository structure and decomposing objective into 4 DAG tasks...       │
│  ┌─ Task DAG ──────────────────────────────────────────────────────────────────────────────┐ │
│  │ 1. [COMPLETED] Index repository symbols (repo_symbols)                                   │ │
│  │ 2. [RUNNING]   Add error types to src/error.rs (write_file)                              │ │
│  │ 3. [PENDING]   Wire error propagation in src/main.rs                                     │ │
│  │ 4. [PENDING]   Run cargo test verification suite                                         │ │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                               │
│  [Implementer] Proposal: Write 42 lines to `src/error.rs`                                     │
│  [Policy Gate] Policy: ASK (Mutating workspace filesystem)                                    │
│                                                                                               │
│  ┌─ Policy Approval Required ──────────────────────────────────────────────────────────────┐ │
│  │ Tool: fs.write  |  Path: src/error.rs  |  Risk: Medium                                  │ │
│  │ [Y] Approve Action    [N] Deny Action    [D] View Diff    [E] Escalate to Shell         │ │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                               │
├─ Active Run: 01924b12...  Model: meta/llama-3.2-11b-vision-instruct  Tokens: 1,420 ──────────┤
│ > enter prompt or /slash command...                                                           │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Global Keyboard Controls

| Keybinding | Function | Scope |
|---|---|---|
| `Tab` / `Shift+Tab` | Cycle focus between surfaces (Conversation, Tasks, Diff, Settings) | Global |
| `Ctrl+P` | Open Command Palette / Route Navigator | Global |
| `Ctrl+C` | Instant safe cancellation (SIGINT signal escalation) | Global |
| `Ctrl+R` | Replay conversation history / scroll log | Conversation |
| `Ctrl+,` | Open Interactive Settings Editor | Global |
| `Esc` | Close dialog / cancel current input / return to conversation | Modals |
| `PageUp` / `PageDown` | Scroll authoritative conversation or diff viewport | Viewports |
| `Y` / `N` | Approve or Deny pending policy approval dialog | Approval Dialog |

## Integrated Slash Commands

Type `/` in the prompt composer to invoke built-in slash commands:

- `/help` - Show keyboard controls and command catalog.
- `/model [NAME]` - Select or inspect active NVIDIA NIM model.
- `/profile [NAME]` - Switch active profile (`safe`, `coding`, `autonomous`, `ci`, `release`).
- `/autonomy [MODE]` - Switch autonomy mode (`safe`, `plan`, `assisted`, `autonomous`, `unattended`).
- `/clear` - Clear current terminal screen projection (preserves database records).
- `/checkpoint` - Force create an immediate durable checkpoint.
- `/diff` - Toggle full-screen Git diff review surface.
- `/doctor` - Run diagnostic health probes directly in cockpit.
- `/tasks` - Toggle visual DAG progression view.
- `/quit` or `/exit` - Restore terminal and cleanly exit M31A.
"""

PAGES["user-guide/execution-lifecycle.md"] = """# Autonomous Execution Lifecycle

Every execution run in M31A transitions through a deterministic state machine managed by `src/controller/` and `src/state_machine/`.

```mermaid
stateDiagram-v2
    [*] --> Intake: Operator Prompt
    Intake --> Discovery: Workspace Inspection
    Discovery --> Architecture: Contract Definition
    Architecture --> Planning: DAG Decomposition
    Planning --> TaskExecution: Schedule Ready Tasks
    
    state TaskExecution {
        [*] --> ModelProposal
        ModelProposal --> PolicyCheck: Policy Evaluation
        PolicyCheck --> ToolExecution: ALLOW
        PolicyCheck --> HumanApproval: ASK
        HumanApproval --> ToolExecution: Approved
        HumanApproval --> PlanRevision: Denied
        ToolExecution --> VerificationTier: Side Effect Complete
        VerificationTier --> [*]: Evidence Recorded
    }
    
    TaskExecution --> VerificationGate: All Tasks Complete
    VerificationGate --> Completed: Nyquist Verification PASSED
    VerificationGate --> Recovery: Evidence Rejected / Drift
    Recovery --> Planning: Differential Replan
    Completed --> [*]: Durable Attribution Committed
```

## 1. Intake & Discovery
The operator's prompt is parsed into an authoritative `ExecutionRun` record with a unique UUID v7. The runtime discovers workspace baselines, Git HEAD, and configuration profiles.

## 2. Planning & DAG Decomposition
The `planner` agent breaks down the high-level objective into discrete, typed tasks forming a Directed Acyclic Graph (DAG). Dependencies and critical paths are resolved using the Critical Path Method (CPM).

## 3. Gated Execution
Tasks with satisfied dependencies are dispatched to worker agents (`implementer`, `researcher`, `verifier`). Each tool call passes through the non-bypassable Policy Gate.

## 4. 7-Tier Verification Gate
Upon task completion, the runtime executes the 7-tier verification hierarchy. The task is only marked `Succeeded` if all required checks pass with cryptographic evidence.

## 5. Isolated Attribution & Git Commit
When the execution run completes, changes are staged, trailers (including `M31A-Execution-Run`, `M31A-Agent-Role`, `M31A-Verification-Id`) are generated, and a clean Git commit is recorded.
"""

PAGES["user-guide/sessions.md"] = """# Sessions & Multi-Turn Interactions

M31A maintains durable multi-turn interactive sessions allowing developers to collaborate iteratively with the autonomous runtime.

## Session Lifecycle

Sessions are stored in the SQLite `sessions` table and track active execution runs, conversation messages, token usage, and operator preferences.

```bash
# Start a new named interactive session
m31a session new --title "Refactor Auth System"

# List existing sessions
m31a session list

# Resume a previous session
m31a session resume <SESSION_ID>

# Show conversation history and token metrics
m31a session show <SESSION_ID>
```

## Multi-Turn Context Compaction

As conversations grow, M31A's `ContextCompiler` (`src/context/compiler.rs`) monitors context window utilization against the active NVIDIA NIM model's ceiling:
1. **Headroom Reservation**: Reserves 1,536 to 4,096 tokens for tool calling definitions and final responses.
2. **Compaction Threshold**: When context reaches 80-85% capacity, older turns are compacted into semantic summaries while preserving critical file diffs and tool execution evidence.
3. **Evidence Priority Ranking**: Verification failures and compiler error diagnostics receive top priority in compiled prompt envelopes.
"""

PAGES["user-guide/policy-approvals.md"] = """# Policy Approvals & Risk Confirmation

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
"""

PAGES["user-guide/artifacts-evidence.md"] = """# Artifacts, Diffs & Verification Evidence

M31A maintains an immutable, content-addressed ledger of all generated artifacts.

## Artifact Types

Artifacts created during execution are tracked in the SQLite `artifacts` table and stored on disk in `~/.local/share/m31a/artifacts/`:

- **Diff Patches (`.patch`)**: Unified diffs of proposed workspace changes.
- **Test Reports (`.xml`, `.json`)**: Structured test runner outputs and JUnit reports.
- **Compiler Diagnostics**: Captured stderr output and compiler warnings.
- **Planning Documents**: Architectural Decision Records (ADRs), Genesis charters, and roadmaps.
- **Verification Scorecards**: 20-point production evidence records.

## Inspecting Artifacts via CLI

```bash
# List all artifacts generated during a run
m31a artifact list --execution-id <ID>

# Display content of an artifact
m31a artifact show <ARTIFACT_ID>
```

## Cryptographic Snapshot Binding

Before marking an execution run successful, the Nyquist completion gate computes the SHA-256 hash of all modified workspace files and verifies them against the recorded artifact hashes. If workspace drift or unexpected manual modification occurred during execution, the gate refuses completion.
"""

PAGES["user-guide/checkpoints-recovery.md"] = """# Checkpoint Restoration & Crash Recovery

M31A is engineered with fail-safe durability protocols to survive sudden crashes, power outages, and process terminations.

## Two-Phase Durable Checkpoint Protocol

Checkpoints follow a strict prepare → promote → verify → commit order (`src/checkpoint/manager.rs`):

1. **Staging**: External evidence and artifacts are written to `staging/{checkpoint_id}/` and flushed to disk (`sync_all`).
2. **Payload Promotion**: Files are promoted to `FsArtifactStore` and SHA-256 hashes are verified.
3. **Atomic SQLite Commit**: In a single SQLite transaction, checkpoint metadata, manifest JSON, and artifact linkages are committed.

## Startup Crash Recovery Scanner

When M31A starts up (`src/checkpoint/crash_recovery.rs`), it automatically inspects the database for unfinished runs and classifies them into 4 deterministic states:

| Recovery State | Definition | Resolution |
|---|---|---|
| **`SafeToResume`** | Checkpoint valid, artifacts intact, repo clean | Auto-resumable from last task |
| **`NeedsRepair`** | Valid checkpoint, workspace files drifted | Prompts operator to restore workspace snapshot |
| **`Ambiguous`** | Conflicting evidence or unexplained drift | Fails closed; halts execution and alerts operator |
| **`Corrupt`** | Missing artifact blobs or corrupt database | Rollback to last known-good checkpoint |

## Manual Checkpoint Management

```bash
# Force create an immediate checkpoint
m31a checkpoint create --label "Pre-refactor snapshot"

# List available checkpoints
m31a checkpoint list

# Restore workspace and runtime state from a checkpoint
m31a checkpoint restore <CHECKPOINT_ID>
```
"""

PAGES["user-guide/headless-ci.md"] = """# Headless Execution & CI Workflows

M31A is designed for headless automation in continuous integration and automated code repair pipelines.

## Stable Exit Codes

CI scripts can reliably branch on M31A's numeric process exit codes (`src/cli/exit_codes.rs`):

| Exit Code | Identifier | Semantic Meaning |
|---|---|---|
| **0** | `Success` | Execution run completed and passed all verification checks |
| **1** | `GeneralError` | Unhandled runtime exception or command failure |
| **2** | `ConfigError` | Invalid or unparseable configuration file |
| **3** | `VerificationFailed` | Nyquist gate failed; tests or compiler checks rejected code |
| **4** | `PolicyViolation` | Action denied by security policy or unattended approval required |
| **5** | `Interrupted` | Execution cancelled by operator or SIGINT/SIGTERM signal |
| **6** | `ResourceExhausted` | Concurrency, timeout, or memory bounds exceeded |
| **7** | `CrashRecovered` | Unhandled crash recovered from durable checkpoint |

## GitHub Actions Example

```yaml
name: Autonomous Code Maintenance

on:
  workflow_dispatch:
  schedule:
    - cron: '0 3 * * 1' # Weekly Monday at 3 AM

jobs:
  m31a-lint-fix:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable
        
      - name: Install M31A
        run: |
          curl -fsSL https://docs.m31a.tonmoyinfrastructure.org/install.sh | bash
          echo "$HOME/.local/bin" >> $GITHUB_PATH
          
      - name: Execute Autonomous Refactor
        env:
          NVIDIA_API_KEY: ${{ secrets.NVIDIA_API_KEY }}
        run: |
          m31a run \
            --autonomy unattended \
            --profile ci \
            --output stream-json \
            "Fix all clippy warnings and ensure cargo test passes"
            
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v6
        with:
          title: "fix: autonomous clippy remediation"
          branch: "m31a/clippy-fixes"
```
"""

PAGES["user-guide/custom-commands.md"] = """# User-Defined Slash Commands

Operators can extend M31A's cockpit with reusable, project-specific custom slash commands defined in TOML.

## Custom Command Schema

Store custom commands in `.m31a/commands/<name>.toml` or user global directory `~/.config/m31a/commands/`:

```toml
# .m31a/commands/review-pr.toml
name = "review-pr"
description = "Perform rigorous architecture and security review of current Git diff"
role = "reviewer"
profile = "security_review"
autonomy = "safe"

prompt = \"\"\"
Inspect all uncommitted changes or diff against origin/master.
Verify that:
1. No sensitive credentials or API keys are exposed.
2. Error handling does not use unwrap() in production paths.
3. Unit tests are included for new code paths.
Emit a structured review scorecard with findings categorized by severity.
\"\"\"
```

## Invocation

Once defined, the command appears in the TUI autocomplete and can be executed directly:

```text
> /review-pr
```

Or from the CLI:

```bash
m31a run "/review-pr"
```
"""

# ─────────────────────────────────────────────────────────────────────────────
# 4. Core Architecture
# ─────────────────────────────────────────────────────────────────────────────

PAGES["architecture/overview.md"] = """# M31A System Architecture (L0-L9)

M31A is organized into 10 strict downward-dependent architectural layers.

```mermaid
graph TD
    L9["Layer 9: CLI, TUI Cockpit & Integrations"]
    L8["Layer 8: Autonomy, Workflow & State Machine"]
    L7["Layer 7: Verification, Recovery & Evaluation"]
    L6["Layer 6: Execution, Jobs & Artifact Ledger"]
    L5["Layer 5: Planning, DAG & Task Scheduling"]
    L4["Layer 4: Agent Pool, Roles & Delegation"]
    L3["Layer 3: Model Providers, Context & Prompts"]
    L2["Layer 2: Capabilities, Tools & Process Tree"]
    L1["Layer 1: Security, Policy Gates & Sandbox"]
    L0["Layer 0: Kernel, Persistence & Storage Layout"]

    L9 --> L8
    L8 --> L7
    L7 --> L6
    L6 --> L5
    L5 --> L4
    L4 --> L3
    L3 --> L2
    L2 --> L1
    L1 --> L0
```

## Layer Summary

| Layer | Primary Subsystems | Core Responsibilities |
|---|---|---|
| **L0 Kernel & Storage** | `kernel`, `persistence`, `storage`, `events`, `ids` | Strongly typed UUID v7 domain IDs, SQLite database pool, storage layout, cancellation tokens |
| **L1 Security & Policy** | `policy`, `sandbox`, `platform`, `config` | Non-bypassable policy evaluation, 8-tier configuration engine, Landlock/seccomp confinement |
| **L2 Capabilities & Tools** | `capability`, `tools`, `process`, `git`, `repo` | 28 core model tools, process tree supervision, Git worktrees, LSP code intelligence |
| **L3 Intelligence & Context**| `model`, `prompt`, `context`, `memory` | NVIDIA NIM provider, SSE streaming accumulator, context token compaction, prompt templates |
| **L4 Agents & Roles** | `agent`, `skill` | 18 built-in agent roles, supervisor, adaptive replanning, multi-agent task delegation |
| **L5 Planning & Scheduling**| `planning`, `dag`, `scheduler` | Task graph decomposition, Critical Path Method (CPM), topological sorting, job worker pool |
| **L6 Execution & Checkpoints**| `change`, `checkpoint`, `pipeline` | Two-phase checkpoint manager, artifact ledger, workspace change application |
| **L7 Verification & Recovery**| `verification`, `eval`, `recovery` | 7-tier verification hierarchy, Nyquist gate, crash recovery scanner, acceptance eval |
| **L8 Autonomy & Workflows** | `controller`, `state`, `workflow`, `telemetry` | Autonomy controller, stage progression, Genesis multi-stage workflows, metrics collection |
| **L9 CLI, TUI & Deployment**| `cli`, `tui`, `init`, `interaction`, `deployment` | Clap 4 CLI, Ratatui cockpit, setup wizard, compile-time deployment channel isolation |
"""

PAGES["architecture/runtime-authority.md"] = """# Runtime Authority & State Machine

The core architectural invariant of M31A is: **The model proposes. The runtime decides.**

## Authoritative vs Projected State

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       AUTHORITATIVE STATE (Layer 0)                         │
│   SQLite Database  •  FsArtifactStore  •  StorageLayout  •  Git Commits     │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Async Event Stream & SQLx Queries
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PROJECTED READ-ONLY STATE (Layer 9)                      │
│   Ratatui Cockpit Surfaces  •  CLI Stdout / JSON  •  TUI Viewports          │
└─────────────────────────────────────────────────────────────────────────────┘
```

The LLM is a stateless reasoning engine. It does not own execution state, task graphs, or verification results.
- **Authoritative State**: Stored in SQLite tables (`execution_runs`, `tasks`, `checkpoints`, `artifacts`, `verification_checks`).
- **Projected State**: Rendered in the Ratatui cockpit or CLI output. A crash or termination of the TUI has zero effect on the validity of authoritative database records.

## State Transition Matrices

M31A enforces formal state transition matrices in `src/state_machine/`:

### ExecutionRun Status Transitions
`Pending → Starting → Running → Paused (or Failed, Cancelled) → Succeeded`
A transition to `Succeeded` requires proof of passing verification checks in SQLite.

### Task Status Transitions
`Pending → Blocked (dependencies) → Ready → Dispatched → Executing → Verifying → Succeeded (or Failed)`
"""

PAGES["architecture/request-dispatch.md"] = """# Request Dispatch & Composition Root

Understanding how CLI commands, interactive inputs, and background jobs enter the M31A runtime.

## The Composition Root: `AppRuntime`

`src/runtime.rs` contains the authoritative composition root: `AppRuntime`.
It wires together:
- `SqlitePool` (Persistence)
- `BroadcastEventBus` (Event distribution)
- `ResolvedConfiguration` (Authoritative config)
- `NvidiaProvider` (Model reasoning)
- `CapabilityRegistry` & `ToolRegistry` (Side-effect interfaces)
- `EffectivePolicy` (Security evaluation)
- `Scheduler` & `ExecutionEngine` (Work scheduling)

## Command Flow

```text
Operator Input (CLI / TUI)
       │
       ▼
clap::Parser / TuiInput
       │
       ▼
CliDispatcher::dispatch() ──► RuntimeCommand::RunExecution
                                        │
                                        ▼
                               AppRuntime::execute_run()
                                        │
                                        ▼
                               WorkerDispatcher / TaskGraph
```

All interactions normalize into typed `RuntimeCommand` variants (`src/cli/dispatch.rs`), guaranteeing identical semantics whether invoked from the CLI or TUI.
"""

PAGES["architecture/planning-dag.md"] = """# Planning DAG & Critical Path Scheduling

M31A models autonomous software engineering as a dependency-aware Directed Acyclic Graph (DAG) of discrete tasks.

## DAG Representation & Critical Path Method

Located in `src/dag/`:
- **Nodes**: `Task` entities with explicit inputs, outputs, required capabilities, and verification strategies.
- **Edges**: Dependency relationships (`depends_on`).
- **Critical Path Method (`cpm.rs`)**: Calculates earliest start times, latest completion times, and identifies bottleneck tasks along the critical path to optimize parallel execution.

```mermaid
graph LR
    T1[1. Index Repository Symbols] --> T2[2. Implement Core Trait]
    T1 --> T3[3. Write Unit Test Suite]
    T2 --> T4[4. Wire Subsystem Callers]
    T3 --> T5[5. Execute Verification Run]
    T4 --> T5
```

## Cycle Detection & Validation

Before materializing a DAG into SQLite, `src/dag/validator.rs` validates:
1. **Acyclicity**: Tarjan's strongly connected components algorithm ensures no cyclic deadlocks exist.
2. **Capability Satisfaction**: Verifies that required capabilities (e.g. `fs.write`, `process.exec`) are permitted under the active policy.
3. **Verification Feasibility**: Confirms that every mutating task specifies an executable verification strategy.
"""

PAGES["architecture/security-boundaries.md"] = """# Security Boundaries & Policy Enforcement

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
"""

PAGES["architecture/persistence-design.md"] = """# Persistence Design & Relational Schema

M31A uses an embedded SQLite database configured with Write-Ahead Logging (WAL) and foreign keys enabled.

## Canonical Relational Entity Relationships

```mermaid
erDiagram
    SESSIONS ||--o{ EXECUTION_RUNS : contains
    EXECUTION_RUNS ||--o{ TASKS : decomposes_into
    EXECUTION_RUNS ||--o{ EVENT_LOG : records
    EXECUTION_RUNS ||--o{ CHECKPOINTS : commits
    EXECUTION_RUNS ||--o{ ARTIFACTS : produces
    TASKS ||--o{ VERIFICATION_CHECKS : requires
    TASKS ||--o{ TOOL_EXECUTIONS : invokes
    TOOL_EXECUTIONS ||--o{ POLICY_DECISIONS : gated_by
```

## Migration Infrastructure

Migrations reside in `migrations/` and are managed via SQLx:
- `001_initial.sql` to `012_interactive_sessions.sql`: Core schema (tasks, events, checkpoints, sessions).
- `013_workflow_orchestration.sql` to `028_model_invocation_cost.sql`: Advanced workflows, prompt refs, and telemetry.
- `029_remove_budget_system.sql`: Decommissioned token budget ledger.
- `030_replace_mission_with_execution_run.sql` to `032_canonical_execution_run_consolidation.sql`: Replaced legacy missions with canonical `execution_runs`.
"""

PAGES["architecture/events-telemetry.md"] = """# Event Bus & Structured Telemetry

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
"""

# ─────────────────────────────────────────────────────────────────────────────
# 5. Subsystems Manuals
# ─────────────────────────────────────────────────────────────────────────────

PAGES["subsystems/overview.md"] = """# Runtime Subsystem Manuals Overview

M31A contains 20 dedicated architectural subsystems. These manuals provide deep architectural explanations of their internal mechanics, authority ownership, data flows, and tested invariants.

## Subsystem Catalog

| Subsystem | Primary Module | Core Functionality |
|---|---|---|
| [Application Startup](startup-lifecycle) | `src/main.rs`, `src/init/` | Panic hooks, storage migration, configuration bootstrapping |
| [Configuration Engine](configuration) | `src/config/` | 8-tier precedence engine, canonical defaults, schema validation |
| [CLI & Dispatch](cli-dispatcher) | `src/cli/` | Clap hierarchy, exit code taxonomy, runtime command routing |
| [Sessions & Runtime](sessions-runtime) | `src/runtime.rs`, `src/interaction/` | `AppRuntime` composition root, interactive session persistence |
| [Agent Pool & Registry](agent-registry) | `src/agent/` | 18 built-in agent roles, supervisor, adaptive replanning |
| [Model & Providers](model-provider) | `src/model/` | NVIDIA NIM provider, SSE stream accumulator, token metrics |
| [Context & Prompts](context-prompts) | `src/context/`, `src/prompt/` | Context compaction, prompt reference catalog, token budgeting |
| [Planning & Scheduling](planning-dag) | `src/planning/`, `src/dag/` | Task decomposition, CPM critical path, cycle validation |
| [Capabilities & Tools](capabilities-tools) | `src/capability/`, `src/tools/` | 28 core tools, extended tools, provider abstraction |
| [Policy & Approvals](policy-approvals) | `src/policy/` | 4 policy decisions, multi-layer rules, interactive approvals |
| [Filesystem & Repo](filesystem-repo) | `src/repo/`, `src/change/` | AST symbol extraction, repo search, workspace mutation |
| [Process Supervision](process-sandboxing) | `src/process/`, `src/sandbox/` | PID recycling protection, spool capture, signal escalation |
| [Git & Attribution](git-attribution) | `src/git/` | Worktree isolation, commit trailers, attribution ledger |
| [Verification & Nyquist](verification-nyquist) | `src/verification/` | 7-tier verification hierarchy, evidence snapshot matching |
| [Events & Telemetry](events-telemetry) | `src/events/`, `src/telemetry/` | Broadcast event bus, distributed tracing spans |
| [Persistence & Migrations](persistence-migrations) | `src/persistence/` | SQLite WAL connection pool, migrations 001-032 |
| [Checkpoints & Recovery](checkpoints-recovery) | `src/checkpoint/` | Two-phase commit protocol, crash recovery scanner |
| [Ratatui TUI Cockpit](tui-ratatui) | `src/tui/` | 62-file terminal cockpit, read-only projection, streaming |
| [Deployment Channels](deployment-channels) | `src/deployment/` | Compile-time channel isolation (`production` vs `development`) |
"""

PAGES["subsystems/startup-lifecycle.md"] = """# Subsystem: Application Startup Lifecycle

Detailed breakdown of how M31A initializes from process entry point to execution readiness.

## Entry Point: `src/main.rs`

The startup sequence follows 10 discrete phases:
1. **Panic Hook Installation (`install_panic_hook`)**: Restores standard terminal modes (disables raw mode, leaves alternate screen, restores cursor) if an unexpected panic occurs.
2. **Channel-Aware `--version` Check**: Intercepts `-V` / `--version` before heavy runtime initialization, returning compile-time channel identity.
3. **CLI Parsing**: Clap parses arguments into `Cli` and extracts `CliOverrides`.
4. **Storage Layout & Migration**: `StorageLayout::new` resolves global platform dirs and migrates any legacy project-local databases to the canonical platform path.
5. **Configuration Resolution**: `ResolvedConfiguration::builder` loads configuration layers. Present-but-invalid configs trigger an immediate exit (`exit(1)`).
6. **SQLite Initialization**: `initialize_database(&db_path)` applies all pending SQL migrations idempotently.
7. **Broadcast Event Bus**: Creates `BroadcastEventBus` with capacity 2,048.
8. **Startup Crash Recovery**: `recover_startup_crashes(&pool)` checks for interrupted runs from previous sessions.
9. **Dispatch or Interactive Cockpit**:
   - If subcommand specified: executes via `CliDispatcher`.
   - If interactive terminal: checks onboarding status and launches `TuiApplication`.
10. **Async Runtime Assembly**: TUI renders an immediate first frame while background async runtime assembly hydrations proceed smoothly.
"""

PAGES["subsystems/configuration.md"] = """# Subsystem: Configuration Engine

The M31A configuration subsystem (`src/config/`) enforces deterministic resolution across 8 hierarchical tiers.

## The 8-Tier Precedence Hierarchy

Defined in `src/config/hierarchy.rs`:

```text
Tier 0: Immutable Security Invariants (Kernel hardcoded floors)
  ▲
Tier 1: System-wide Machine Configuration (/etc/m31a/config.toml)
  ▲
Tier 2: User Global Configuration (~/.config/m31a/config.toml)
  ▲
Tier 3: Workspace Repository Configuration (<repo>/.m31a/config.toml)
  ▲
Tier 4: Active Named Profile (safe, coding, autonomous, ci, release)
  ▲
Tier 5: Environment Variables (M31A_*, NVIDIA_API_KEY)
  ▲
Tier 6: CLI Argument Overrides (--config, --model, --autonomy)
  ▲
Tier 7: Interactive Session Overrides (/model, /profile slash commands)
```

## Monotonic Security Merging

The `MonotonicSecurityMerger` (`src/config/merge.rs`) guarantees that higher configuration tiers **can never weaken** security invariants established by lower tiers. A profile or CLI flag can enforce stricter policies (e.g. converting `Ask` to `Deny`), but cannot disable Landlock sandboxing or grant access to sensitive paths.
"""

PAGES["subsystems/cli-dispatcher.md"] = """# Subsystem: CLI & Command Dispatch

The command dispatch subsystem (`src/cli/`) unifies command handling across CLI invocations and TUI user interactions.

## Dispatch Architecture

- `src/cli/args.rs`: Clap 4 declarative parser definitions.
- `src/cli/dispatch.rs`: `CliDispatcher` executing `RuntimeCommand` variants.
- `src/cli/exit_codes.rs`: Stable process exit codes (0 to 7).
- `src/cli/output.rs`: Formatted text, JSON, and NDJSON streaming formatters.

## Exit Code Taxonomy

Guaranteed exit code values:
- `0`: Success
- `1`: General Error
- `2`: Configuration Error
- `3`: Verification Failed (Nyquist gate)
- `4`: Policy Violation / Unattended Approval Required
- `5`: Interrupted (SIGINT/SIGTERM)
- `6`: Resource Exhausted
- `7`: Crash Recovered
"""

PAGES["subsystems/sessions-runtime.md"] = """# Subsystem: Sessions & Runtime Core

The `AppRuntime` struct in `src/runtime.rs` is the authoritative composition root.

## Composition Root Responsibilities

`AppRuntime` encapsulates:
- SQLite persistence pool (`SqlitePool`)
- Event distribution bus (`Arc<BroadcastEventBus>`)
- Resolved configuration (`Arc<ResolvedConfiguration>`)
- Model provider (`Arc<dyn ModelProvider>`)
- Capability & Tool catalogs (`Arc<CapabilityRegistry>`, `Arc<ToolRegistry>`)
- Policy engine (`Arc<EffectivePolicy>`)

It provides high-level application methods:
- `execute_run(prompt, profile, ...)`
- `pause_execution(run_id)`
- `resume_execution(run_id)`
- `cancel_execution(run_id, reason)`
"""

PAGES["subsystems/agent-registry.md"] = """# Subsystem: Agent Pool & Registry

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
"""

PAGES["subsystems/model-provider.md"] = """# Subsystem: Model & Provider Layer

The model subsystem (`src/model/`) interfaces with language model reasoning engines.

## NVIDIA NIM Exclusivity

Production model invocation is handled exclusively by `NvidiaProvider` (`src/model/provider/nvidia.rs`), communicating via OpenAI-compatible Server-Sent Events (SSE) streaming with `https://integrate.api.nvidia.com/v1`.

### Masked Secrets
API keys are wrapped in `MaskedSecret` (`src/config/provider_registry.rs`). The raw key is exposed only when constructing HTTP `Authorization: Bearer ...` headers. In all logs, events, and TUI projections, it is masked (`nvap...[MASKED]`).
"""

PAGES["subsystems/context-prompts.md"] = """# Subsystem: Context & Prompt System

Manages prompt templates, token budgeting, and context compaction (`src/context/`, `src/prompt/`).

## Dynamic Context Compilation

The `ContextCompiler` compiles prompt envelopes dynamically:
- Calculates exact token counts using tiktoken-compatible tokenizers.
- Compresses older conversation history when context exceeds 80% of model limits.
- Injects repository baseline evidence, relevant symbols, and active policy rules.
"""

PAGES["subsystems/planning-dag.md"] = """# Subsystem: Planning & DAG Scheduling

Constructs and executes task graphs (`src/planning/`, `src/dag/`, `src/scheduler/`).

## Task Graph Materialization

1. The `planner` proposes tasks and dependencies.
2. `DagValidator` checks for cycles and capability validity.
3. Tasks are materialized into the SQLite `tasks` table with initial status `Pending` or `Blocked`.
4. As upstream tasks succeed, the `Scheduler` admits ready tasks up to concurrency limits.
"""

PAGES["subsystems/capabilities-tools.md"] = """# Subsystem: Capabilities & Tools Catalog

The tool catalog (`src/tools/registry.rs`) provides 28 core tools and extended tools.

## Core 28 Tools

- **Filesystem (7)**: `read_file`, `write_file`, `edit_file`, `apply_patch`, `list_files`, `glob`, `grep`.
- **Repository (3)**: `repo_search`, `repo_symbols`, `repo_dependencies`.
- **Process & Jobs (5)**: `run_command`, `start_job`, `job_status`, `job_output`, `job_stop`.
- **Git (8)**: `git_status`, `git_diff`, `git_log`, `git_show`, `git_branch`, `git_checkout`, `git_add`, `git_commit`.
- **QA (3)**: `run_tests`, `run_formatter`, `run_linter`.
- **Artifacts (2)**: `create_artifact`, `read_artifact`.
"""

PAGES["subsystems/policy-approvals.md"] = """# Subsystem: Policy & Approval Coordination

Enforces security authorization before every tool call (`src/policy/`).

## Approval Coordination

`ApprovalCoordinator` coordinates interactive human confirmation:
- Creates `ApprovalRequest` with unique ID and risk level.
- Emits approval event to cockpit.
- Suspends tool execution until operator grants (`Approve`) or denies (`Deny`) the request.
"""

PAGES["subsystems/filesystem-repo.md"] = """# Subsystem: Filesystem & Repository Intelligence

Indexes codebases and handles file mutations (`src/repo/`, `src/change/`).

## Code Intelligence

- AST symbol parsing and definition lookup (`src/repo/symbols.rs`).
- Fast regex and keyword search across repositories (`src/repo/search.rs`).
- Workspace drift detection comparing active files against pre-execution baselines.
"""

PAGES["subsystems/process-sandboxing.md"] = """# Subsystem: Process Supervision & Sandboxing

Supervises background processes and enforces OS sandboxing (`src/process/`, `src/sandbox/`).

## Process Supervision

- `ProcessTreeController` tracks child PIDs and process groups.
- Validates `/proc/<pid>/stat` start times before sending signals to prevent PID recycling race conditions.
- Captures stdout/stderr into bounded disk spools.
"""

PAGES["subsystems/git-attribution.md"] = """# Subsystem: Git Worktrees & Attribution

Isolates changes and guarantees audit provenance (`src/git/`).

## Git Worktree Isolation

Runs execute in dedicated worktrees under `.m31a/worktrees/run-<id>/` on branch `m31a/run/<id>`.

## Commit Trailers

Commits include structured provenance trailers:
```text
M31A-Execution-Run: 01924b12-9c48-7fa0-a110-38491823901a
M31A-Agent-Role: implementer
M31A-Model: meta/llama-3.2-11b-vision-instruct
M31A-Verification-Id: 01924b12-9d10-7aa1-b204-129038192301
```
"""

PAGES["subsystems/verification-nyquist.md"] = """# Subsystem: Verification & Nyquist Completion Gate

Enforces Law 6: Completion requires deterministic evidence (`src/verification/`).

## The 7-Tier Verification Hierarchy

```text
Tier 1: Deterministic Check (file presence, syntax, hash consistency)
  ▼
Tier 2: Compiler Check (cargo check, type verification)
  ▼
Tier 3: Test Runner (cargo test, pytest, npm test)
  ▼
Tier 4: Static Analysis (clippy, formatting, linter)
  ▼
Tier 5: Diff & Invariants (workspace baseline snapshot matching)
  ▼
Tier 6: Automated Reviewer (independent review role audit)
  ▼
Tier 7: Failure Diagnosis (diagnostician analysis on failure)
```

Fail-fast gating halts downstream checks immediately if an earlier tier fails.
"""

PAGES["subsystems/events-telemetry.md"] = """# Subsystem: Events & Observability

Event distribution and distributed telemetry spans (`src/events/`, `src/telemetry/`).

## Telemetry Metrics

Tracks:
- Total execution duration and task wall-clock time
- Model invocations, prompt tokens, completion tokens
- Tool execution count, success rate, and failure taxonomy
"""

PAGES["subsystems/persistence-migrations.md"] = """# Subsystem: Persistence & Migrations

SQLite database management and schema evolution (`src/persistence/`).

## WAL Mode & Connection Pool

- Configured with `PRAGMA journal_mode = WAL` and `PRAGMA synchronous = NORMAL`.
- Supports concurrent reader threads without blocking writes.
- Manages migrations 001 through 032.
"""

PAGES["subsystems/checkpoints-recovery.md"] = """# Subsystem: Checkpoints & Crash Recovery

Two-phase commit checkpoints and startup recovery (`src/checkpoint/`).

## Crash Recovery Flow

1. On startup, queries `checkpoints` and `execution_runs`.
2. Inspects unsealed spool files and seals them with `[INTERRUPTED]`.
3. Reconciles running jobs and orphan processes.
4. Classifies status into `SafeToResume`, `NeedsRepair`, `Ambiguous`, or `Corrupt`.
"""

PAGES["subsystems/tui-ratatui.md"] = """# Subsystem: Ratatui TUI Cockpit

The 62-file terminal user interface (`src/tui/`).

## Rendering Pipeline

- First frame rendered synchronously before any async runtime await.
- Event loop polls crossterm input and runtime action channels.
- Renders modular surfaces: Conversation, Tasks, Diff, Settings, Doctor, Model Selector.
"""

PAGES["subsystems/deployment-channels.md"] = """# Subsystem: Deployment Channels & Updates

Compile-time channel isolation and update mechanisms (`src/deployment/`).

## Mutually Exclusive Channels

- Production: binary `m31a`, global directory `~/.local/share/m31a`, feed `stable`.
- Development: binary `m31a-dev`, global directory `~/.local/share/m31a-dev`, feed `development`.
- Rollback mechanism restores previous binary from `.bak` backup if an update fails.
"""

# ─────────────────────────────────────────────────────────────────────────────
# 6. Tests, Reference, Developer, Security, Deployment, Troubleshooting
# ─────────────────────────────────────────────────────────────────────────────

PAGES["tests/overview.md"] = """# Test Architecture Overview

M31A maintains an exhaustive 266-suite test architecture located under `tests/` and in inline module unit tests.

## Testing Strategy

Testing is structured into distinct assurance tiers:
1. **Deterministic CI Tests**: Run in continuous integration without network or credential dependencies, utilizing mock doubles and isolated temporary worktrees.
2. **Architectural Invariant Tests**: Programmatic verification of layer dependencies, single-crate rules, and authority boundaries.
3. **Security Regressions**: Targeted negative tests for policy enforcement, Landlock confinement, and sensitive paths.
4. **Partitioned Live Model Tests**: Real NVIDIA NIM API invocations, strictly marked `#[ignore]` to prevent false-green CI outcomes.
"""

PAGES["tests/categories.md"] = """# Test Categories & Execution Contracts

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
"""

PAGES["reference/cli.md"] = """# Complete CLI Reference

Exhaustive reference of all CLI commands, subcommands, and flags in M31A 0.1.12.

## Command Tree

```text
m31a [OPTIONS] [COMMAND]

COMMANDS:
  session      Interactive developer session operations: list, show, resume, new
  execution    Execution run operations: run, list, show, pause, resume, cancel, fork (alias: exec)
  run          Direct execution run: execute prompt immediately
  task         Task management and inspection: list, show
  agent        Agent roles and pool inspection: list
  capability   System capabilities and provider status: list
  policy       Policy evaluation and security rule checks: check
  checkpoint   State checkpoint management: list, restore
  artifact     Inspect generated execution artifacts: list, show
  doctor       Run comprehensive environmental diagnostic probes
  telemetry    Local telemetry and execution trace inspection: inspect
  config       Configuration validation and inspection: validate, get, set, sources, explain
  eval         Autonomous evaluation harness for acceptance scenarios: run
  tui          Launch full Ratatui interactive TUI cockpit
  init         Initialize workspace onboarding state
  version      Print version information (--verbose shows build identity)
  deployment   Show deployment identity: channel, version, target, paths
  update       Check for or apply updates from a deployment manifest file
  rollback     Restore previous known-good binary after failed update
```
"""

PAGES["reference/configuration.md"] = """# Configuration Schema & Precedence Reference

Complete specification of M31A configuration fields and defaults.

## Configuration File Example (`config.toml`)

```toml
# Authoritative defaults from src/config/canonical.rs
model = "meta/llama-3.2-11b-vision-instruct"

[runtime]
sandbox_mode = "standard"
concurrency_limit = 4
timeout_secs = 300

[policy]
default_action = "ask"
interactive_approvals = true
sandbox_mode = "standard"

[git]
branch_prefix = "m31a/run"
retention_policy = "keep_on_failure"
execution_isolation = "best_effort"

[tui]
theme = "dark-slate-cyan"
fps = 30
```
"""

PAGES["reference/profiles.md"] = """# Profiles Reference

M31A includes 10 pre-configured profiles in `assets/profiles/`:

| Profile | Autonomy Mode | Verification Tier | Concurrency | Primary Use Case |
|---|:---:|:---:|:---:|---|
| **`safe`** | Safe | 5 | 2 | Default profile; interactive approvals on all mutations |
| **`coding`** | Assisted | 4 | 4 | General development, automated refactoring |
| **`autonomous`**| Autonomous | 3 | 4 | Large-scale autonomous feature development |
| **`ci`** | Unattended | 5 | 8 | Headless continuous integration automation |
| **`research`** | Plan | 1 | 4 | Read-only codebase exploration and architecture analysis |
| **`security_review`** | Plan | 6 | 2 | Deep security auditing and attack surface evaluation |
| **`release`** | Assisted | 7 | 2 | Release certification across 20-point evidence matrix |
| **`balanced`** | Assisted | 3 | 4 | General daily development |
| **`conservative`** | Safe | 6 | 1 | High-risk production hotfixes |
| **`code_reviewer`** | Plan | 6 | 2 | Automated pull request code reviews |
"""

PAGES["reference/tools.md"] = """# Tools Catalog Reference

Complete specification of all model-facing tools registered in `ToolRegistry`.

## 28 Core Tools

### Filesystem
- `read_file`: Read contents of file within workspace.
- `write_file`: Overwrite file contents.
- `edit_file`: Contiguous pattern replacement.
- `apply_patch`: Apply unified diff.
- `list_files`: Enumerate workspace files.
- `glob`: Pattern file search.
- `grep`: Regex text search.

### Repository
- `repo_search`: Semantic and keyword code search.
- `repo_symbols`: AST symbol extraction.
- `repo_dependencies`: Module dependency analysis.

### Process & Jobs
- `run_command`: Supervised foreground process execution.
- `start_job`: Background job admission.
- `job_status`: Check job status and PID.
- `job_output`: Stream stdout/stderr.
- `job_stop`: Signal termination.

### Git
- `git_status`, `git_diff`, `git_log`, `git_show`, `git_branch`, `git_checkout`, `git_add`, `git_commit`.

### QA & Artifacts
- `run_tests`, `run_formatter`, `run_linter`, `create_artifact`, `read_artifact`.
"""

PAGES["reference/database.md"] = """# Database Schema & Migrations Reference

M31A maintains an embedded SQLite database with 32 schema migrations.

## Key Tables

- `execution_runs`: Canonical root orchestrator entities (ID, objective, status, workspace_root).
- `tasks`: Decomposed DAG tasks (run_id, title, status, dependencies).
- `checkpoints`: Durable state snapshots (run_id, manifest_hash, manifest_json).
- `artifacts`: Content-addressed file ledger (run_id, hash, artifact_type, storage_path).
- `verification_checks`: Recorded verification results and evidence hashes.
- `policy_decisions`: Comprehensive audit trail of all policy evaluations.
- `sessions`: Interactive multi-turn developer conversations.
"""

PAGES["developer/setup.md"] = """# Developer Setup & Tooling

How to set up a local development environment for contributing to M31A.

## Prerequisites

- **Rust**: 1.85+ stable (`rustup toolchain install stable`)
- **Git**: 2.30+
- **Make**: GNU Make

## Bootstrap & Build

```bash
git clone https://github.com/eshanized/M31A.git
cd M31A

# Validate environment and toolchain
make bootstrap

# Check compilation across both channels
make check

# Build production binary
make build

# Run deterministic test suite
make test
```
"""

PAGES["developer/contributing.md"] = """# Contributor Guidelines

Guidelines for submitting bug reports, documentation updates, and pull requests to M31A.

## Non-Negotiable Rules

1. Single crate architecture: Do not introduce Cargo workspace splits.
2. Downward dependency discipline: Lower layers must not import higher layers.
3. Policy gate non-bypassability: All side effects must pass through Layer 1.
4. TUI is a read-only projection: Authoritative state belongs in SQLite.
5. No fake success: Unimplemented paths return explicit errors.
"""

PAGES["developer/adding-tools-and-agents.md"] = """# Adding Tools & Agent Roles

How to extend M31A with new capabilities or agent personas.

## Adding a New Tool

1. Implement the `TypedTool` trait in `src/tools/`.
2. Define input arguments with `serde::Deserialize`.
3. Specify required capabilities and risk classification.
4. Register the tool in `ToolRegistry::new_default` or `register_extended_tools`.
5. Add unit tests verifying policy gate enforcement.

## Adding an Agent Role

1. Add role identifier to `src/state_machine/agent.rs`.
2. Define role profile in `src/agent/registry/builtins.rs` with model policy, context limits, and capability envelope.
3. Add corresponding prompt template in `prompts/agents/`.
4. Register role in `RoleRegistry`.
"""

PAGES["developer/testing-guidelines.md"] = """# Testing Guidelines & CI Quality Gates

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
"""

PAGES["security/overview.md"] = """# Security Architecture & Threat Model

M31A is built on the principle that autonomous AI agents are untrusted actors operating inside your development environment.

## Threat Assumptions

- Model proposals may contain hallucinations, invalid syntax, or unintended side effects.
- Repository contents may contain prompt injection payloads designed to trick agents into exfiltrating secrets.
- External dependencies or build scripts may contain malicious post-install hooks.

## Defense Layers

1. **Non-Bypassable Policy Gate**: Evaluates every tool execution before invocation.
2. **Process Sandboxing**: Landlock filesystem sandboxing and seccomp system call filtering.
3. **Sensitive Path Blocking**: Absolute prohibition on accessing SSH keys, cloud tokens, or password stores.
4. **Secret Masking**: Prevents credentials from ever appearing in logs, events, or UI projections.
"""

PAGES["security/threat-model.md"] = """# Threat Model & Attack Surface

Analysis of threats and how M31A mitigates them.

### Prompt Injection
Untrusted repository data (e.g. comments, READMEs) attempting to instruct the model to "delete all files" or "curl evil.com".
- *Mitigation*: The LLM has zero direct execution authority. Mutating commands trigger the Policy Gate, requiring human approval (`Ask`) in Safe mode or strict denial (`Deny`) in Plan mode.

### Secret Exfiltration
Model attempting to read `~/.ssh/id_rsa` or `~/.aws/credentials` and output them.
- *Mitigation*: Sensitive path filters block reads at the kernel seam before filesystem IO occurs. Network egress is restricted exclusively to NVIDIA NIM endpoints.
"""

PAGES["security/policy-enforcement.md"] = """# Policy Enforcement Mechanics

Technical implementation of Layer 1 policy evaluation.

## Rule Matching Algorithm

Rules in `src/policy/matcher.rs` match on:
1. Tool identifier (e.g. `fs:write`, `cli:bash`, `git:commit`)
2. Target path canonicalization (resolving symlinks and `..` traversals)
3. Autonomy mode constraints
4. Effective risk score

Evaluation returns `PolicyDecision::Allow`, `Deny`, `Ask`, or `Escalate`.
"""

PAGES["deployment/overview.md"] = """# Deployment & Release Engineering

Architecture of M31A deployment channels, installers, and release verification.

## Architecture

- Compile-time channel selection: `production` (`m31a`) vs `development` (`m31a-dev`).
- Self-contained binary distribution with zero shared library dependencies.
- Automated update discovery from release manifests.
"""

PAGES["deployment/channels.md"] = """# Deployment Channels & Updates

M31A maintains two completely isolated channels:

| Property | Production Channel (`m31a`) | Development Channel (`m31a-dev`) |
|---|---|---|
| **Binary Name** | `m31a` | `m31a-dev` |
| **Cargo Feature**| Default (no feature) | `--features development` |
| **Global State** | `~/.local/share/m31a/` | `~/.local/share/m31a-dev/` |
| **Update Feed** | `stable` | `development` |
| **Mutual Exclusion**| Fails compile if both set | Fails compile if both set |

## In-Place Updater

```bash
# Check for updates
m31a update --check

# Apply update
m31a update

# Rollback to previous binary
m31a rollback
```
"""

PAGES["deployment/website-hosting.md"] = """# Documentation Website Hosting

Deployment guide for this Docusaurus documentation website at `https://docs.m31a.tonmoyinfrastructure.org/`.

## Hosting Infrastructure

- **Domain**: `docs.m31a.tonmoyinfrastructure.org`
- **Engine**: Docusaurus v3 (Static HTML/JS generation)
- **Base URL**: `/`
- **Output Directory**: `build/`

## Production Build

```bash
cd /home/snigdha/Desktop/docs.m31a.tonmoyinfrastructure.org
npm run build
```

The resulting `build/` directory is completely self-contained and ready for deployment to any static hosting provider (Cloudflare Pages, Vercel, Netlify, Nginx, or AWS S3 + CloudFront).
"""

PAGES["troubleshooting/diagnostics.md"] = """# Diagnostic Procedures & Health Probes

Structured guide for diagnosing runtime issues.

## Diagnostic Commands

```bash
# Complete system diagnosis
m31a doctor

# Category-specific probe
m31a doctor --category environment
m31a doctor --category git
m31a doctor --category models
m31a doctor --category sandbox
m31a doctor --category storage

# Inspect recent execution spans
m31a telemetry inspect <RUN_ID> --spans
```
"""

PAGES["troubleshooting/faq.md"] = """# Frequently Asked Questions (FAQ)

### Q: Why does M31A only support NVIDIA NIM models?
A: High-assurance autonomous engineering requires verified model alignments, deterministic JSON tool calling, and high-throughput streaming. NVIDIA NIM provides standardized enterprise inference endpoints. Other providers are intentionally retired in production to eliminate multi-provider behavioral discrepancies.

### Q: Where does M31A store its database?
A: In platform user data directories (`~/.local/share/m31a/m31a.db` on Linux). It never commits databases into your repository.

### Q: How do I cancel an autonomous task in progress?
A: In the TUI, press `Ctrl+C`. In CLI mode, send `SIGINT` (Ctrl+C). M31A initiates instant cancellation, terminates child process trees, and seals output spools.

### Q: Can M31A run without an internet connection?
A: LLM reasoning requires internet access to reach the NVIDIA NIM endpoint. However, all deterministic verification checks, compilers, linters, and SQLite transactions execute 100% locally on your machine.
"""

def main():
    print(f"Writing {len(PAGES)} comprehensive documentation pages...")
    for rel_path, content in PAGES.items():
        full_path = DOCS_DIR / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
    print(f"Successfully generated all {len(PAGES)} documentation pages.")

if __name__ == "__main__":
    main()
