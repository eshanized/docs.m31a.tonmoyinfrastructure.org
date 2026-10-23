# Tools Catalog Reference

Complete specification of all model-facing tools registered in `ToolRegistry`.

## 28 Core Tools

### Filesystem
- `read_file`: Read contents of file within workspace.
- `write_file`: Overwrite file contents.
- `edit_file`: Contiguous pattern replacement.
- `apply_patch`: Apply unified diff.
- `list_files`: Enumerate workspace files.
- `glob`: Pattern file search.
- `grep`: Regex text search.

### Repository
- `repo_search`: Semantic and keyword code search.
- `repo_symbols`: AST symbol extraction.
- `repo_dependencies`: Module dependency analysis.

### Process & Jobs
- `run_command`: Supervised foreground process execution.
- `start_job`: Background job admission.
- `job_status`: Check job status and PID.
- `job_output`: Stream stdout/stderr.
- `job_stop`: Signal termination.

### Git
- `git_status`, `git_diff`, `git_log`, `git_show`, `git_branch`, `git_checkout`, `git_add`, `git_commit`.

### QA & Artifacts
- `run_tests`, `run_formatter`, `run_linter`, `create_artifact`, `read_artifact`.
