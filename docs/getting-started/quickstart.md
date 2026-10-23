# 5-Minute Quickstart

Get up and running with M31 Autonomous in less than 5 minutes.

## Prerequisites

1. An **NVIDIA NIM API Key** (obtainable from [build.nvidia.com](https://build.nvidia.com)).
2. An initialized Git repository with code to inspect or modify.

## Step 1: Install M31A

Download and install the standalone binary using our official installation script:

```bash
# On Linux & macOS
curl -fsSL https://docs.m31a.tonmoyinfrastructure.org/install.sh | bash

# On Windows (PowerShell)
irm https://docs.m31a.tonmoyinfrastructure.org/install.ps1 | iex
```

Verify your installation:

```bash
m31a --version
```

Expected output:
```text
m31a 0.1.12 (production, x86_64-unknown-linux-gnu, git:3eddbfd)
```

## Step 2: Configure Your NVIDIA NIM Key

Set your API key in your shell environment:

```bash
export NVIDIA_API_KEY="nvapi-..."
```

Or configure it persistently in M31A's user configuration:

```bash
m31a config set provider.nvidia_nim.api_key "nvapi-..."
```

## Step 3: Run Environmental Doctor

Ensure your environment meets all requirements:

```bash
m31a doctor
```

The doctor probe will verify Git availability, directory permissions, sandbox support, and NVIDIA NIM endpoint connectivity.

## Step 4: Launch Your First Autonomous Run

Navigate to any Git repository and execute an autonomous prompt:

```bash
cd /path/to/your/project

m31a run "Inspect src/main.rs, add comprehensive error logging, and run tests"
```

## Step 5: Explore the Interactive Cockpit

To launch the full interactive Ratatui cockpit:

```bash
m31a
```

Use the interactive cockpit to chat with the planner, approve policy actions, view real-time DAG progression, and inspect diffs.
