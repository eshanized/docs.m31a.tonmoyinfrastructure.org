# Subsystem: CLI & Command Dispatch

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
