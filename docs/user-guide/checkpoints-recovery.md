# Checkpoint Restoration & Crash Recovery

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
