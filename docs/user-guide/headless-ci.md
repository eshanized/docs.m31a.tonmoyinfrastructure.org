# Headless Execution & CI Workflows

M31A is designed for headless automation in continuous integration and automated code repair pipelines.

## Stable Exit Codes

CI scripts can reliably branch on M31A's numeric process exit codes (`src/cli/exit_codes.rs`):

| Exit Code | Identifier | Semantic Meaning |
|---|---|---|
| **0** | `Success` | Execution run completed and passed all verification checks |
| **1** | `GeneralError` | Unhandled runtime exception or command failure |
| **2** | `ConfigError` | Invalid or unparseable configuration file |
| **3** | `VerificationFailed` | Nyquist gate failed; tests or compiler checks rejected code |
| **4** | `PolicyViolation` | Action denied by security policy or unattended approval required |
| **5** | `Interrupted` | Execution cancelled by operator or SIGINT/SIGTERM signal |
| **6** | `ResourceExhausted` | Concurrency, timeout, or memory bounds exceeded |
| **7** | `CrashRecovered` | Unhandled crash recovered from durable checkpoint |

## GitHub Actions Example

```yaml
name: Autonomous Code Maintenance

on:
  workflow_dispatch:
  schedule:
    - cron: '0 3 * * 1' # Weekly Monday at 3 AM

jobs:
  m31a-lint-fix:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable
        
      - name: Install M31A
        run: |
          curl -fsSL https://docs.m31a.tonmoyinfrastructure.org/install.sh | bash
          echo "$HOME/.local/bin" >> $GITHUB_PATH
          
      - name: Execute Autonomous Refactor
        env:
          NVIDIA_API_KEY: ${{ secrets.NVIDIA_API_KEY }}
        run: |
          m31a run             --autonomy unattended             --profile ci             --output stream-json             "Fix all clippy warnings and ensure cargo test passes"
            
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v6
        with:
          title: "fix: autonomous clippy remediation"
          branch: "m31a/clippy-fixes"
```
