# Architectural and Behavioral Discrepancies in M31A

This document records contradictions, evolutions, and strict implementation realities discovered during systematic code inspection of the M31 Autonomous (M31A) codebase.

---

## 1. Canonical Root Execution Entity: `ExecutionRun` vs Legacy `Mission`

- **Old Documentation / Intuition**: References `mission` as the primary orchestrator entity and CLI target (`m31a mission run`, `MissionId`).
- **Actual Implementation**:
  - Migrations `030_replace_mission_with_execution_run.sql`, `031_retire_legacy_mission_foreign_keys.sql`, and `032_canonical_execution_run_consolidation.sql` established `execution_runs` as the canonical root execution entity across all 28+ relational tables.
  - In `src/cli/args.rs`, `Commands::Execution` (alias `exec`) and `Commands::Run` are the primary commands. `Commands::Mission` is marked `#[command(hide = true)]` and deprecated.
  - `src/persistence/sqlite/repositories/execution_run.rs` is authoritative; `MissionRepository` is maintained as a legacy compatibility adapter.
- **Documentation Policy**: Document `execution` / `run` as primary, while explaining `mission` as a legacy backward-compatibility layer.

---

## 2. Decommissioned Budget System

- **Old Documentation / Specification**: Described budget tokens, financial caps, currency allocations, and budget ledger tables (`budget_grants`, `budget_ledger`).
- **Actual Implementation**:
  - Migration `029_remove_budget_system.sql` explicitly executed `DROP TABLE budget_grants`, `DROP TABLE budget_ledger`, and `ALTER TABLE missions DROP COLUMN budget`.
  - `tests/docs_contract.rs` has an automated test `test_budget_system_documented_as_decommissioned` asserting that documentation explicitly states the budget system is decommissioned.
  - Execution bounds are enforced not by token budgets, but by:
    1. Step limits (`max_steps` per agent role, default 20-30 steps).
    2. Stall timeouts (`step_stall_timeout_secs`, default 60-90s).
    3. Wall-clock timeouts (`task_wall_clock_timeout_secs`, default 300-900s).
    4. Action failure limits (`max_consecutive_action_failures`, default 3).
    5. Concurrency bounds (`ResourcePolicy`).

---

## 3. Single Production Model Provider: NVIDIA NIM Exclusivity

- **Old Documentation / Generic Agent Assumptions**: Assumed multi-provider support including OpenAI, Anthropic Claude, Google Gemini, Ollama, and local OpenAI-compatible endpoints.
- **Actual Implementation**:
  - `src/config/provider_registry.rs` designates `NvidiaNim` (`nvidia_nim` / `nvidia`) as the sole production provider.
  - Endpoints other than canonical NVIDIA (`https://integrate.api.nvidia.com/v1`) or explicit test endpoints are rejected with `NVIDIA_ONLY_ERROR`: `"Only NVIDIA NIM models are supported in this release."`
  - Retired provider descriptors (`openai`, `anthropic`, `gemini`, `openai_compatible`, `local`, `ollama`) remain in the registry solely to return clear, deterministic rejection diagnostics rather than ambiguous "unknown provider" errors.
  - `Mock` provider exists strictly as test infrastructure in `tests/` and is uncallable from production CLI or TUI commands.

---

## 4. Mutually Exclusive Deployment Channels at Compile-Time

- **Common Cargo Expectation**: Running `cargo test --all-features` or `cargo clippy --all-features`.
- **Actual Implementation**:
  - `src/deployment/channel.rs` contains a `compile_error!` macro triggering when both `feature = "development"` and `feature = "production"` are set simultaneously.
  - The channel identity is compile-time baked into the binary (`m31a` vs `m31a-dev`) and determines global directory isolation (`~/.local/share/m31a` vs `~/.local/share/m31a-dev`). It can never be switched via runtime environment variables like `M31A_ENV`.
  - CI gates and build scripts must run channels separately (`--features development` vs default features).

---

## 5. Strict Fail-Closed Configuration Resolution

- **Permissive Pattern**: Silently falling back to defaults if a configuration file has syntax errors or invalid fields.
- **Actual Implementation**:
  - `src/main.rs` and `src/config/resolved.rs`: If a configuration file exists in `.m31a/config.toml` or `--config <path>` but is malformed, M31A exits immediately with exit code 2 (`M31aExitCode::ConfigError`) and refuses to start on fallback defaults.
  - Fallback defaults are only constructed if there is intentional absence (no config file found anywhere).

---

## 6. Live Test Partition & Deterministic CI

- **False-Green Anti-Pattern**: Tests that attempt to call live APIs and silently return early or skip when credentials are missing.
- **Actual Implementation**:
  - `tests/architecture_live_test_partition.rs` strictly enforces that live model tests are marked `#[ignore]` and cataloged in `tests/support/live_inventory.rs`.
  - Live tests hard-fail with clear diagnostics when invoked without required environment variables, rather than passing silently.
  - CI runs deterministic tests with mock doubles, zero external network dependency.

---

## 7. Ratatui TUI as Pure Projection

- **Common TUI Anti-Pattern**: State stored in UI widgets, screen state driving business logic.
- **Actual Implementation**:
  - The TUI cockpit in `src/tui/` is strictly a read-only projection over SQLite and tokio broadcast channels (`TuiRuntimeBridge`).
  - Terminal actions are dispatched as `RuntimeCommand` into the core composition root (`AppRuntime`), which updates SQLite and emits events. The TUI repaints based on authoritative database updates.
