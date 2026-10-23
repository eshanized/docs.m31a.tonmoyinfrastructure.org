# Developer Setup & Tooling

How to set up a local development environment for contributing to M31A.

## Prerequisites

- **Rust**: 1.85+ stable (`rustup toolchain install stable`)
- **Git**: 2.30+
- **Make**: GNU Make

## Bootstrap & Build

```bash
git clone https://github.com/eshanized/M31A.git
cd M31A

# Validate environment and toolchain
make bootstrap

# Check compilation across both channels
make check

# Build production binary
make build

# Run deterministic test suite
make test
```
