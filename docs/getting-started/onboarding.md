# First-Run Onboarding & Workspace Initialization

When M31A is launched in a workspace for the first time, it ensures the repository is properly configured before executing autonomous work.

## Automatic Onboarding Wizard

If you run `m31a` in a new workspace without prior configuration, the interactive **Workspace Setup Wizard** appears automatically in the cockpit:

```text
┌─────────────────────────── Workspace Setup Wizard ───────────────────────────┐
│                                                                               │
│  Welcome to M31 Autonomous (M31A).                                            │
│  Let's configure this repository for safe, verifiable engineering.            │
│                                                                               │
│  [1] Primary Model: meta/llama-3.2-11b-vision-instruct (NVIDIA NIM)           │
│  [2] Autonomy Mode: Safe (Interactive human confirmation on mutations)        │
│  [3] Git Isolation: Isolated Worktrees (m31a/run/*)                           │
│  [4] Sandbox Policy: Standard (Confinement enabled)                           │
│                                                                               │
│  [ Enter ] Save & Initialize Workspace        [ Esc ] Exit                    │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

## Non-Interactive Workspace Initialization

In headless or CI environments, initialize a workspace non-interactively via:

```bash
m31a init
```

To overwrite existing configuration with defaults:

```bash
m31a init --force
```

## Created Files & Storage Structure

Initialization creates the following files within your repository:

```text
<workspace>/
└── .m31a/
    ├── config.toml           # Workspace configuration overrides
    ├── project/              # Projected planning documents & charters
    └── skills/               # Custom workspace skills (optional)
```

All heavy persistent data (SQLite database, checkpoints, event logs, artifact blobs) is stored in **platform user directories**, keeping your git repository completely clean:
- **Linux**: `~/.local/share/m31a/`
- **macOS**: `~/Library/Application Support/m31a/`
- **Windows**: `%LOCALAPPDATA%\m31a\`
