# Deployment & Release Engineering

Architecture of M31A deployment channels, installers, and release verification.

## Architecture

- Compile-time channel selection: `production` (`m31a`) vs `development` (`m31a-dev`).
- Self-contained binary distribution with zero shared library dependencies.
- Automated update discovery from release manifests.
