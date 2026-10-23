# Profiles Reference

M31A includes 10 pre-configured profiles in `assets/profiles/`:

| Profile | Autonomy Mode | Verification Tier | Concurrency | Primary Use Case |
|---|:---:|:---:|:---:|---|
| **`safe`** | Safe | 5 | 2 | Default profile; interactive approvals on all mutations |
| **`coding`** | Assisted | 4 | 4 | General development, automated refactoring |
| **`autonomous`**| Autonomous | 3 | 4 | Large-scale autonomous feature development |
| **`ci`** | Unattended | 5 | 8 | Headless continuous integration automation |
| **`research`** | Plan | 1 | 4 | Read-only codebase exploration and architecture analysis |
| **`security_review`** | Plan | 6 | 2 | Deep security auditing and attack surface evaluation |
| **`release`** | Assisted | 7 | 2 | Release certification across 20-point evidence matrix |
| **`balanced`** | Assisted | 3 | 4 | General daily development |
| **`conservative`** | Safe | 6 | 1 | High-risk production hotfixes |
| **`code_reviewer`** | Plan | 6 | 2 | Automated pull request code reviews |
