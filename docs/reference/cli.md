# Complete CLI Reference

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
