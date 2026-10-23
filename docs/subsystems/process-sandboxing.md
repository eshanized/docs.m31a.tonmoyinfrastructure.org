# Subsystem: Process Supervision & Sandboxing

Supervises background processes and enforces OS sandboxing (`src/process/`, `src/sandbox/`).

## Process Supervision

- `ProcessTreeController` tracks child PIDs and process groups.
- Validates `/proc/<pid>/stat` start times before sending signals to prevent PID recycling race conditions.
- Captures stdout/stderr into bounded disk spools.
