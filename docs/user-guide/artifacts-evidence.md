# Artifacts, Diffs & Verification Evidence

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
