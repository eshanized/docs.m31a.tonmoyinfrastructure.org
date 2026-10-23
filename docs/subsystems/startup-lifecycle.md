# Subsystem: Application Startup Lifecycle

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
