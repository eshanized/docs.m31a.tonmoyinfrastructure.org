# Troubleshooting Installation

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
