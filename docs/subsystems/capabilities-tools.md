# Subsystem: Capabilities & Tools Catalog

The tool catalog (`src/tools/registry.rs`) provides 28 core tools and extended tools.

## Core 28 Tools

- **Filesystem (7)**: `read_file`, `write_file`, `edit_file`, `apply_patch`, `list_files`, `glob`, `grep`.
- **Repository (3)**: `repo_search`, `repo_symbols`, `repo_dependencies`.
- **Process & Jobs (5)**: `run_command`, `start_job`, `job_status`, `job_output`, `job_stop`.
- **Git (8)**: `git_status`, `git_diff`, `git_log`, `git_show`, `git_branch`, `git_checkout`, `git_add`, `git_commit`.
- **QA (3)**: `run_tests`, `run_formatter`, `run_linter`.
- **Artifacts (2)**: `create_artifact`, `read_artifact`.
