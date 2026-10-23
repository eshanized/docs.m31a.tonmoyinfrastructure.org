# CLI Command Hierarchy & Global Options

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
