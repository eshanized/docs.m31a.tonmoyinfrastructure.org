# Interactive Ratatui TUI Cockpit

Launch the cockpit by executing `m31a` with no subcommand in an interactive terminal.

## Cockpit Architecture

The TUI cockpit is powered by Ratatui and Crossterm, running at 30 FPS with bounded channel backpressure. It is strictly a **read-only projection** of the underlying SQLite persistence layer.

```text
┌─ M31 Autonomous Cockpit ──────────────────────────────────── [Mode: Safe] [Profile: Coding] ─┐
│                                                                                               │
│  [Planner] Analyzing repository structure and decomposing objective into 4 DAG tasks...       │
│  ┌─ Task DAG ──────────────────────────────────────────────────────────────────────────────┐ │
│  │ 1. [COMPLETED] Index repository symbols (repo_symbols)                                   │ │
│  │ 2. [RUNNING]   Add error types to src/error.rs (write_file)                              │ │
│  │ 3. [PENDING]   Wire error propagation in src/main.rs                                     │ │
│  │ 4. [PENDING]   Run cargo test verification suite                                         │ │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                               │
│  [Implementer] Proposal: Write 42 lines to `src/error.rs`                                     │
│  [Policy Gate] Policy: ASK (Mutating workspace filesystem)                                    │
│                                                                                               │
│  ┌─ Policy Approval Required ──────────────────────────────────────────────────────────────┐ │
│  │ Tool: fs.write  |  Path: src/error.rs  |  Risk: Medium                                  │ │
│  │ [Y] Approve Action    [N] Deny Action    [D] View Diff    [E] Escalate to Shell         │ │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                               │
├─ Active Run: 01924b12...  Model: meta/llama-3.2-11b-vision-instruct  Tokens: 1,420 ──────────┤
│ > enter prompt or /slash command...                                                           │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Global Keyboard Controls

| Keybinding | Function | Scope |
|---|---|---|
| `Tab` / `Shift+Tab` | Cycle focus between surfaces (Conversation, Tasks, Diff, Settings) | Global |
| `Ctrl+P` | Open Command Palette / Route Navigator | Global |
| `Ctrl+C` | Instant safe cancellation (SIGINT signal escalation) | Global |
| `Ctrl+R` | Replay conversation history / scroll log | Conversation |
| `Ctrl+,` | Open Interactive Settings Editor | Global |
| `Esc` | Close dialog / cancel current input / return to conversation | Modals |
| `PageUp` / `PageDown` | Scroll authoritative conversation or diff viewport | Viewports |
| `Y` / `N` | Approve or Deny pending policy approval dialog | Approval Dialog |

## Integrated Slash Commands

Type `/` in the prompt composer to invoke built-in slash commands:

- `/help` - Show keyboard controls and command catalog.
- `/model [NAME]` - Select or inspect active NVIDIA NIM model.
- `/profile [NAME]` - Switch active profile (`safe`, `coding`, `autonomous`, `ci`, `release`).
- `/autonomy [MODE]` - Switch autonomy mode (`safe`, `plan`, `assisted`, `autonomous`, `unattended`).
- `/clear` - Clear current terminal screen projection (preserves database records).
- `/checkpoint` - Force create an immediate durable checkpoint.
- `/diff` - Toggle full-screen Git diff review surface.
- `/doctor` - Run diagnostic health probes directly in cockpit.
- `/tasks` - Toggle visual DAG progression view.
- `/quit` or `/exit` - Restore terminal and cleanly exit M31A.
