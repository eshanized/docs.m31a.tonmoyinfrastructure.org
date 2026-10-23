# Installation Methods

M31A can be installed via precompiled standalone binaries, package managers, or built from source.

## Method 1: Official Shell Installer (Recommended)

Our verified installer detects your OS architecture, downloads the release binary, verifies SHA-256 checksums, and places `m31a` in your PATH (`~/.local/bin` on Linux/macOS):

```bash
# Linux / macOS
curl -fsSL https://docs.m31a.tonmoyinfrastructure.org/install.sh | bash
```

To install the **development channel** binary (`m31a-dev`):

```bash
curl -fsSL https://docs.m31a.tonmoyinfrastructure.org/install.sh | bash -s -- --channel development
```

### Windows (PowerShell)

```powershell
irm https://docs.m31a.tonmoyinfrastructure.org/install.ps1 | iex
```

## Method 2: Precompiled Binary Releases

Download archive bundles directly from the GitHub Releases page:
[https://github.com/eshanized/M31A/releases](https://github.com/eshanized/M31A/releases)

Available target triples:
- `x86_64-unknown-linux-gnu`
- `aarch64-unknown-linux-gnu`
- `aarch64-apple-darwin` (Apple Silicon M-series)
- `x86_64-apple-darwin` (Intel Mac)
- `x86_64-pc-windows-msvc`

### Checksum Verification

Always verify the SHA-256 hash against `SHA256SUMS.txt`:

```bash
sha256sum -c SHA256SUMS.txt --ignore-missing
```

## Method 3: Building from Source (Cargo)

Prerequisites: Rust 1.85.0+ installed via `rustup`.

```bash
# Clone the repository
git clone https://github.com/eshanized/M31A.git
cd M31A

# Build production binary (release mode)
cargo build --release

# The compiled binary is located at target/release/m31a
cp target/release/m31a ~/.local/bin/
```

To build the development channel binary:

```bash
cargo build --release --features development
# Produces target/release/m31a-dev
```

> **Warning:** Do not run `cargo build --all-features`. The `production` and `development` channels are mutually exclusive; enabling both is a compile-time error.
