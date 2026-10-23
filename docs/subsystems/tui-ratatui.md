# Subsystem: Ratatui TUI Cockpit

The 62-file terminal user interface (`src/tui/`).

## Rendering Pipeline

- First frame rendered synchronously before any async runtime await.
- Event loop polls crossterm input and runtime action channels.
- Renders modular surfaces: Conversation, Tasks, Diff, Settings, Doctor, Model Selector.
