# Subsystem: Checkpoints & Crash Recovery

Two-phase commit checkpoints and startup recovery (`src/checkpoint/`).

## Crash Recovery Flow

1. On startup, queries `checkpoints` and `execution_runs`.
2. Inspects unsealed spool files and seals them with `[INTERRUPTED]`.
3. Reconciles running jobs and orphan processes.
4. Classifies status into `SafeToResume`, `NeedsRepair`, `Ambiguous`, or `Corrupt`.
