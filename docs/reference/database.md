# Database Schema & Migrations Reference

M31A maintains an embedded SQLite database with 32 schema migrations.

## Key Tables

- `execution_runs`: Canonical root orchestrator entities (ID, objective, status, workspace_root).
- `tasks`: Decomposed DAG tasks (run_id, title, status, dependencies).
- `checkpoints`: Durable state snapshots (run_id, manifest_hash, manifest_json).
- `artifacts`: Content-addressed file ledger (run_id, hash, artifact_type, storage_path).
- `verification_checks`: Recorded verification results and evidence hashes.
- `policy_decisions`: Comprehensive audit trail of all policy evaluations.
- `sessions`: Interactive multi-turn developer conversations.
