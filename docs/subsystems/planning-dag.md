# Subsystem: Planning & DAG Scheduling

Constructs and executes task graphs (`src/planning/`, `src/dag/`, `src/scheduler/`).

## Task Graph Materialization

1. The `planner` proposes tasks and dependencies.
2. `DagValidator` checks for cycles and capability validity.
3. Tasks are materialized into the SQLite `tasks` table with initial status `Pending` or `Blocked`.
4. As upstream tasks succeed, the `Scheduler` admits ready tasks up to concurrency limits.
